from datetime import datetime, timedelta
from termcolor import cprint

def get_week_start_date(prompt=None):
    """Helper function to get the start date of a week"""
    if prompt is None:
        prompt = "\nEnter start date of the week (YYYY-MM-DD), 'prev', 'next' or press Enter for current week: "
        
    start_date_str = input(prompt)
    
    today = datetime.now()
    if not start_date_str:
        start_date = today - timedelta(days=today.weekday())
    elif start_date_str.lower() == 'prev':
        this_monday = today - timedelta(days=today.weekday())
        start_date = this_monday - timedelta(days=7)
    elif start_date_str.lower() == 'next':
        this_monday = today - timedelta(days=today.weekday())
        start_date = this_monday + timedelta(days=7)
    else:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            cprint("Invalid date format. Using current week.", "yellow")
            start_date = today - timedelta(days=today.weekday())
    
    return start_date 