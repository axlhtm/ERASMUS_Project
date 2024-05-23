# =============================================================================
# UFITA Irrigation Networks - Tutorial for Merging Hydraulic Simulation Datasets
# =============================================================================

# IMPORT PYTHON LIBRARIES
import os
import glob
import pandas as pd
import time

# =============================================================================
# END PART - COUNT PROCESSING TIME
# =============================================================================
start_time = time.time()

# =============================================================================
# PART 1: MERGE EXCEL DATASETS WITHIN A FOLDER
# =============================================================================
path = "G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Results/2008/May 2008"

def hydrant_status(): 
    global monthly_hydrant_status
    # Specify the sheet name 
    sheet_name = "Hydrant_Status"  
    # List all excel files in the directory
    all_files = glob.glob(path + "/*.xlsx")
    # Create an empty list to store the DataFrames
    list_dfs = []
    # Loop through all excel files
    for filename in all_files:
      # Read the current excel file into a DataFrame, specifying the sheet name
      df = pd.read_excel(filename, sheet_name=sheet_name)
      # Add the DataFrame to the list
      list_dfs.append(df)
    # Concatenate all DataFrames into a single DataFrame
    monthly_hydrant_status = pd.concat(list_dfs, ignore_index=True)
hydrant_status()

def hydrant_pressure(): 
    global monthly_hydrant_pressure
    # Specify the sheet name 
    sheet_name = "Hydrant_Pressure"
    # List all excel files in the directory
    all_files = glob.glob(path + "/*.xlsx")
    # Create an empty list to store the DataFrames
    list_dfs = []
    # Loop through all excel files
    for filename in all_files:
      # Read the current excel file into a DataFrame, specifying the sheet name
      df = pd.read_excel(filename, sheet_name=sheet_name)
      # Add the DataFrame to the list
      list_dfs.append(df)
    # Concatenate all DataFrames into a single DataFrame
    monthly_hydrant_pressure = pd.concat(list_dfs, ignore_index=True)
hydrant_pressure()

monthly_hydrant_pressure = monthly_hydrant_pressure.drop(monthly_hydrant_pressure.columns[0], axis=1)  # axis=1 specifies columns
monthly_hydrant_status   = monthly_hydrant_status.drop(monthly_hydrant_status.columns[0], axis=1)  # axis=1 specifies columns

# =============================================================================
# PART 2: EXPORT MERGED EXCEL DATASETS
# =============================================================================
os.chdir('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Results/2008/Merged Data/') 

filename = "may_2008_merged.xlsx"  # f-string for formatted output

def Excel_Writer(): 
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    monthly_hydrant_pressure.to_excel(writer, sheet_name='Hydrant_Pressure', index=True)
    monthly_hydrant_status.to_excel(writer, sheet_name='Hydrant_Status', index=True)
    writer.close()
Excel_Writer()

# =============================================================================
# END PART - CALCULATE PROCESSING TIME
# =============================================================================
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time, "seconds")