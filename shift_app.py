import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="Shift App", layout="centered")

st.title("🔁 My Shift Schedule")

# =========================
# Hidden Anchor (DO NOT TOUCH)
# =========================
anchor_date = datetime(2026, 4, 17).date()  # Day 2 Morning
anchor_cycle_day = 1

today = datetime.today().date()

days_since_anchor = (today - anchor_date).days
today_cycle_day = (anchor_cycle_day + days_since_anchor) % 8

# =========================
# Shift Logic
# =========================
def get_shift_status(target_date):
    delta_days = (target_date - today).days
    cycle_day = (today_cycle_day + delta_days) % 8

    if cycle_day == 0:
        return "Morning", "Day 1"
    elif cycle_day == 1:
        return "Morning", "Day 2"
    elif cycle_day == 2:
        return "Off", "Day 1"
    elif cycle_day == 3:
        return "Off", "Day 2"
    elif cycle_day == 4:
        return "Night", "Day 1"
    elif cycle_day == 5:
        return "Night", "Day 2"
    elif cycle_day == 6:
        return "Off", "Day 1"
    elif cycle_day == 7:
        return "Off", "Day 2"

# =========================
# 🎯 TODAY / TOMORROW PANEL
# =========================
st.subheader("📌 Quick View")

today_shift, today_day = get_shift_status(today)
tomorrow_shift, tomorrow_day = get_shift_status(today + timedelta(days=1))

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
    **{today + timedelta(days=1)}**  
    🔵 **{tomorrow_shift}**  
    ({tomorrow_day})
    """)

st.divider()

# =========================
# 🔍 DATE CHECKER
# =========================
st.subheader("🔍 Check Any Date")

input_date = st.date_input("Select a date")

if st.button("Check"):
    shift, day = get_shift_status(input_date)
    st.success(f"{input_date} → {shift} ({day})")

st.divider()

# =========================
# 📅 MONTHLY CALENDAR
# =========================
import calendar

st.subheader("📅 Monthly Calendar View")

year = st.number_input("Year", 2020, 2100, today.year, key="year")
month = st.number_input("Month", 1, 12, today.month, key="month")

def get_color(shift):
    if shift == "Morning":
        return "#4CAF50"  # Green
    elif shift == "Night":
        return "#2196F3"  # Blue
    else:
        return "#9E9E9E"  # Gray

if st.button("Generate Calendar Grid"):
    cal = calendar.monthcalendar(year, month)

    st.markdown("### 🗓️ Calendar")

    # Weekday headers
    cols = st.columns(7)
    for i, day_name in enumerate(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]):
        cols[i].markdown(f"**{day_name}**")

    # Calendar rows
    for week in cal:
        cols = st.columns(7)

        for i, day_num in enumerate(week):
            if day_num == 0:
                cols[i].write("")
            else:
                date_obj = datetime(year, month, day_num).date()
                shift, day = get_shift_status(date_obj)
                color = get_color(shift)

                cols[i].markdown(
                    f"""
                    <div style="
                        background-color:{color};
                        padding:10px;
                        border-radius:10px;
                        text-align:center;
                        color:white;
                        font-size:14px;
                    ">
                        <b>{day_num}</b><br>
                        {shift}<br>
                        {day}
                    </div>
                    """,
                    unsafe_allow_html=True
                )