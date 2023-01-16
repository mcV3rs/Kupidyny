from project.models import UserWedding


def test_new_user_wedding():
    """
    GIVEN a UserWedding model
    WHEN a new UserWedding is created
    THEN check the variables
    """

    user_wedding = UserWedding(wedding_id=1, user_id=1)

    assert user_wedding.get_user_id() == '1'
    assert user_wedding.get_wedding_id() == '1'
    assert user_wedding.__repr__() == '<User_Wedding: 1, 1>'
