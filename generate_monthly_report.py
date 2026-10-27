import os
from datetime import datetime

def save_monthly_report(total_used, water_saved):

    folder = "reports/monthly_reports"

    os.makedirs(folder, exist_ok=True)

    filename = datetime.now().strftime("%B_%Y") + ".txt"

    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as file:

        file.write("MONTHLY WATER REPORT\n")
        file.write("=" * 40 + "\n\n")

        file.write(f"Total Water Used : {total_used} Liters\n")
        file.write(f"Estimated Water Saved : {water_saved} Liters\n")

    print("Monthly Report Saved Successfully")