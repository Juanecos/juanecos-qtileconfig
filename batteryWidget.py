# from libqtile import widget
import subprocess
import re

battery_icons = [
    "󰂃",  # 0-10%
    "󰂃",  # 10-20%
    "󰁺",  # 20-30%
    "󰁻",  # 30-40%
    "󰁼",  # 40-50%
    "󰁽",  # 50-60%
    "󰁾",  # 60-70%
    "󰁿",  # 70-80%
    "󰂀",  # 80-90%
    "󰂁",  # 90-100%
]


def get_battery_percent():
    try:
        output = subprocess.check_output("acpi -b", shell=True, text=True).strip()
        cleaned = re.sub(r"[^0-9.%]", "", output).replace("%", "")
        filtered = f"{cleaned[0]}{cleaned[1]}{cleaned[2]}"
        percent = float(filtered)
        return percent
    except Exception:
        return None
    
def get_battery_icon(percent):
        if percent is None:
                return "N/A"
        index = min(int(percent // 10), len(battery_icons) - 1)
        return battery_icons[index]
                
    

def get_battery_text():
    try:
        percent = get_battery_percent()
        if not percent:
            return "N/A"
        icon = get_battery_icon(percent)
        return f"{icon} {percent:.0f}%"
    except Exception:
        return "N/A"

