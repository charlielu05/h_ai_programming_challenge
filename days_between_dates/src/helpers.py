month_to_dates = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}

def return_date_from_str(date:str)->tuple[int,int,int]:
    year, month, date = [int(d) for d in date.split('-')]
    
    return year, month, date

def is_leap_year(year:int)->bool:
    # function to calculate if leap year
    # divisible by 4 but not divisible by 100
    # divisible by 400
    
    return year % 400 == 0 or year % 4 == 0 and year % 100 != 0

def is_valid_date(year:int, month:int, date:int)->bool:
    valid_year = year >= 0
    valid_month = 1 <= month <= 12
    valid_date = 1 <= date <= 29 if (is_leap_year(year) and month == 2) else 1 <= date <= month_to_dates.get(month)
    
    return valid_year and valid_month and valid_date

def validate_str_date(date:str)->bool:
    # input format is YYYY-MM-DD
    year, month, date = return_date_from_str(date)
    
    return is_valid_date(year, month, date)

def return_leap_years(years:int)->set[int]:
    leap_years = set(
                    filter(lambda x: is_leap_year(x) ,
                            range(1, years)))
    none_leap_years = set(range(1, years)) - leap_years
    
    return leap_years, none_leap_years

def years_to_days(years:int)->int:
    # number of leap years * 366
    # number of none leap years * 365
    
    leap_years, none_leap_years = return_leap_years(years)
    return (366 * len(leap_years)) + (365 * len(none_leap_years))
    
