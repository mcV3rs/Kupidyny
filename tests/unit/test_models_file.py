from project.models import File


def test_new_file():
    """
    GIVEN a File model
    WHEN a new File is created
    THEN check the path
    """

    file = File('test_file.png', wedding_id=1, guest_name="Test")
    assert file.path == 'test_file.png'
    assert file.__repr__() == '<File: test_file.png>'


def test_new_file_with_fixture(new_file):
    """
    GIVEN a File model
    WHEN a new File is created
    THEN check the path is defined correctly
    """

    assert new_file.path == 'test_file.png'
