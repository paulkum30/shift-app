import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

from shift_logic import get_shift_status
from summary import get_monthly_summary
from calendar_view import render_monthly_calendar


# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="My Shift App",
    page_icon="🔁",
    layout="centered"
)


# =========================
# Main Title
# =========================
st.title("🔁 My Shift Schedule")

today = datetime.today().date()
tomorrow = today + timedelta(days=1)


# =========================
# 📌 Quick View
# =========================
st.subheader("📌 Quick View")

today_shift, today_day = get_shift_status(today)
tomorrow_shift, tomorrow_day = get_shift_status(tomorrow)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        ### Today
        **{today}**  
        🟢 **{today_shift}**  
        ({today_day})
        """
    )

with col2:
    st.markdown(
        f"""
        ### Tomorrow
        **{tomorrow}**  
        🔵 **{tomorrow_shift}**  
        ({tomorrow_day})
        """
    )


# =========================
# 📆 Next 7 Days
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

next_days_df = pd.DataFrame(next_days)

st.dataframe(next_days_df, use_container_width=True)

st.divider()


# =========================
# 🔍 Date Checker
# =========================
st.subheader("🔍 Check Any Date")

input_date = st.date_input("Select a date")

if st.button("Check"):
    shift, day = get_shift_status(input_date)
    st.success(f"{input_date} → {shift} ({day})")

st.divider()


# =========================
# 📅 Monthly Calendar
# =========================
st.subheader("📅 Monthly Calendar View")

year = st.number_input(
    "Year",
    min_value=2020,
    max_value=2100,
    value=today.year,
    step=1
)

month = st.number_input(
    "Month",
    min_value=1,
    max_value=12,
    value=today.month,
    step=1
)

render_monthly_calendar(year, month, today)

st.divider()


# =========================
# 📊 Monthly Shift Summary
# =========================
st.subheader("📊 Monthly Shift Summary")

summary_df = get_monthly_summary(year, month)

st.dataframe(summary_df, use_container_width=True)

st.divider()


# =========================
# 🔔 Daily Reminder
# =========================
st.subheader("🔔 Daily Reminder")

if st.button("Show Tomorrow's Shift"):
    shift, day = get_shift_status(tomorrow)
    st.info(f"Tomorrow: {shift} ({day})")