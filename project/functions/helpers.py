import os

from project.models import File


def list_dir(path, extensions):
    """
    Function that returns a list of found files whose extensions match those provided

    :param path: where the files will be searched
    :param extensions: list of extensions to search for
    :return:
    """
    file_list = []
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() in extensions:
            file_list.append(f)

    return file_list


def get_photos(wedding_id=None):
    if wedding_id is None:
        files = File.query.all()
    else:
        files = File.query.filter_by(wedding_id=wedding_id)

    return_paths = []

    for file in files:
        return_paths.append(file.get_path())

    return return_paths
