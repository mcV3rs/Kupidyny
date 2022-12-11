from project.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password_hashed, authenticated, and active fields are defined correctly
    """

    user = User('jgurgul@kupidyn.pl', '!QAZxsw2')
    assert user.email == 'jgurgul@kupidyn.pl'
    assert user.password_hashed != '!QAZxsw2'
    assert user.__repr__() == '<User: jgurgul@kupidyn.pl>'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """

    assert new_user.email == 'jgurgul@kupidyn.pl'
    assert new_user.password_hashed != '!QAZxsw2'


def test_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """

    new_user.set_password('NewPassword')
    assert new_user.password_hashed != 'NewPassword'
    assert new_user.is_password_correct('NewPassword')
    assert not new_user.is_password_correct('NewNewPassword')
    assert not new_user.is_password_correct('FlaskIsAwesome')


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 17
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == '17'
