import numpy as np
import datetime
import math
import re
from typing import Optional

def extract_percent(s: str) -> Optional[float]:
    """Extract the number from a percentage string"""
    match = re.search(r'-?\d+(\.\d+)?', s)
    if match:
        return float(match.group())
    return None

'''def extract_date(s: str) -> Optional[str]:
    match = re.search(r'\b(\d{4})-(\d{2})-(\d{2})\b', s)
    if match:
        return match.group()
    return None'''

def find_closest_date(date_list: list[datetime.date], n: int) -> int:
    """Return index of date that is closest to being n days before today"""
    target_date = datetime.datetime.now().date() - datetime.timedelta(days = n)
    try:
        date_diff = np.abs([date - target_date for date in date_list])
        return date_diff.argmin(0)
    except ValueError:
        print("There were no dates for this stock")

def count_days(horizon: str):
    if horizon == '1_month_return':
        return 30
    elif horizon == '3_month_return':
        return 90
    elif horizon == 'ytd_return':
        now = datetime.datetime.now()
        year_start = datetime.datetime(now.year, 1, 1)
        return (now - year_start).days
    elif horizon == '1_year_return':
        return 365
    elif horizon == '3_year_return':
        return 1095
    else:
        return 1825

def annualized_return(curr_price: float, last_price: float, horizon: str):
    if horizon in {'1_month_return', '3_month_return', 'ytd_return'}:
        return 100.0 * (curr_price-last_price)/last_price
    return 100.0 * (math.pow((curr_price/last_price), 1/(count_days(horizon)/365)) - 1)  # annualize if >= 1 year