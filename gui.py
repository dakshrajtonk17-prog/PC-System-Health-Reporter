
# -----------------------------------------
# PC SYSTEM HEALTH REPORTER - GUI
# -----------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import os

# Import functions from our existing project
from main import (
    get_system_info,
    get_cpu_info,
    get_ram_info,
    get_disk_info,
    get_battery_info,
    get_internet_status,
    get_health_status,
    generate_report
)


# -----------------------------------------
# MAIN WINDOW
# -----------------------------------------

root = tk.Tk()

root.title("PC System Health Reporter")

root.geometry("900x650")

root.configure(bg="#101827")

root.resizable(True, True)


# Store collected information
system_data = None


# -----------------------------------------
# COLORS
# -----------------------------------------

BG = "#101827"
CARD = "#1e293b"
TEXT = "#ffffff"
ACCENT = "#38bdf8"
GREEN = "#22c55e"


# -----------------------------------------
# HEADER
# -----------------------------------------

header = tk.Frame(root, bg=BG)

header.pack(fill="x", padx=30, pady=25)

title = tk.Label(
    header,
    text="PC SYSTEM HEALTH REPORTER",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg=TEXT
)

title.pack(anchor="w")

subtitle = tk.Label(
    header,
    text="Computer Performance & Diagnostic Dashboard",
    font=("Arial", 11),
    bg=BG,
    fg="#94a3b8"
)

subtitle.pack(anchor="w", pady=5)


# -----------------------------------------
# SYSTEM STATUS
# -----------------------------------------

status_frame = tk.Frame(
    root,
    bg=CARD,
    padx=20,
    pady=15
)

status_frame.pack(fill="x", padx=30, pady=10)

status_label = tk.Label(
    status_frame,
    text="System Status: Waiting for Scan",
    font=("Arial", 14, "bold"),
    bg=CARD,
    fg=ACCENT
)

status_label.pack(anchor="w")


# -----------------------------------------
# INFORMATION CARDS
# -----------------------------------------

cards_frame = tk.Frame(root, bg=BG)

cards_frame.pack(fill="x", padx=30, pady=15)


def create_card(parent, title, value, column):

    card = tk.Frame(
        parent,
        bg=CARD,
        padx=20,
        pady=20,
        width=190,
        height=115
    )

    card.grid(row=0, column=column, padx=8, sticky="nsew")

    card.grid_propagate(False)

    heading = tk.Label(
        card,
        text=title,
        font=("Arial", 11),
        bg=CARD,
        fg="#94a3b8"
    )

    heading.pack(anchor="w")

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 23, "bold"),
        bg=CARD,
        fg=TEXT
    )

    value_label.pack(anchor="w", pady=12)

    return value_label


cpu_value = create_card(
    cards_frame, "CPU USAGE", "--", 0
)

ram_value = create_card(
    cards_frame, "RAM USAGE", "--", 1
)

disk_value = create_card(
    cards_frame, "DISK USAGE", "--", 2
)

battery_value = create_card(
    cards_frame, "BATTERY", "--", 3
)


# -----------------------------------------
# SYSTEM DETAILS
# -----------------------------------------

details_frame = tk.Frame(
    root,
    bg=CARD,
    padx=20,
    pady=15
)


details_title = tk.Label(
    details_frame,
    text="SYSTEM INFORMATION",
    font=("Arial", 13, "bold"),
    bg=CARD,
    fg=ACCENT
)

details_title.pack(anchor="w", pady=5)


details_label = tk.Label(
    details_frame,
    text="Click Scan System to collect computer information.",
    font=("Arial", 10),
    bg=CARD,
    fg=TEXT,
    justify="left",
    anchor="nw"
)

details_label.pack(fill="both", expand=True, anchor="nw", pady=10)


# -----------------------------------------
# SCAN SYSTEM FUNCTION
# -----------------------------------------

def scan_system():

    global system_data

    try:

        status_label.config(
            text="System Status: Scanning...",
            fg=ACCENT
        )

        root.update_idletasks()

        system_data = {
            "System": get_system_info(),
            "CPU": get_cpu_info(),
            "RAM": get_ram_info(),
            "Disk": get_disk_info(),
            "Battery": get_battery_info(),
            "Internet": get_internet_status()
        }

        # Update dashboard cards

        cpu_value.config(
            text=system_data["CPU"]["CPU Usage"]
        )

        ram_value.config(
            text=system_data["RAM"]["RAM Usage"]
        )

        disk_value.config(
            text=system_data["Disk"]["Disk Usage"]
        )

        battery_value.config(
            text=system_data["Battery"].get(
                "Battery Percentage", "N/A"
            )
        )

        # Get system health

        health, issues = get_health_status()

        status_label.config(
            text=f"System Status: {health}",
            fg=GREEN if health == "Healthy" else "#f59e0b"
        )

        # Display system details

        details = f"""
Computer Name: {system_data["System"]["Computer Name"]}

Operating System: {system_data["System"]["Operating System"]}

Processor: {system_data["System"]["Processor"]}

CPU Cores: {system_data["CPU"]["CPU Cores"]}

Logical Processors: {system_data["CPU"]["Logical Processors"]}

Total RAM: {system_data["RAM"]["Total RAM"]}

Available RAM: {system_data["RAM"]["Available RAM"]}

Total Storage: {system_data["Disk"]["Total Storage"]}

Free Storage: {system_data["Disk"]["Free Storage"]}

Internet: {system_data["Internet"]}

Health Assessment: {", ".join(issues)}
"""

        details_label.config(text=details)

    except Exception as error:

        messagebox.showerror(
            "Scan Error",
            str(error)
        )


# -----------------------------------------
# GENERATE REPORT FUNCTION
# -----------------------------------------

def create_report():

    global system_data

    try:

        if system_data is None:

            messagebox.showinfo(
                "Information",
                "Please scan your system first."
            )

            return

        report_path = generate_report(system_data)

        messagebox.showinfo(
            "Report Generated",
            f"Your report has been saved:\n\n{report_path}"
        )

        # Open report in default browser
        os.startfile(report_path)

    except Exception as error:

        messagebox.showerror(
            "Report Error",
            str(error)
        )


# -----------------------------------------
# BUTTONS
# -----------------------------------------

button_frame = tk.Frame(root, bg=BG)

button_frame.pack(side="bottom", pady=15)


scan_button = tk.Button(
    button_frame,
    text="SCAN SYSTEM",
    command=scan_system,
    font=("Arial", 11, "bold"),
    bg=ACCENT,
    fg="#101827",
    padx=25,
    pady=12,
    relief="flat",
    cursor="hand2"
)

scan_button.grid(row=0, column=0, padx=12)


report_button = tk.Button(
    button_frame,
    text="GENERATE REPORT",
    command=create_report,
    font=("Arial", 11, "bold"),
    bg=GREEN,
    fg="#101827",
    padx=25,
    pady=12,
    relief="flat",
    cursor="hand2"
)

report_button.grid(row=0, column=1, padx=12)

# Keep buttons visible at the bottom
details_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)

# -----------------------------------------
# START APPLICATION
# -----------------------------------------

root.mainloop()
