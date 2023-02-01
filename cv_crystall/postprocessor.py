import math

import cv2.cv2 as cv2
import numpy as np
from tqdm import tqdm

from .sobel_technique import circular_bluring_kernel


def get_defects(imgs, img_to_draw):
    ans_img = np.copy(img_to_draw)
    ind_technique = 0
    radius = 25
    for img in imgs:
        step = 5
        avg_list = []
        for x in tqdm(range(0, img.shape[0], step), desc='Defects filtering' + str(ind_technique)):
            for y in range(0, img.shape[1], step):
                avg_here = (np.mean(img[x - radius:x + radius, y - radius:y + radius]), y, x)
                if math.isnan(avg_here[0]):
                    continue
                avg_list.append(avg_here)
        ind_technique += 1
        avg_list.sort()
        for avg in avg_list:
            if avg[0] > avg_list[int(len(avg_list)*0.90)][0]:
                cv2.rectangle(ans_img, (avg[1] - radius, avg[2] - radius),
                              (avg[1] + radius, avg[2] + radius),
                              (0, 0, 255), -1)
    return ans_img


def apply(imgs, img_path):
    img = cv2.imread(img_path)
    if img is None:
        print('Image not found.')
        return
    circled_defects = get_defects(imgs, img)
    img = cv2.filter2D(img, -1, circular_bluring_kernel(3) * 8)
    ans_img = cv2.addWeighted(circled_defects, 0.4, img, 1, 1.4)
    cv2.imwrite('input_image.jpg', img)
    return ans_img


def apply_without_processing(imgs, img_path):
    img = cv2.imread(img_path)
    img = cv2.filter2D(img, -1, circular_bluring_kernel(3) * 8)
    if img is None:
        print('Image not found.')
        return
    for img_ in imgs:
        img = cv2.addWeighted(img, 1, img_, 0.4, 1.4)
    return img