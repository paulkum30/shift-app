from datetime import datetime
import calendar
import pandas as pd
from shift_logic import get_shift_status

def get_monthly_summary(year, month):
    summary = {"Morning": 0, "Night": 0, "Off": 0}

    _, total_days = calendar.monthrange(year, month)

    for day_num in range(1, total_days + 1):
        date_obj = datetime(year, month, day_num).date()
        shift, _ = get_shift_status(date_obj)
        summary[shift] += 1

    return pd.DataFrame({
        "Shift": list(summary.keys()),
        "Days": list(summary.values())
    })