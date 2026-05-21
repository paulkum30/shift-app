from datetime import datetime

anchor_date = datetime(2026, 4, 17).date()
anchor_cycle_day = 1

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
    return {
        "Morning": "#4CAF50",
        "Night": "#2196F3",
        "Off": "#9E9E9E",
    }.get(shift, "#9E9E9E")