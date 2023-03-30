import pytest
from helpers import (is_leap_year, 
                     is_valid_date, 
                     validate_str_date, 
                     return_date_from_str,
                     return_leap_years,
                     years_to_days,
                     months_to_days)

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

def test_return_date_from_str():
    assert return_date_from_str("2012-01-10") == (2012, 1, 10)
    assert return_date_from_str("2001-02-29") == (2001, 2, 29)

def test_return_leap_years():
    assert return_leap_years(4) == (set(), set({1,2,3}))
    
def test_years_to_days():
    assert years_to_days(4) == 1095

def test_months_to_days():
    assert months_to_days(year=3, month=3) == 59
    assert months_to_days(year=4, month=3) == 60