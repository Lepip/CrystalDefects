import math

import cv2.cv2 as cv2
import numpy as np
from tqdm import tqdm


def create_args(args):
    if 'step' not in args:
        args['step'] = 5
    if 'border_crop' not in args:
        args['border_crop'] = 10
    if 'corner_crop' not in args:
        args['corner_crop'] = 20
    if 'pic_mode' not in args:
        args['pic_mode'] = True
    if 'save' not in args:
        args['save'] = False
    if 'save_path' not in args:
        args['save_path'] = None
    if 'defect_size' not in args:
        args['defect_size'] = 8
    if 'sensitivity_multiplier' not in args:
        args['sensitivity_multiplier'] = 1
    if 'sensitivity_level' not in args:
        args['sensitivity_level'] = 2
        if 'postprocess' not in args:
            args['postprocess'] = 1
    return args


def circular_bluring_kernel(size):
    """Creates a bluring kernel of 'size' size with a circular square weights"""
    ones = np.ones((size, size), np.float32)
    for i in range(size):
        for j in range(size):
            ones[i][j] = 1 / ((i - size / 2) ** 2 + (j - size / 2) ** 2)
    ones = ones / np.linalg.norm(ones)
    return ones


def process(img, step=5, border_crop=5, corner_crop=50, pic_mode=True, save=False, save_path=None, defect_size=8,
            sensitivity_multiplier=1, sensitivity_level=2):
    """
        Detects defects using OpenCV edge detection.\n
        Default arguments:\n
        step=5 : defects check will be performed every 5 pixels\n
        border_crop=5 : cropping 5 pixels of a border\n
        corner_crop=30 : cropping 30 pixels of each corner\n
        pic_mode=True : show result\n
        save=False : don't save result picture\n
        save_path=None : no save path\n
        defect_size=8 : defect size affects the size of a kernel, which will find defects in pattern with a detail of such
        size.\n
        sensitivity_multiplier=1 : multiplies the sensitivity\n
        sensitivity_level=2 : 1 is linear sensitivity, 2 is quadratic and so on. Can also be fractional.
    """
    print('Performing sobel edge detection - defects detection technique')
    imgx = np.float32(sobel_x(img, 7))
    imgx = cv2.normalize(src=imgx, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    imgxy_blured = cv2.filter2D(imgx, -1, circular_bluring_kernel(3) * 12)
    imgxy = np.float32(sobel_xy(img, 1 + int(defect_size) * 2))
    ans_img = solution_1(cv2.cvtColor(imgxy, cv2.COLOR_BGR2GRAY), imgxy_blured, step, border_crop, corner_crop,
                         sensitivity_multiplier, sensitivity_level)
    if save:
        success = cv2.imwrite(save_path, ans_img)
        if not success:
            print(f'Couldn\'t save in \"{save_path}\" location.')
    if pic_mode:
        cv2.imshow('Result', ans_img)
        cv2.imshow('Input image', imgxy_blured)
        cv2.waitKey(0)
        print('Closing windows...')
        cv2.destroyWindow('Result')
        cv2.destroyWindow('Input image')
    return ans_img


def sobel_xy(img, ksize):
    return cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=ksize)


def sobel_x(img, ksize):
    return cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=ksize)


def sobel_y(img, ksize):
    return cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=ksize)


def in_corner(x, y, corner_crop, x_size, y_size):
    if x ** 2 + y ** 2 < corner_crop ** 2:
        return True
    if (x-x_size) ** 2 + y ** 2 < corner_crop ** 2:
        return True
    if (x - x_size) ** 2 + (y - y_size) ** 2 < corner_crop ** 2:
        return True
    if x ** 2 + (y - y_size) ** 2 < corner_crop ** 2:
        return True
    return False


def solution_1(img, img_to_draw_on, step, border_crop, corner_crop, sensitivity_multiplier, sensitivity_level):
    avg_list = []
    avg_for_mean = []
    for x in tqdm(range(border_crop, img.shape[0] - border_crop, step), desc='Detection progress (sobel)'):
        for y in range(border_crop, img.shape[1] - border_crop, step):
            if in_corner(x, y, corner_crop, img.shape[0], img.shape[1]):
                continue
            avg_here = (np.mean(img[x - step:x + step, y - step:y + step]), y, x)
            if math.isnan(avg_here[0]):
                continue
            avg_for_mean.append(avg_here[0])
            avg_list.append(avg_here)
    avg_list.sort()
    mean = np.mean(avg_for_mean)
    coef = 1 / max(abs(np.max(avg_for_mean) - mean) ** sensitivity_level,
                   abs(np.min(avg_for_mean) - mean) ** sensitivity_level)
    dummy_img = np.copy(img_to_draw_on)
    cv2.rectangle(dummy_img, (0, 0), (dummy_img.shape[0], dummy_img.shape[1]), (0, 0, 0), -1)
    for avg in tqdm(avg_list, desc='Drawing defects'):
        cv2.rectangle(dummy_img, (avg[1] - step // 2, avg[2] - step // 2), (avg[1] + step // 2, avg[2] + step // 2),
                      (0, 0, min(int(255 * (abs(avg[0] - mean) ** sensitivity_level) * coef * sensitivity_multiplier), 255)), -1)
    # dummy_img = cv2.addWeighted(dummy_img, 0.4, img_to_draw_on, 1, 1.4)
    return dummy_img
