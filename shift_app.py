import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import calendar
import streamlit.components.v1 as components

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="My Shift App",
    page_icon="🔁",
    layout="centered"
)

st.title("🔁 My Shift Schedule")


# =========================
# Shift Settings
# =========================
anchor_date = datetime(2026, 4, 17).date()  # Day 2 Morning
anchor_cycle_day = 1

today = datetime.today().date()


# =========================
# Shift Logic
# =========================
def get_shift_status(target_date):
    delta_days = (target_date - anchor_date).days
    cycle_day = (anchor_cycle_day + delta_days) % 8

    shift_pattern = {
        0: ("Morning", "Day 1"),
        1: ("Morning", "Day 2"),
        2: ("Off", "Day 1"),
        3: ("Off", "Day 2"),
        4: ("Night", "Day 1"),
        5: ("Night", "Day 2"),
        6: ("Off", "Day 1"),
        7: ("Off", "Day 2"),
    }

    return shift_pattern[cycle_day]


def get_color(shift):
    colors = {
        "Morning": "#4CAF50",
        "Night": "#2196F3",
        "Off": "#9E9E9E",
    }

    return colors.get(shift, "#9E9E9E")


# =========================
# Quick View
# =========================
st.subheader("📌 Quick View")

today_shift, today_day = get_shift_status(today)
tomorrow = today + timedelta(days=1)
tomorrow_shift, tomorrow_day = get_shift_status(tomorrow)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    ### Today
    **{today}**  
    🟢 **{today_shift}**  
    ({today_day})
    """)

with col2:
    st.markdown(f"""
    ### Tomorrow
    **{tomorrow}**  
    🔵 **{tomorrow_shift}**  
    ({tomorrow_day})
    """)


# =========================
# Next 7 Days
# =========================
st.subheader("📆 Next 7 Days")

next_days = []

for i in range(7):
    date_obj = today + timedelta(days=i)
    shift, day = get_shift_status(date_obj)

    next_days.append({
        "Date": date_obj,
        "Day": date_obj.strftime("%A"),
        "Shift": shift,
        "Cycle Day": day
    })

st.dataframe(pd.DataFrame(next_days), use_container_width=True)

st.divider()


# =========================
# Date Checker
# =========================
st.subheader("🔍 Check Any Date")

input_date = st.date_input("Select a date")

if st.button("Check"):
    shift, day = get_shift_status(input_date)
    st.success(f"{input_date} → {shift} ({day})")

st.divider()


# =========================
# Monthly Calendar
# =========================
st.subheader("📅 Monthly Calendar View")

year = st.number_input("Year", 2020, 2100, today.year, key="year")
month = st.number_input("Month", 1, 12, today.month, key="month")

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


# =========================
# Monthly Shift Summary
# =========================
st.subheader("📊 Monthly Shift Summary")

summary = {
    "Morning": 0,
    "Night": 0,
    "Off": 0
}

_, total_days = calendar.monthrange(year, month)

for day_num in range(1, total_days + 1):
    date_obj = datetime(year, month, day_num).date()
    shift, _ = get_shift_status(date_obj)
    summary[shift] += 1

summary_df = pd.DataFrame({
    "Shift": list(summary.keys()),
    "Days": list(summary.values())
})

st.dataframe(summary_df, use_container_width=True)

st.divider()


# =========================
# Daily Reminder
# =========================
st.subheader("🔔 Daily Reminder")

if st.button("Show Tomorrow's Shift"):
    shift, day = get_shift_status(tomorrow)
    st.info(f"Tomorrow: {shift} ({day})")