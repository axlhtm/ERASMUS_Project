# Import Python Libraries
import glob
import numpy as np
import os 
import pandas as pd
import wntr 

# =============================================================================
# PART VI. DATA VISUALIZATION
# =============================================================================

# IV. 1. Create a Data Frame for Storing Contemporary Hydrant Value
def cont_hydrant_obj(): 
    global cont_hydrant
    months = ["May", "June", "July", "August", "September", "October"]
    index = range(0, 84601, 1800)
    cont_hydrant = pd.DataFrame(index=index, columns=months)
    cont_hydrant[:] = 0
cont_hydrant_obj() 

# IV. 2. Change Working Directory
folder_path = "G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Results/October 2007/"

# Specify the sheet name you want to import (replace with your actual sheet name)
sheet_name = "Hydrant_Status"  # Adjust as needed

# Use glob to find all Excel files (replace *.xlsx with your file pattern if needed)
excel_files = glob.glob(f"{folder_path}/*.xlsx")

# Create a dictionary to store the DataFrames with filenames as keys
dataframes = {}

# Loop through each Excel file
for filename in excel_files:
  # Extract the filename without the path
  file_name = filename.split("/")[-1]  # Adjust based on your path separator
  # Read the specified sheet from the Excel file
  df = pd.read_excel(filename, sheet_name=sheet_name)
  # Add the DataFrame to the dictionary with filename as key
  dataframes[file_name] = df
  
  
a= dataframes["October 2007\\2007-10-05.xlsx"] 
