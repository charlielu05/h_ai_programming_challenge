import pytest
from helpers import is_leap_year, is_valid_date, validate_str_date

def test_is_leap_year():
    assert is_leap_year(1999) == False
    assert is_leap_year(2000) == True
    assert is_leap_year(2022) == False
    assert is_leap_year(2100) == False
    
def test_is_valid_date():
    assert is_valid_date(1999, 12, 31) == True
    assert is_valid_date(2000, 2, 29) == True
    assert is_valid_date(2001, 2, 29) == False

def test_validate_str_date():
    assert validate_str_date("2012-01-10") == True
    assert validate_str_date("2001-02-29") == False