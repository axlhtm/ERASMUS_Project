# Import Python Libraries
import glob
import numpy as np
import os 
import pandas as pd
import wntr 

# =============================================================================
# PART IV. EXPORT HYDRAULIC SIMULATION RESULTS
# =============================================================================

# IV. 1. Change Working Directory
os.chdir('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Results/') 

# IV. 2. Construct the Filename using String Formatting
filename = f"{Hydrant_Operational_Date}.xlsx"  # f-string for formatted output

# IV. 3. Use the variable in the ExcelWriter constructor
def Excel_Writer(): 
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    demand_hydrant_model.to_excel(writer, sheet_name='Hydrant_Demand', index=True)
    pressure_hydrant_model.to_excel(writer, sheet_name='Hydrant_Pressure', index=True)
    status_hydrant_model.to_excel(writer, sheet_name='Hydrant_Status', index=True)
    water_withdrawn_hydrant_model.to_excel(writer, sheet_name='Water_Withdrawn', index=True)
    writer.close()
#Excel_Writer()