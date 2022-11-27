import imghdr
import os


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != '.jpeg' else '.jpg')


def list_dir(path, extensions):
    imgs = []
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() in extensions:
            imgs.append(f)

    return imgs
