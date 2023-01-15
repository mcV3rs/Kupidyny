from datetime import datetime

from project.models import Wedding


def test_new_wedding():
    """
    GIVEN a Wedding model
    WHEN a new Wedding is created
    THEN check the variables
    """

    wedding = Wedding(wife="Justyna", husband="Karol", city="Gliwice", date=datetime(2023, 1, 15))
    assert wedding.get_wife() == "Justyna"
    assert wedding.get_husband() == "Karol"
    assert wedding.get_city() == "Gliwice"
    assert wedding.get_date() == "15.01.2023"
    assert wedding.__repr__() == '<Wedding: Justyna, Karol, Gliwice, 2023-01-15 00:00:00>'
