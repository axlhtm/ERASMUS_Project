import shutil
import os
from datetime import date, timedelta

# Define the original excel file name and path
original_file = "G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Results/Base_Model.xlsx"  # Replace with your actual file name
original_path = "G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Results/2008/December 2008"  # Replace with your folder path

# Starting date (assuming year is 2007)
start_date = date(2008, 12, 1)

# Loop for 31 iterations
for i in range(31):
  # Create new date by adding i days to start_date
  new_date = start_date + timedelta(days=i)

  # Format the date as YYYY-MM-DD
  formatted_date = new_date.strftime("%Y-%m-%d")

  # Construct the new file name with the formatted date
  new_file_name = f"{formatted_date}.xlsx"

  # Construct the full path for the new file
  new_file_path = os.path.join(original_path, new_file_name)

  # Copy the original file to the new path using shutil.copy2
  shutil.copy2(os.path.join(original_path, original_file), new_file_path)

print(f"Successfully copied and renamed the excel file to 31 new files.")
