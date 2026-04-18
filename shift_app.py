import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import calendar

# =========================
# Page Config (ONLY ONCE)
# =========================
st.set_page_config(
    page_title="My Shift App",
    page_icon="🔁",
    layout="centered"
)

st.title("🔁 My Shift Schedule")

# =========================
# Hidden Anchor (DO NOT TOUCH)
# =========================
anchor_date = datetime(2026, 4, 17).date()  # Day 2 Morning
anchor_cycle_day = 1

today = datetime.today().date()

# =========================
# Shift Logic (FIXED - STABLE)
# =========================
def get_shift_status(target_date):
    delta_days = (target_date - anchor_date).days
    cycle_day = (anchor_cycle_day + delta_days) % 8

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
# 📌 TODAY / TOMORROW PANEL
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
                is_today = (date_obj == today)

                border = "3px solid yellow" if is_today else "none"

                cols[i].markdown(
                    f"""
                    <div style="
                        background-color:{color};
                        padding:8px;
                        border-radius:10px;
                        text-align:center;
                        color:white;
                        font-size:13px;
                        line-height:1.2;
                        border:{border};
                    ">
                        <b>{day_num}</b><br>
                        {shift}<br>
                        <small>{day}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# =========================
# 🔔 DAILY REMINDER
# =========================
st.divider()
st.subheader("🔔 Daily Reminder")

if st.button("Show Tomorrow's Shift"):
    tomorrow = today + timedelta(days=1)
    shift, day = get_shift_status(tomorrow)
    st.info(f"Tomorrow: {shift} ({day})")
