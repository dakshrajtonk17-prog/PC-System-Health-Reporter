
import os
import platform
import socket
import psutil
import shutil

from datetime import datetime
from html import escape


print("=" * 50)
print("       PC SYSTEM INFORMATION & HEALTH REPORTER")
print("=" * 50)

print("\nStarting system analysis...")


def get_system_info():

    system_info = {
        "Computer Name": platform.node(),
        "Operating System": platform.system(),
        "Windows Version": platform.version(),
        "Architecture": platform.machine(),
        "Processor": platform.processor(),
        "Boot Time": datetime.fromtimestamp(
            psutil.boot_time()
        ).strftime("%d-%m-%Y %H:%M:%S")
    }

    return system_info


# --------------------------------
# CPU INFORMATION
# --------------------------------

def get_cpu_info():

    cpu_info = {
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical Processors": psutil.cpu_count(logical=True),
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%"
    }

    return cpu_info


# --------------------------------
# RAM INFORMATION
# --------------------------------

def get_ram_info():

    ram = psutil.virtual_memory()

    ram_info = {
        "Total RAM": f"{ram.total / (1024**3):.2f} GB",
        "Used RAM": f"{ram.used / (1024**3):.2f} GB",
        "Available RAM": f"{ram.available / (1024**3):.2f} GB",
        "RAM Usage": f"{ram.percent}%"
    }

    return ram_info


# --------------------------------
# DISK INFORMATION
# --------------------------------

def get_disk_info():

    drive = os.environ.get("SystemDrive", "C:") + "\\"

    disk = shutil.disk_usage(drive)

    disk_info = {
        "Drive": drive,
        "Total Storage": f"{disk.total / (1024**3):.2f} GB",
        "Used Storage": f"{disk.used / (1024**3):.2f} GB",
        "Free Storage": f"{disk.free / (1024**3):.2f} GB",
        "Disk Usage": f"{(disk.used / disk.total) * 100:.2f}%"
    }

    return disk_info


# --------------------------------
# BATTERY INFORMATION
# --------------------------------

def get_battery_info():

    battery = psutil.sensors_battery()

    if battery is None:
        return {
            "Battery": "Not available"
        }

    battery_info = {
        "Battery Percentage": f"{battery.percent}%",
        "Power Connected": (
            "Yes" if battery.power_plugged else "No"
        ),
        "Battery Status": (
            "Charging" if battery.power_plugged else "Discharging"
        )
    }

    if battery.secsleft < 0:
        battery_info["Estimated Time Remaining"] = "Unknown"
    else:
        minutes = battery.secsleft // 60
        battery_info["Estimated Time Remaining"] = f"{minutes} minutes"

    return battery_info


# --------------------------------
# INTERNET CONNECTION CHECK
# --------------------------------

def get_internet_status():

    try:
        connection = socket.create_connection(
            ("1.1.1.1", 53),
            timeout=3
        )

        connection.close()

        return "Connected"

    except OSError:

        return "Not connected / Unavailable"

# --------------------------------
# BASIC SYSTEM HEALTH CHECK
# --------------------------------

def get_health_status():

    ram_usage = psutil.virtual_memory().percent

    cpu_usage = psutil.cpu_percent(interval=1)

    drive = os.environ.get("SystemDrive", "C:") + "\\"

    disk = shutil.disk_usage(drive)

    disk_usage = (disk.used / disk.total) * 100

    issues = []

    if ram_usage >= 85:
        issues.append("High RAM usage")

    if cpu_usage >= 85:
        issues.append("High CPU usage")

    if disk_usage >= 90:
        issues.append("Low disk space")

    if len(issues) > 0:

        return "Attention Required", issues

    else:

        return "Healthy", ["No major resource warning detected"]


# --------------------------------
# HTML REPORT GENERATOR
# --------------------------------

def generate_report(data):

    # Create reports folder if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    # Generate unique report filename
    filename = datetime.now().strftime(
        "PC_Report_%Y%m%d_%H%M%S.html"
    )

    filepath = os.path.join("reports", filename)

    # Get system health
    status, issues = get_health_status()

    # Function to convert dictionary data into HTML tables
    def make_section(title, information):

        rows = ""

        for key, value in information.items():

            rows += f"""
            <tr>
                <td>{escape(str(key))}</td>
                <td>{escape(str(value))}</td>
            </tr>
            """

        return f"""
        <h2>{escape(title)}</h2>
        <table>
            {rows}
        </table>
        """

    # Create HTML document
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>

        <title>PC System Health Report</title>

        <style>

            body {{
                font-family: Arial, sans-serif;
                background: #eef2f7;
                margin: 0;
                padding: 30px;
                color: #222;
            }}

            .container {{
                max-width: 900px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
            }}

            h1 {{
                color: #17365d;
                text-align: center;
            }}

            h2 {{
                color: #24558a;
                margin-top: 30px;
                border-bottom: 2px solid #e5eaf0;
                padding-bottom: 8px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }}

            td:first-child {{
                font-weight: bold;
                width: 40%;
            }}

            .status {{
                padding: 18px;
                background: #e4f5e9;
                border-radius: 8px;
                margin-top: 20px;
            }}

            .warning {{
                background: #fff0d6;
            }}

            .footer {{
                text-align: center;
                margin-top: 35px;
                color: #777;
                font-size: 13px;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>PC System Health Report</h1>

            <p>
                <b>Report Generated:</b>
                {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
            </p>

            <div class="status {'warning' if status != 'Healthy' else ''}">

                <h2>System Status: {escape(status)}</h2>

                <p>{escape(", ".join(issues))}</p>

            </div>

            {make_section("System Information", data["System"])}

            {make_section("CPU Information", data["CPU"])}

            {make_section("RAM Information", data["RAM"])}

            {make_section("Disk Information", data["Disk"])}

            {make_section("Battery Information", data["Battery"])}

            <h2>Internet Connectivity</h2>

            <p>{escape(data["Internet"])}</p>

            <div class="footer">

                Generated by PC System Information
                & Health Reporter

            </div>

        </div>

    </body>
    </html>
    """

    # Save HTML report
    with open(filepath, "w", encoding="utf-8") as file:

        file.write(html_content)

    return os.path.abspath(filepath)


# --------------------------------
# MAIN PROGRAM
# --------------------------------

def main():

    print("\nCollecting computer information...")

    # Collect all information
    data = {
        "System": get_system_info(),
        "CPU": get_cpu_info(),
        "RAM": get_ram_info(),
        "Disk": get_disk_info(),
        "Battery": get_battery_info(),
        "Internet": get_internet_status()
    }

    print("\nGenerating system health report...")

    # Generate report
    report_path = generate_report(data)

    print("\n" + "=" * 45)
    print("REPORT GENERATED SUCCESSFULLY!")
    print("=" * 45)

    print("\nReport location:")
    print(report_path)

    # Ask user whether to open report
    choice = input(
        "\nWould you like to open the report? (y/n): "
    ).lower().strip()

    if choice == "y":

        os.startfile(report_path)

    print("\nThank you for using PC System Health Reporter!")


# Program execution starts here

if __name__ == "__main__":

    main()
