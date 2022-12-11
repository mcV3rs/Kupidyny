from project.models import File


def test_new_file():
    """
    GIVEN a File model
    WHEN a new File is created
    THEN check the name
    """

    file = File('test_file.png')
    assert file.name == 'test_file.png'
    assert file.__repr__() == '<File: test_file.png>'


def test_new_file_with_fixture(new_file):
    """
    GIVEN a File model
    WHEN a new File is created
    THEN check the name is defined correctly
    """

    assert new_file.name == 'test_file.png'
