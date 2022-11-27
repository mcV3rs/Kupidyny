import os


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
