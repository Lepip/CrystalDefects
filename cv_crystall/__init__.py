from . import main


def windowed_mode(img_path, **args):
    if args is None:
        args = {}
    technique = main.Technique.ALL
    if 'technique' in args:
        technique = args['technique']
    main.windowed_mode(img_path, technique, args)


def process_image(img_path, **args):
    if args is None:
        args = {}
    technique = main.Technique.SOBEL
    if 'technique' in args:
        technique = args['technique']
    return main.process_image(img_path, technique, args)
