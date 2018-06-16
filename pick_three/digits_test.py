# coding=utf-8
"""
Exercise digits
"""

from pick_three.digits_class import Digits

def test_basics():
    digits = Digits(123, 3)
    assert len(digits.chosen) == 3
    digits = Digits(123, 4)
    assert len(digits.chosen) == 4

def test_invalids():
    try:
        digits = Digits(-1, 3)
        digits = Digits(0, 3)
        digits = Digits(123, -1)
        raise TypeError("Expected errors for these junk inputs")
        assert False, "Expected errors for these junk inputs"
    except Exception as ex:
        assert True
