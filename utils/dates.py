from datetime import datetime


def in_current_financial_year(date: datetime) -> bool:
    today = datetime.today()
    if today.month >= 7:
        fy_start = datetime(today.year, 7, 1)
        fy_end = datetime(today.year + 1, 6, 30)
    else:
        fy_start = datetime(today.year - 1, 7, 1)
        fy_end = datetime(today.year, 6, 30)

    return fy_start <= date <= fy_end
