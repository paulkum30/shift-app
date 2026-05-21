import calendar
from datetime import datetime
import streamlit.components.v1 as components

from shift_logic import get_shift_status, get_color


def render_monthly_calendar(year, month, today):
    """
    Renders a mobile-friendly monthly shift calendar.

    Args:
        year (int): The selected year.
        month (int): The selected month.
        today (date): Today's date.
    """

    cal = calendar.monthcalendar(year, month)

    calendar_html = """
    <style>
    .shift-calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 4px;
        width: 100%;
    }

    .day-header {
        text-align: center;
        font-weight: bold;
        font-size: 12px;
    }

    .day-card {
        min-height: 58px;
        border-radius: 8px;
        padding: 5px 2px;
        text-align: center;
        color: white;
        font-size: 11px;
        line-height: 1.2;
        box-sizing: border-box;
    }

    .day-number {
        font-weight: bold;
        font-size: 13px;
    }

    .shift-text {
        font-size: 10px;
    }

    .cycle-day {
        font-size: 9px;
    }

    .empty-day {
        min-height: 58px;
    }

    .today-card {
        border: 3px solid #FFD700;
    }

    @media (max-width: 480px) {
        .shift-calendar {
            gap: 2px;
        }

        .day-card {
            min-height: 50px;
            padding: 4px 1px;
            font-size: 9px;
            border-radius: 6px;
        }

        .day-number {
            font-size: 11px;
        }

        .shift-text {
            font-size: 8px;
        }

        .cycle-day {
            font-size: 7px;
        }

        .day-header {
            font-size: 10px;
        }
    }
    </style>

    <div class="shift-calendar">
    """

    for day_name in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        calendar_html += f'<div class="day-header">{day_name}</div>'

    for week in cal:
        for day_num in week:
            if day_num == 0:
                calendar_html += '<div class="empty-day"></div>'
            else:
                date_obj = datetime(year, month, day_num).date()
                shift, day = get_shift_status(date_obj)
                color = get_color(shift)

                today_class = "today-card" if date_obj == today else ""

                calendar_html += f"""
                <div class="day-card {today_class}" style="background-color:{color};">
                    <div class="day-number">{day_num}</div>
                    <div class="shift-text">{shift}</div>
                    <div class="cycle-day">{day}</div>
                </div>
                """

    calendar_html += "</div>"

    components.html(calendar_html, height=430, scrolling=False)