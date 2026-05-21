# 🔁 Shift Schedule App

A Python + Streamlit application for tracking rotating shift schedules.

Built for shift workers who need a simple and reliable way to:
- track work rotations,
- view future schedules,
- check shift patterns,
- and analyze monthly work distribution.

---

# ✨ Features

## 📌 Quick View
- Displays today's shift
- Displays tomorrow's shift

## 📆 Next 7 Days
- Shows upcoming shifts for the next week

## 🔍 Date Checker
- Check the shift for any selected date

## 📅 Monthly Calendar
- Responsive calendar view
- Mobile-friendly layout
- Color-coded shifts
- Highlights current day

## 📊 Monthly Shift Summary
- Counts:
  - Morning shifts
  - Night shifts
  - Off days

## 🔔 Daily Reminder
- Quick reminder for tomorrow’s shift

---

# 🔄 Current Shift Rotation

2 Morning → 2 Off → 2 Night → 2 Off

Cycle length: 8 days

---

# 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- HTML/CSS (inside Streamlit)

---

# 📁 Project Structure

```text
shift_app/
│
├── app.py
├── shift_logic.py
├── calendar_view.py
├── summary.py
├── requirements.txt
└── README.md