from project.models import File


def get_photos(wedding_id: int = None) -> list[str]:
    """
    Functions listing all pictures in location and returnint it as list of strings.
    If additional parameter wedding_id is provided, then a function will only return a files connected to a given wedding

    :param wedding_id:
    :return:
    """
    if wedding_id is None:
        files = File.query.all()
    else:
        files = File.query.filter_by(wedding_id=wedding_id)

    return_paths = []

    for file in files:
        return_paths.append(file.get_path())

    return return_paths


def get_photos_with_names(wedding_id: int) -> dict[str: str]:
    """
    Functions listing all pictures in location and returnint it as dictionary of filenames in DB and paths
    If additional parameter wedding_id is provided, then a function will only return a files connected to a given wedding

    :param wedding_id:
    :return:
    """
    files = File.query.filter_by(wedding_id=wedding_id)

    return_paths = {}

    for row in files:
        return_paths[row.get_guest_name()] = row.get_path()

    return return_paths
