# calculate days between two dates given as string format YYYY-MM-DD
# leap year feb has 29 days instead of 28
# Note that start and end day should not be counted and we only care about the absolute difference in dates. 
# If the order of two dates being compared is flipped the difference remains the same.

from helpers import return_date_from_str, years_to_days
from dataclasses import dataclass

@dataclass
class Date:
    year: int
    month: int
    date: int
    
def days_between_dates(date_1: str, date_2:str):
    pass

def convert_to_days(date:Date)->int:
    years_days = years_to_days(date.year)
    
    return years_days

if __name__ == "__main__":
    date_1 = "2012-01-10" 
    date_2 = "2012-01-11"
    
    date_1_repr = Date(*return_date_from_str(date_1))
    date_2_repr = Date(*return_date_from_str(date_2))

    test = convert_to_days(date_1_repr)
    
    # assert days_between_dates("2012-01-10", "2012-01-11") == 0


