import os
from datetime import datetime

def save_analytics(avg_usage, max_usage):

    folder = "reports/analytics"

    os.makedirs(folder, exist_ok=True)

    filename = datetime.now().strftime("%Y_%m_%d") + ".txt"

    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as file:

        file.write("SMART WATER ANALYTICS\n")
        file.write("=" * 40 + "\n\n")

        file.write(f"Average Usage : {avg_usage} Liters\n")
        file.write(f"Maximum Usage : {max_usage} Liters\n")

    print("Analytics Report Saved Successfully")