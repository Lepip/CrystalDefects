import cv2.cv2 as cv2
from enum import Enum
from . import sobel_technique
from . import postprocessor


class Technique(Enum):
    ALL = 0
    SOBEL = 1


def process_image(img_path, technique, args):
    if technique == Technique.ALL:
        imgs = [
            apply_technique_image(img_path, Technique.SOBEL, args),

        ]
    else:
        imgs = [apply_technique_image(img_path, technique, args)]
    if 'postprocess' not in args or args['postprocess'] == 1:
        ans_img = postprocessor.apply(imgs, img_path)
    else:
        ans_img = postprocessor.apply_without_processing(imgs, img_path)
    return ans_img


def apply_technique_image(img_path, technique, args):
    img = cv2.imread(img_path)
    if img is None:
        print('Image not found.')
        return

    if technique == Technique.SOBEL:
        if args is not None and len(args) > 0:
            args = sobel_technique.create_args(args)
            pre_processed = sobel_technique.process(img, args['step'], args['border_crop'], args['corner_crop'], args['pic_mode'],
                                    args['save'], args['save_path'], args['defect_size'],
                                    args['sensitivity_multiplier'], args['sensitivity_level'])
            return pre_processed
        else:
            return sobel_technique.process(img)
        return

    print('Technique not found.')


class Args:
    pass


def windowed_mode(img_path, technique, args):
    img = cv2.imread(img_path)
    if img is None:
        print('Image not found.')
        return

    if technique == Technique.SOBEL or technique == Technique.ALL:
        args = sobel_technique.create_args(args)
        window_name = 'Crystal Defect Detector'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.createTrackbar("step", window_name, 4, 20, nothing)
        cv2.setTrackbarPos("step", window_name, args['step'])
        cv2.createTrackbar("border_crop", window_name, 0, 50, nothing)
        cv2.setTrackbarPos("border_crop", window_name, args["border_crop"])
        cv2.createTrackbar("corner_crop", window_name, 0, 50, nothing)
        cv2.setTrackbarPos("corner_crop", window_name, args["corner_crop"])
        cv2.createTrackbar('defect_size', window_name, 0, 15, nothing)
        cv2.setTrackbarPos('defect_size', window_name, args['defect_size'])
        cv2.createTrackbar('sens_mult', window_name, 1, 200, nothing)
        cv2.setTrackbarPos('sens_mult', window_name, args['sensitivity_multiplier']*10)
        cv2.createTrackbar('sens_lvl', window_name, 1, 50, nothing)
        cv2.setTrackbarPos('sens_lvl', window_name, args['sensitivity_level']*10)
        cv2.createTrackbar('Proceed', window_name, 0, 1, do_image)
        cv2.createTrackbar('Save', window_name, 0, 1, do_save)
        cv2.createTrackbar('postprocess', window_name, 0, 1, nothing)
        cv2.setTrackbarPos('postprocess', window_name, args['postprocess'])
        scaled_img = cv2.resize(img, (40, img.shape[0]*40//img.shape[0]))
        cv2.imshow(window_name, scaled_img)
        Args.img_path = img_path
        Args.save_slot = 0
        key = cv2.waitKey(0)
        # while True:
        #     key = cv2.waitKey(1)
        #     if key == ord('q'):
        #         break
        return
    print('Technique not found.')


def nothing(x):
    pass


def get_args_from_window():
    window_name = 'Crystal Defect Detector'
    args = {
        'step': cv2.getTrackbarPos('step', window_name),
        "border_crop": cv2.getTrackbarPos("border_crop", window_name),
        "corner_crop": cv2.getTrackbarPos("corner_crop", window_name),
        'defect_size': cv2.getTrackbarPos('defect_size', window_name),
        'sensitivity_multiplier': cv2.getTrackbarPos('sens_mult', window_name)/10,
        'sensitivity_level': cv2.getTrackbarPos('sens_lvl', window_name)/10,
        'pic_mode': False,
        'postprocess': cv2.getTrackbarPos('postprocess', window_name),
    }
    return args


def do_image(x):
    if x == 1:
        args = get_args_from_window()
        ans_img = process_image(Args.img_path, Technique.ALL, args)
        Args.img = ans_img
        cv2.imshow('Crystal Defect Detector', ans_img)


def do_save(x):
    if x == 1:
        cv2.imwrite('result_image' + str(Args.save_slot) + '.jpg', Args.img)

def apply_postprocess(*imgs):
    pass