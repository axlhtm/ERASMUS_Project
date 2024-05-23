# =============================================================================
# GREEN VALVE SYSTEM AND OASIS ANALYSIS - MERGE HYDRAULIC SIMULATION DATASETS
# =============================================================================

# IMPORT PYTHON LIBRARIES
import glob
import numpy as np
import matplotlib.pyplot as plt
import os 
import pandas as pd
import time

start_time = time.time()

# SETH WORKING DIRECTORY FOLDER
path = "G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Results/2008/January 2008"  # Replace with your path to the folder containing excel files

# PART I - NUMERICAL PARAMETER 
num_nodes   = 574
num_istanti = 365 * 48 # Number of half an hour in a year
Q           = 5 # [l/s] flowrate
eta_gen     = 0.8 # [%] efficiency of the generator
rho         = 1000 # [kg/m3] density
g           = 9.8125# [m/s2]
powerLimit  = 20 # W
brakeAngle  = 8 # degree
P_min       = 20 #[m] minimum pressure at the hydrants
time_step   = dt = 0.5 #dt
OAS_size    = np.ones(500, dtype=int) * 2  # Initialize with 2 for all time steps
days_per_month  = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] # No. of days each months 
num_mezzore     = [x * 48 for x in days_per_month] # No of half hours each months
months_names= ['january','february','march','april','may','june','july','august','september','october','november','december']

# =============================================================================
# GVS PART I: SEPARATE HYDRANTS PRESSURE AND ACTIVATIONS BASED ON REGION
# =============================================================================
# Identify hydrants ID for each region
def hydrants_ID(): 
    global Name_Hydrants_ALL, Name_Hydrants_EAST, Name_Hydrants_WEST
    file_path = "G:/My Drive/Work Data/PT. Cipta Harmoni Hutama/Hydroinformatics/ERASMUS_Project/Green Valve System/Hydrant_Names.xlsx"  # Replace with your actual file path
    sheet_ALL = "ALL"
    sheet_EAST = "EAST"
    Name_Hydrants_ALL  = pd.read_excel(file_path, sheet_name=sheet_ALL)
    Name_Hydrants_ALL  = Name_Hydrants_ALL["Hydrant_Name"].tolist()
    
    List_HD_EAST = pd.read_excel(file_path, sheet_name=sheet_EAST)
    List_HD_EAST = List_HD_EAST["Hydrant_Name"].tolist()
    
    Name_Hydrants_EAST = [col for col in Name_Hydrants_ALL if col in List_HD_EAST]
    Name_Hydrants_WEST = [col for col in Name_Hydrants_ALL if col not in List_HD_EAST]
hydrants_ID()

# Separate hydrants pressure based on region
def pressure_by_zone(folder_path):
  """
  This function processes pressure data by zone for all excel files in a folder.

  Args:
      folder_path (str): Path to the folder containing the excel files.

  Returns:
      dict, dict: Pressure_EAST and Pressure_WEST dictionaries containing pressure data for each zone per file.
  """
  Pressure_EAST = {}
  Pressure_WEST = {}
  sheet_pressure = "Hydrant_Pressure"

  # Loop through all excel files in the folder
  for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
      file_path = os.path.join(folder_path, filename)
      
      # Read the current excel file
      monthly_simulation_pressure = pd.read_excel(file_path, sheet_name=sheet_pressure)

      # Filter data for each zone
      monthly_simulation_pressure_EAST = monthly_simulation_pressure[Name_Hydrants_EAST]
      monthly_simulation_pressure_WEST = monthly_simulation_pressure[Name_Hydrants_WEST]

      # Extract month information from filename (assuming consistent naming)
      month = filename.split("_")[0]

      # Add data for the current month to dictionaries
      Pressure_EAST[month] = monthly_simulation_pressure_EAST
      Pressure_WEST[month] = monthly_simulation_pressure_WEST

  return Pressure_EAST, Pressure_WEST
Pressure_EAST, Pressure_WEST = pressure_by_zone('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Results/2008/Merged Data/')

# Separate hydrants activations based on region
def activations_by_zone(folder_path):
  """
  This function processes hydrants status data by zone for all excel files in a folder.

  Args:
      folder_path (str): Path to the folder containing the excel files.

  Returns:
      dict, dict: Activations_EAST and Activations_WEST dictionaries containing Activations data for each zone per file.
  """
  Activations_EAST = {}
  Activations_WEST = {}
  sheet_Activations = "Hydrant_Status"

  # Loop through all excel files in the folder
  for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
      file_path = os.path.join(folder_path, filename)
      
      # Read the current excel file
      monthly_simulation_Activations = pd.read_excel(file_path, sheet_name=sheet_Activations)

      # Filter data for each zone
      monthly_simulation_Activations_EAST = monthly_simulation_Activations[Name_Hydrants_EAST]
      monthly_simulation_Activations_WEST = monthly_simulation_Activations[Name_Hydrants_WEST]

      # Extract month information from filename (assuming consistent naming)
      month = filename.split("_")[0]

      # Add data for the current month to dictionaries
      Activations_EAST[month] = monthly_simulation_Activations_EAST
      Activations_WEST[month] = monthly_simulation_Activations_WEST

  return Activations_EAST, Activations_WEST
Activations_EAST, Activations_WEST = activations_by_zone('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Results/2008/Merged Data/')

# Delete VASCAGRANDE node 
def delete_columns_in_dict_dfs(data_dict, columns_to_delete):
  """
  Deletes specified columns from DataFrames within a dictionary.

  Args:
      data_dict (dict): A dictionary where values are DataFrames.
      columns_to_delete (list): A list of column names to delete.

  Returns:
      dict: A new dictionary with DataFrames having specified columns deleted.
  """
  updated_dict = {}
  for key, value in data_dict.items():
    # Check if the value is a DataFrame
    if isinstance(value, pd.DataFrame):
      # Delete specified columns
      updated_df = value.drop(columns_to_delete, axis=1)
    else:
      # Keep non-DataFrame values as they are
      updated_df = value
    updated_dict[key] = updated_df
  return updated_dict
Pressure_WEST = delete_columns_in_dict_dfs(Pressure_WEST.copy(), ["VASCA_GRANDE"])
Activations_WEST = delete_columns_in_dict_dfs(Activations_WEST.copy(), ["VASCA_GRANDE"])

# =============================================================================
# GVS PART II: CONCATENATED PRESSURE AND ACTIVATIONS BASED ON REGIONS
# =============================================================================
# Filter the pressure matrix based on the activation of the hydrants and fin the minimum pressure
def min_pressure_filtered(): 
    global Pressure_EAST_Filtered,Pressure_WEST_Filtered, minimum_EAST, minimum_WEST
    Pressure_EAST_Filtered = {}
    for name, df_A in Pressure_EAST.items():
      df_B = Activations_EAST[name]
      Pressure_EAST_Filtered[name] = df_A * df_B
    Pressure_WEST_Filtered = {}
    for name, df_C in Pressure_WEST.items():
      df_D = Activations_WEST[name]
      Pressure_WEST_Filtered[name] = df_C * df_D
    minimum_EAST = [] 
    for name, df in Pressure_EAST_Filtered.items():
        minimum_EAST.append(df[df > 0].min().min())  
    minimum_WEST = [] 
    for name, df in Pressure_WEST_Filtered.items():
        minimum_WEST.append(df[df > 0].min().min())  
min_pressure_filtered()

def pres_con_east():
    global Pressure_EAST_concatenated
    Pressure_EAST_concatenated = pd.DataFrame()
    for df_name in months_names:
        df = Pressure_EAST_Filtered[df_name]  # Access DataFrame for the current month
        Pressure_EAST_concatenated = pd.concat([Pressure_EAST_concatenated, df], ignore_index=True)
pres_con_east()
def pres_con_west():
    global Pressure_WEST_concatenated
    Pressure_WEST_concatenated = pd.DataFrame()
    for df_name in months_names:
        df = Pressure_WEST_Filtered[df_name]  # Access DataFrame for the current month
        Pressure_WEST_concatenated = pd.concat([Pressure_WEST_concatenated, df], ignore_index=True)
pres_con_west()
def acti_con_east(): 
    global Activations_EAST_conc
    Activations_EAST_conc = pd.DataFrame()
    for df_name in months_names:
        df = Activations_EAST[df_name]  # Access DataFrame for the current month
        Activations_EAST_conc = pd.concat([Activations_EAST_conc, df], ignore_index=True)
acti_con_east()
def acti_con_west(): 
    global Activations_WEST_conc
    Activations_WEST_conc = pd.DataFrame()
    for df_name in months_names:
        df = Activations_WEST[df_name]  # Access DataFrame for the current month
        Activations_WEST_conc = pd.concat([Activations_WEST_conc, df], ignore_index=True)
acti_con_west()

# =============================================================================
# GVS PART II: CHECK PRESSURE AVAILABILITY FOR GREEN VALVE SYSTEM
# =============================================================================
vector_support_EAST = [0 for _ in range(206)]
vector_support_WEST = [0 for _ in range(367)]
DP_GV_EAST = []
DP_GV_WEST = []
#DP_GV_EAST = [0 for _ in range(len(Pressure_EAST_concatenated))]
#DP_GV_WEST = [0 for _ in range(len(Pressure_WEST_concatenated))]
P_net_EAST = Pressure_EAST_concatenated.copy()
P_net_EAST[:] = 0
P_net_WEST = Pressure_WEST_concatenated.copy()
P_net_WEST[:] = 0

for i in range(len(Pressure_EAST_concatenated)):
    vector_support_EAST = Pressure_EAST_concatenated.iloc[i, :]
    vector_support_WEST = Pressure_WEST_concatenated.iloc[i, :]
    # Find the minimum pressure value in each time step (i)`
    mask_EAST = vector_support_EAST != 0
    min_EAST  = vector_support_EAST[mask_EAST].min()
    mask_WEST = vector_support_WEST != 0
    min_WEST  = vector_support_WEST[mask_WEST].min()
    # Substract the minimum pressure at each time step (i) with hydrant minimum pressure 20m
    if min_EAST == 0 : 
        dp_EAST = 0 
    else: 
        dp_EAST = min_EAST - P_min
        
    if min_WEST == 0 : 
        dp_WEST = 0 
    else: 
        dp_WEST = min_WEST - P_min
    # Make a series with size of all nodes in the system which filled with dp_EAST and dp_WEST value
    dp_EAST_rep = [dp_EAST for _ in range(Pressure_EAST_concatenated.shape[1])] 
    dp_WEST_rep = [dp_WEST for _ in range(Pressure_WEST_concatenated.shape[1])] 
    # Subtract the GV head for each active node in the Net
    P_net_EAST_temp = vector_support_EAST - Activations_EAST_conc.iloc[i, :] * dp_EAST_rep 
    P_net_WEST_temp = vector_support_WEST - Activations_WEST_conc.iloc[i, :] * dp_WEST_rep 
    P_net_EAST.loc[i] = P_net_EAST_temp
    P_net_WEST.loc[i] = P_net_WEST_temp
    DP_GV_EAST.append(dp_EAST)
    DP_GV_WEST.append(dp_WEST)
    print (i)
    
# =============================================================================
# GVS PART III: CHECK ENERGY RECOVERY FOR GREEN VALVE SYSTEM
# =============================================================================
Size_GV_EAST = 6 # [inches]
Size_GV_WEST = 4 # [inches]

# Total number of activations for each time step
activations_count_EAST = (Activations_EAST_conc.sum(axis=1)).tolist()
activations_count_WEST = (Activations_WEST_conc.sum(axis=1)).tolist()

# Flowrate for each hydrant multiplied by the total number of activations (5L/s)
Q_EAST_GV = [element * 5 for element in activations_count_EAST]
Q_WEST_GV = [element * 5 for element in activations_count_WEST]

# Calculate Flow Coefficient (CV), Available Power (Pow), Opening Adjustment, and Efficiency
CV_Necessary_EAST_GV    = []
Pow_available_GV_EAST   = []
opening_GV_EAST         = []
Efficiency_GV_EAST      = []
for i in range(len(Pressure_EAST_concatenated)):
    # Necessary flow coefficient computation
    CV_Necessary_EAST_GV.append((Q_EAST_GV[i]*3.6)/(0.865*((DP_GV_EAST[i]*0.09806)**0.5)))
    # Total available power for the GV
    Pow_available_GV_EAST.append(rho * g * (Q_EAST_GV[i]/1000) * (DP_GV_EAST[i]))
    # GV opening derivation from flow coefficient
    opening_GV_EAST.append(0.019866185 
                           * (CV_Necessary_EAST_GV[i] / (Size_GV_EAST**2))**4 - 0.337964376
                           * (CV_Necessary_EAST_GV[i] / (Size_GV_EAST**2))**3 + 1.243263993
                           * (CV_Necessary_EAST_GV[i] / (Size_GV_EAST**2))**2 + 8.69532324
                           * (CV_Necessary_EAST_GV[i] / (Size_GV_EAST**2)) + 0.970542041) 
    # Opening adjustments
    if opening_GV_EAST[i] > 100 :
        opening_GV_EAST[i] = 100
    elif opening_GV_EAST[i] < 0 : 
        opening_GV_EAST[i] = 0
    opening_GV_EAST[i] = opening_GV_EAST[i] / 100*(90 - brakeAngle)+brakeAngle
        
    # Efficiency definition as a function of the opening
    Efficiency_GV_EAST.append((-9.18759E-10 *(opening_GV_EAST[i])**5
                             +2.58404E-07 *(opening_GV_EAST[i])**4 
                             -2.54209E-05 *(opening_GV_EAST[i])**3 
                             +0.000972469 *(opening_GV_EAST[i])**2 
                             -0.009785738 *(opening_GV_EAST[i])
                             +0.032159983 ) * eta_gen)

CV_Necessary_WEST_GV    = []
Pow_available_GV_WEST   = []
opening_GV_WEST         = []
Efficiency_GV_WEST      = []
for i in range(len(Pressure_WEST_concatenated)):
    # Necessary flow coefficient computation
    CV_Necessary_WEST_GV.append((Q_WEST_GV[i]*3.6)/(0.865*((DP_GV_WEST[i]*0.09806)**0.5)))
    # Total available power for the GV
    Pow_available_GV_WEST.append(rho * g * (Q_WEST_GV[i]/1000) * (DP_GV_WEST[i]))
    # GV opening derivation from flow coefficient
    opening_GV_WEST.append(0.019866185 
                           * (CV_Necessary_WEST_GV[i] / (Size_GV_WEST**2))**4 - 0.337964376
                           * (CV_Necessary_WEST_GV[i] / (Size_GV_WEST**2))**3 + 1.243263993
                           * (CV_Necessary_WEST_GV[i] / (Size_GV_WEST**2))**2 + 8.69532324
                           * (CV_Necessary_WEST_GV[i] / (Size_GV_WEST**2)) + 0.970542041) 
    # Opening adjustments
    if opening_GV_WEST[i] > 100 :
        opening_GV_WEST[i] = 100
    elif opening_GV_WEST[i] < 0 : 
        opening_GV_WEST[i] = 0
    opening_GV_WEST[i] = opening_GV_WEST[i] / 100*(90 - brakeAngle)+brakeAngle
        
    # Efficiency definition as a function of the opening
    Efficiency_GV_WEST.append((-9.18759E-10 *(opening_GV_WEST[i])**5
                             +2.58404E-07 *(opening_GV_WEST[i])**4 
                             -2.54209E-05 *(opening_GV_WEST[i])**3 
                             +0.000972469 *(opening_GV_WEST[i])**2 
                             -0.009785738 *(opening_GV_WEST[i])
                             +0.032159983 ) * eta_gen)

# Calculate Recovered Energy with GV
Recovered_Energy_GV_EAST = []
Recovered_Energy_GV_WEST = []
for i in range(len(Pressure_EAST_concatenated)):
    Recovered_Energy_GV_EAST.append(Pow_available_GV_EAST[i] * Efficiency_GV_EAST[i] * 0.5 )
    Recovered_Energy_GV_WEST.append(Pow_available_GV_WEST[i] * Efficiency_GV_WEST[i] * 0.5 )
    
# =============================================================================
# GVS PART IV: CHECK GVS CONSUMPTION
# =============================================================================
start_columns = [0, 1488, 2832, 4320, 5760, 7248, 8688, 10176, 11664, 13104, 14592, 16032]
end_columns   = [1488, 2832, 4320, 5760, 7248, 8688, 10176, 11664, 13104, 14592, 16032, 17520]

# Initialize dictionaries for Open_GV_EAST and Open_GV_WEST
Open_GV_EAST = {}
Open_GV_WEST = {}

# Loop through months (assuming months_names is a list of month names)
def open_GV(): 
    global Open_GV_EAST, Open_GV_WEST
    for month in range(0, 12):
        month_name = months_names[month]  # Access month name by index (0-based)
        start = start_columns[month]  # Access start index by index (0-based)
        finish = end_columns[month]  # Access finish index by index (0-based)
        # Extract data matrix for the current month
        mat_EST  = opening_GV_EAST[start:finish]  
        mat_WEST  = opening_GV_WEST[start:finish]  
        # Add data matrix to the dictionary with month name as key
        Open_GV_EAST[month_name] = mat_EST
        Open_GV_WEST[month_name] = mat_WEST
open_GV()

# Initiation of active GV in binary structure
Active_GV_EST  = {key: [1 if val > 0 and not pd.isna(val) else 0 for val in Open_GV_EAST[key]] for key in Open_GV_EAST}
Active_GV_WEST = {key: [1 if val > 0 and not pd.isna(val) else 0 for val in Open_GV_WEST[key]] for key in Open_GV_WEST}

# I computed the number of consecutive active time step for each month
# in excel, and based on that I computed the number of communications
# for each month. Then, to add this consumption to the code, I divided
# the total monthly consumption equally per each half an hour of each
# month

Consumption_EAST_GV = [720, 720, 720, 720, 1994.5, 2448.5, 3165.3333, 3185, 2575, 888.833333, 720, 720]
Consumption_WEST_GV = [720, 720, 720, 720, 1728.5, 2058.8333, 3084.666667, 3080.833333, 2447.833333, 772.8333333, 720, 720]
half_hours_month    = num_mezzore

# Calculation of daily consumption for each month
consumption_half_hour_month = np.divide(Consumption_EAST_GV, half_hours_month)

consumption_GV_EAST = []
for i in range(len(Consumption_EAST_GV)):
  # Repeat daily consumption using numpy.tile
  consumption_GV_EAST.extend(np.tile(consumption_half_hour_month[i], half_hours_month[i]))
final_consumption_GV_EAST = np.cumsum(consumption_GV_EAST)

consumption_GV_WEST = []
for i in range(len(Consumption_WEST_GV)):
  # Repeat daily consumption using numpy.tile
  consumption_GV_WEST.extend(np.tile(consumption_half_hour_month[i], half_hours_month[i]))
final_consumption_GV_WEST = np.cumsum(consumption_GV_WEST)

# Replace NaN with 0 for EAST network
Recovered_Energy_GV_EST_clean = np.where(np.isnan(Recovered_Energy_GV_EAST), 0, Recovered_Energy_GV_EAST)

# Replace NaN with 0 for WEST network
Recovered_Energy_GV_WEST_clean = np.where(np.isnan(Recovered_Energy_GV_WEST), 0, Recovered_Energy_GV_WEST)

# Calculate final recovery for EAST network
final_recovery_GV_EAST = np.cumsum(Recovered_Energy_GV_EST_clean)

# Calculate final recovery for WEST network
final_recovery_GV_WEST = np.cumsum(Recovered_Energy_GV_WEST_clean)

# X coordinates for the months
x_coords = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]

# =============================================================================
# OASIS ANALYSIS
# =============================================================================

# =============================================================================
# OASIS PART I: AVAILABLE PRESSURE, POWER AND REQUIRED FLOW COEFFICIENT
# =============================================================================
# Find rows where at least one element is nonzero
nonzero_rows_EAST = np.any(P_net_EAST, axis=0)
nonzero_rows_WEST = np.any(P_net_WEST, axis=0)

# Filter original matrices based on non-zero rows
P_net_EAST_filt = P_net_EAST.T[nonzero_rows_EAST]
Activations_EAST_filt = Activations_EAST_conc.T[nonzero_rows_EAST]
P_net_WEST_filt = P_net_WEST.T[nonzero_rows_WEST]
Activations_WEST_filt = Activations_WEST_conc.T[nonzero_rows_WEST]

# Create Matrix that calculates necessary CV node by node hour per hour
Press_available_EAST = np.zeros_like(P_net_EAST_filt)
Pow_available_EAST = np.zeros_like(P_net_EAST_filt)
CV_required_EAST = np.zeros_like(P_net_EAST_filt)

# Cycle for each node and each hour in the matrix EAST
for node in range (P_net_EAST_filt.shape[0]):
    for hour in range (P_net_EAST_filt.shape[1]):
        # Check if the node is active
        if Activations_EAST_filt.iloc[node, hour] == 1: 
            # Check if the pressure exceeds the limit
            if P_net_EAST_filt.iloc[node, hour] >= P_min: 
                # Calculate the pressure difference and insert into Press_available_EAST
                Press_available_EAST[node, hour] = P_net_EAST_filt.iloc[node, hour] - P_min
                # Calculate available power and CV at the node
                Pow_available_EAST[node, hour]   = (rho * g * (Q/1000) * (Press_available_EAST[node, hour]))
                CV_required_EAST[node, hour]     = ((Q * 3.6) / (0.865 * ((Press_available_EAST[node, hour] * 0.09806)**0.5)))
            else : 
                # Insert 0 if the pressure is equal or lower than the minimum value
                Press_available_EAST[node, hour]= 0
                Pow_available_EAST[node, hour]  = 0
                CV_required_EAST[node, hour]    = 0
        else : 
            # Fill with 0 if the node is not active
            Press_available_EAST[node, hour] = 0
            Pow_available_EAST[node, hour]   = 0
            CV_required_EAST[node, hour]     = 0
            
# Create Matrix that calculates necessary CV node by node hour per hour
Press_available_WEST = np.zeros_like(P_net_WEST_filt)
Pow_available_WEST = np.zeros_like(P_net_WEST_filt)
CV_required_WEST = np.zeros_like(P_net_WEST_filt)

# Cycle for each node and each hour in the matrix WEST
for node in range (P_net_WEST_filt.shape[0]):
    for hour in range (P_net_WEST_filt.shape[1]):
        # Check if the node is active
        if Activations_WEST_filt.iloc[node, hour] == 1: 
            # Check if the pressure exceeds the limit
            if P_net_WEST_filt.iloc[node, hour] >= P_min: 
                # Calculate the pressure difference and insert into Press_available_WEST
                Press_available_WEST[node, hour] = P_net_WEST_filt.iloc[node, hour] - P_min
                # Calculate available power and CV at the node
                Pow_available_WEST[node, hour]   = (rho * g * (Q/1000) * (Press_available_WEST[node, hour]))
                CV_required_WEST[node, hour]     = ((Q * 3.6) / (0.865 * ((Press_available_WEST[node, hour] * 0.09806)**0.5)))
            else : 
                # Insert 0 if the pressure is equal or lower than the minimum value
                Press_available_WEST[node, hour]= 0
                Pow_available_WEST[node, hour]  = 0
                CV_required_WEST[node, hour]    = 0
        else : 
            # Fill with 0 if the node is not active
            Press_available_WEST[node, hour] = 0
            Pow_available_WEST[node, hour]   = 0
            CV_required_WEST[node, hour]     = 0
            
# =============================================================================
# OASIS ANALYSIS PART II: ANALYSING THE OPENING AND EFFICIENCY IN EACH REGION
# =============================================================================
def Opening_Effieciency_OAS_East(): 
    global OAS_opening_EAST, OAS_efficiency_EAST
    OAS_opening_EAST = np.zeros_like(CV_required_EAST)
    OAS_efficiency_EAST = np.zeros_like(CV_required_EAST)
    # Calculate the value of opening on east region
    for i in range (CV_required_EAST.shape[0]):
        for j in range (CV_required_EAST.shape[1]):
            OAS_opening_EAST[i, j] = 0.00147470153299696 * (CV_required_EAST[i, j])**4 \
                                  - 0.030736861804376 * (CV_required_EAST[i, j])**3 \
                                  - 0.182356368565236 * (CV_required_EAST[i, j])**2 \
                                  + 8.41199017155187 * (CV_required_EAST[i, j]) - 7.73246122232044E-14
            if OAS_opening_EAST[i, j] > 100: 
                OAS_opening_EAST[i, j] = 100 
            elif OAS_opening_EAST[i, j] < 1:
                OAS_opening_EAST[i, j] = 0
    # Calculate the value of efficiency on east region
    for i in range (CV_required_EAST.shape[0]):
        for j in range (CV_required_EAST.shape[1]):
            if OAS_opening_EAST[i, j] == 0 :
                OAS_efficiency_EAST[i,j] = 0
            else : 
                OAS_efficiency_EAST[i, j] = ((-4.55851424972361E-08 * (OAS_opening_EAST[i, j])**5 \
                                              + 0.00001592406009907 * (OAS_opening_EAST[i, j])**4 \
                                              - 0.00179911621964658 * (OAS_opening_EAST[i, j])**3 \
                                              + 0.06654449421999400 * (OAS_opening_EAST[i, j])**2 \
                                              + 1.55056331925843E-13) / 100) * eta_gen
            if OAS_efficiency_EAST[i,j] < 0.002 :
                OAS_efficiency_EAST[i,j] = 0
Opening_Effieciency_OAS_East()

def Opening_Effieciency_OAS_West(): 
    global OAS_opening_WEST, OAS_efficiency_WEST
    OAS_opening_WEST = np.zeros_like(CV_required_WEST)
    OAS_efficiency_WEST = np.zeros_like(CV_required_WEST)
    # Calculate the value of opening on west region
    for i in range (CV_required_WEST.shape[0]):
        for j in range (CV_required_WEST.shape[1]):
            OAS_opening_WEST[i, j] = 0.00147470153299696 * (CV_required_WEST[i, j])**4 \
                                  - 0.030736861804376 * (CV_required_WEST[i, j])**3 \
                                  - 0.182356368565236 * (CV_required_WEST[i, j])**2 \
                                  + 8.41199017155187 * (CV_required_WEST[i, j]) - 7.73246122232044E-14
            if OAS_opening_WEST[i, j] > 100: 
                OAS_opening_WEST[i, j] = 100 
            elif OAS_opening_WEST[i, j] < 1:
                OAS_opening_WEST[i, j] = 0
    # Calculate the value of efficiency on west region
    for i in range (CV_required_WEST.shape[0]):
        for j in range (CV_required_WEST.shape[1]):
            if OAS_opening_WEST[i, j] == 0 :
                OAS_efficiency_WEST[i,j] = 0
            else : 
                OAS_efficiency_WEST[i, j] = ((-4.55851424972361E-08 * (OAS_opening_WEST[i, j])**5 \
                                              + 0.00001592406009907 * (OAS_opening_WEST[i, j])**4 \
                                              - 0.00179911621964658 * (OAS_opening_WEST[i, j])**3 \
                                              + 0.06654449421999400 * (OAS_opening_WEST[i, j])**2 \
                                              + 1.55056331925843E-13) / 100) * eta_gen
            if OAS_efficiency_WEST[i,j] < 0.002 :
                OAS_efficiency_WEST[i,j] = 0
Opening_Effieciency_OAS_West()

# =============================================================================
# OASIS ANALYSIS PART III: POWER AND ENERGY RECOVERED
# =============================================================================
# Recovered energy computation [Wh]
Pow_recovered_EAST = Pow_available_EAST * OAS_efficiency_EAST
Recovered_Energy_EAST = Pow_recovered_EAST * time_step

Pow_recovered_WEST = Pow_available_WEST * OAS_efficiency_WEST
Recovered_Energy_WEST = Pow_recovered_WEST * time_step

# =============================================================================
# OASIS ANALYSIS PART IV: ENERGY CONSUMPTION 
# =============================================================================
Deep_Sleep_consumption  = 0.0001 # [W]
Standby_consumption     = 0.0005 # [W]
Active_consumption      = 0.001 # [W]
dt = 0.5#%  [h]
movement_consumption    = 40 * 10 / 3600 # [W] % 40 Watt, each movement lasting 10 seconds converted in [hours]

# Deep Sleep First interval
vector_1 = list(range(0,5760)) # Columns in the data matrices between January and May
# Deep Sleep Second interval
vector_2 = list(range(14592,17520)) # Columns in the data matrices between January and May
# Concatenation of the two vectors
indices_deep_sleep_column = vector_1 + vector_2

# matrices and structures initialization
consumption_EAST = Activations_EAST_filt * 0 
consumption_WEST = Activations_WEST_filt * 0 
modality_EAST    = Activations_EAST_filt * 0 
modality_WEST    = Activations_WEST_filt * 0 

def optimize_loop_EAST(Activations_EAST_filt, indices_deep_sleep_column,
                  Deep_Sleep_consumption, dt, Active_consumption, Standby_consumption):
  # Use vectorized operations for efficiency
  is_deep_sleep = np.isin(np.arange(Activations_EAST_filt.shape[1]), indices_deep_sleep_column)  # Vectorized check
  modality_EAST = np.where(is_deep_sleep, 'deep_sleep',
                           np.where(Activations_EAST_filt == 1, 'active', 'standby'))
  consumption_EAST = np.where(is_deep_sleep, Deep_Sleep_consumption * dt,
                              np.where(Activations_EAST_filt == 1, Active_consumption * dt,
                                       Standby_consumption * dt))
  return modality_EAST, consumption_EAST

modality_EAST_optimized, consumption_EAST_optimized = optimize_loop_EAST(
    Activations_EAST_filt, indices_deep_sleep_column,
    Deep_Sleep_consumption, dt, Active_consumption, Standby_consumption)
modality_EAST       = modality_EAST_optimized
consumption_EAST    = consumption_EAST_optimized

def optimize_loop_WEST(Activations_WEST_filt, indices_deep_sleep_column,
                  Deep_Sleep_consumption, dt, Active_consumption, Standby_consumption):
  # Use vectorized operations for efficiency
  is_deep_sleep = np.isin(np.arange(Activations_WEST_filt.shape[1]), indices_deep_sleep_column)  # Vectorized check
  modality_WEST = np.where(is_deep_sleep, 'deep_sleep',
                           np.where(Activations_WEST_filt == 1, 'active', 'standby'))
  consumption_WEST = np.where(is_deep_sleep, Deep_Sleep_consumption * dt,
                              np.where(Activations_WEST_filt == 1, Active_consumption * dt,
                                       Standby_consumption * dt))
  return modality_WEST, consumption_WEST

modality_WEST_optimized, consumption_WEST_optimized = optimize_loop_WEST(
    Activations_WEST_filt, indices_deep_sleep_column,
    Deep_Sleep_consumption, dt, Active_consumption, Standby_consumption)
modality_WEST       = modality_WEST_optimized
consumption_WEST    = consumption_WEST_optimized

# =============================================================================
# OASIS ANALYSIS PART V: MOVING CONSUMPTION 
# =============================================================================
# Anytime the activation logical parameter changes add a movement consumption
for row in range (Activations_EAST_filt.shape[0]):
    for column in range (1, Activations_EAST_filt.shape[1]):
        print(row, column)
        if Activations_EAST_filt.iloc[row, column] != Activations_EAST_filt.iloc[row, column - 1]:
            # Add the movement consumption to the corresponding value of consumption
            consumption_EAST[row, column] = consumption_EAST[row, column] + movement_consumption
            print(consumption_EAST[row, column])
        else : 
            pass

for row in range (Activations_WEST_filt.shape[0]):
    for column in range (1, Activations_WEST_filt.shape[1]):
        print(row, column)
        if Activations_WEST_filt.iloc[row, column] != Activations_WEST_filt.iloc[row, column - 1]:
            # Add the movement consumption to the corresponding value of consumption
            consumption_WEST[row, column] = consumption_WEST[row, column] + movement_consumption
            print(consumption_WEST[row, column])
        else : 
            pass

# =============================================================================
# OASIS ANALYSIS PART VI: COMMUNICATION CONSUMPTION 
# =============================================================================
Pow_communication           = 40 # [W]
duration_communication      = 10 # [s]
En_communication            = Pow_communication * duration_communication/3600 # [Wh]
Communication_consumption   = np.zeros_like(consumption_EAST)

# Define occurrence frequency for the different modalities
occurrence_frequency_deepsleep  = 10 * 48 # [half an hour]
occurrence_frequency_active     = 10 # [10 times every half an hour, that is every 3 minutes]
occurrence_frequency_standby    = 3  #[every 10 minutes]

communication_consumption_EAST  = np.zeros_like(consumption_EAST)
communication_consumption_WEST  = np.zeros_like(consumption_WEST)
[num_rows_EAST, num_columns]    = consumption_EAST.shape
num_rows_WEST                   = consumption_WEST.shape[0]

# Communication consumption for active and standby modality in EAST network
for row in range(num_rows_EAST):
  for column in range(num_columns):
      # Active modality
      print(row, column)
      if modality_EAST [row, column] ==  'active':
          communication_consumption_EAST[row, column] = En_communication * occurrence_frequency_active
      # Standby modality
      elif modality_EAST [row, column] == 'standby':
          communication_consumption_EAST[row, column] = En_communication * occurrence_frequency_standby
      # Deepsleep modality
      else: 
          pass

# Communication consumption for active and standby modality in WEST network
for row in range(num_rows_WEST):
  for column in range(num_columns):
      # Active modality
      print(row, column)
      if modality_WEST [row, column] ==  'active':
          communication_consumption_WEST[row, column] = En_communication * occurrence_frequency_active
      # Standby modality
      elif modality_WEST [row, column] == 'standby':
          communication_consumption_WEST[row, column] = En_communication * occurrence_frequency_standby
      # Deepsleep modality
      else: 
          pass

# Communication consumption for deep sleep modality in EAST and WEST network
indices_deep_sleep = [1, 481, 961, 1441, 1488, 1489, 1969, 2449, 2832, 2833, 3313, 3793, 4320, 4321, 4801, 5281, 5760, 14593, 15073, 15553, 16032, 16033, 16513, 16993, 17473, 17520];
indices_deep_sleep = [x - 1 for x in indices_deep_sleep]
for i in range(len(indices_deep_sleep)): 
    communication_consumption_EAST[:, indices_deep_sleep[i]] = communication_consumption_EAST[:, indices_deep_sleep[i]] + En_communication
    communication_consumption_WEST[:, indices_deep_sleep[i]] = communication_consumption_WEST[:, indices_deep_sleep[i]] + En_communication

# Total consumption matrix
consumption_EAST = consumption_EAST + communication_consumption_EAST
consumption_WEST = consumption_WEST + communication_consumption_WEST

# =============================================================================
# OASIS ANALYSIS PART VII - CLASSIFICATION OF BALANCES BASED ON OPERATING HOURS
# =============================================================================
# Calculate recovery energy classification in each region
def recov_energy_class_EAST(): 
    global Recovery_less_than_50_EAST, Recovery_50_100_EAST, Recovery_100_150_EAST, \
           Recovery_150_200_EAST, Recovery_200_250_EAST, Recovery_more_than_250_EAST 
    num_active_EAST = []
    for i in modality_EAST:
        num_active_EAST.append(sum(element == 'active' for element in i))
    # Find indices for different ranges
    indices_less_than_50_EAST   = [i for i, count in enumerate(num_active_EAST) if count < 50]
    indices_50_to_100_EAST      = [i for i, count in enumerate(num_active_EAST) if 50 <= count < 100]
    indices_100_to_150_EAST     = [i for i, count in enumerate(num_active_EAST) if 100 <= count < 150]
    indices_150_to_200_EAST     = [i for i, count in enumerate(num_active_EAST) if 150 <= count < 200]
    indices_200_to_250_EAST     = [i for i, count in enumerate(num_active_EAST) if 200 <= count < 250]
    indices_more_than_250_EAST  = [i for i, count in enumerate(num_active_EAST) if count >= 250]
    # Extract corresponding rows from Recovered_Energy_EAST
    Recovery_less_than_50_EAST  = Recovered_Energy_EAST[indices_less_than_50_EAST]
    Recovery_50_100_EAST        = Recovered_Energy_EAST[indices_50_to_100_EAST]
    Recovery_100_150_EAST       = Recovered_Energy_EAST[indices_100_to_150_EAST]
    Recovery_150_200_EAST       = Recovered_Energy_EAST[indices_150_to_200_EAST]
    Recovery_200_250_EAST       = Recovered_Energy_EAST[indices_200_to_250_EAST]
    Recovery_more_than_250_EAST = Recovered_Energy_EAST[indices_more_than_250_EAST]
recov_energy_class_EAST()
def recov_energy_class_WEST(): 
    global Recovery_less_than_50_WEST, Recovery_50_100_WEST, Recovery_100_150_WEST, \
           Recovery_150_200_WEST, Recovery_200_250_WEST, Recovery_more_than_250_WEST 
    num_active_WEST = []
    for i in modality_WEST:
        num_active_WEST.append(sum(element == 'active' for element in i))
    # Find indices for different ranges
    indices_less_than_50_WEST   = [i for i, count in enumerate(num_active_WEST) if count < 50]
    indices_50_to_100_WEST      = [i for i, count in enumerate(num_active_WEST) if 50 <= count < 100]
    indices_100_to_150_WEST     = [i for i, count in enumerate(num_active_WEST) if 100 <= count < 150]
    indices_150_to_200_WEST     = [i for i, count in enumerate(num_active_WEST) if 150 <= count < 200]
    indices_200_to_250_WEST     = [i for i, count in enumerate(num_active_WEST) if 200 <= count < 250]
    indices_more_than_250_WEST  = [i for i, count in enumerate(num_active_WEST) if count >= 250]
    # Extract corresponding rows from Recovered_Energy_WEST
    Recovery_less_than_50_WEST  = Recovered_Energy_WEST[indices_less_than_50_WEST]
    Recovery_50_100_WEST        = Recovered_Energy_WEST[indices_50_to_100_WEST]
    Recovery_100_150_WEST       = Recovered_Energy_WEST[indices_100_to_150_WEST]
    Recovery_150_200_WEST       = Recovered_Energy_WEST[indices_150_to_200_WEST]
    Recovery_200_250_WEST       = Recovered_Energy_WEST[indices_200_to_250_WEST]
    Recovery_more_than_250_WEST = Recovered_Energy_WEST[indices_more_than_250_WEST]
recov_energy_class_WEST()

# =============================================================================
# GVS AND OASIS ANALYSIS: PLOTS
# =============================================================================

# =============================================================================
# GVS AND OASIS ANALYSIS: PLOTS FOR PRESSURE BEFORE AND AFTER GVS IN EACH REGIONS
# =============================================================================
# Define pressure differences ante and post gv in each region
def pressure_dif_gv(): 
    global max_P_anteGV_EAST, max_P_postGV_EAST, max_P_anteGV_WEST, max_P_postGV_WEST
    max_P_anteGV_EAST = [0] * 17520  
    max_P_postGV_EAST = [0] * 17520
    for column_EAST in range(P_net_EAST.shape[0]):
        max_P_anteGV_EAST[column_EAST] = max(Pressure_EAST_concatenated.iloc[column_EAST, :])
        max_P_postGV_EAST[column_EAST] = max(P_net_EAST.iloc[column_EAST, :])
    max_P_anteGV_WEST = [0] * 17520  
    max_P_postGV_WEST = [0] * 17520
    for column_WEST in range(P_net_WEST.shape[0]):
        max_P_anteGV_WEST[column_WEST] = max(Pressure_WEST_concatenated.iloc[column_WEST, :])
        max_P_postGV_WEST[column_WEST] = max(P_net_WEST.iloc[column_WEST, :])
    # Replace nan with 0 
    max_P_postGV_EAST = list(map(lambda x: 0 if pd.isna(x) else x, max_P_postGV_EAST))
    max_P_postGV_WEST = list(map(lambda x: 0 if pd.isna(x) else x, max_P_postGV_WEST))    
pressure_dif_gv()
# Plot pressure differences 
def plot_pressure_dif_gv_EAST(): 
    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Create the high-resolution figure
    plt.figure(figsize=(8, 6), dpi=300)  # Adjust figure size and resolution as needed
    # Plot the EAST Region
    ## Plot the pressure distribution before the GVS
    for i in range(P_net_EAST.shape[1]):
        plt.plot(x, P_net_EAST.iloc[:, i ], 'bo')
    ## Plot the pressure distribution after the GVS
    for i in range(Pressure_EAST_concatenated.shape[1]):
        plt.plot(x, Pressure_EAST_concatenated.iloc[:, i ], 'ro')
    plt.plot(x, max_P_anteGV_EAST, 'r', label='Before GV Installation', linewidth=2)
    plt.plot(x, max_P_postGV_EAST[:], 'b', label='After GV Installation', linewidth=2)
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)
    # Set Y-Axis range and ticks
    plt.ylim(0, 100)  # Set y-axis limits from 0 to 100
    plt.yticks(range(0, 121, 10)) 
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.ylabel('Pressure (m)')
    plt.title('Pressure Distribution within Eastern Network')
    plt.legend(loc='upper left') 
plot_pressure_dif_gv_EAST()
def plot_pressure_dif_gv_WEST(): 
    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Create the high-resolution figure
    plt.figure(figsize=(8, 6), dpi=300)  # Adjust figure size and resolution as needed
    # Plot the WEST Region
    ## Plot the pressure distribution before the GVS
    for i in range(P_net_WEST.shape[1]):
        plt.plot(x, P_net_WEST.iloc[:, i ], 'bo')
    ## Plot the pressure distribution after the GVS
    for i in range(Pressure_WEST_concatenated.shape[1]):
        plt.plot(x, Pressure_WEST_concatenated.iloc[:, i ], 'ro')
    plt.plot(x, max_P_anteGV_WEST, 'r', label='Before GV Installation', linewidth=2)
    plt.plot(x, max_P_postGV_WEST[:], 'b', label='After GV Installation', linewidth=2)
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)
    # Set Y-Axis range and ticks
    plt.ylim(0, 100)  # Set y-axis limits from 0 to 100
    plt.yticks(range(0, 121, 10)) 
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.ylabel('Pressure (m)')
    plt.title('Pressure Distribution within Western Network')
    plt.legend(loc='upper left') 
plot_pressure_dif_gv_WEST()

# =============================================================================
# GVS AND OASIS ANALYSIS: PLOTS FOR GVS ENERGETIC BALANCE IN EACH REGIONS
# =============================================================================
def plot_gvs_energy_bal(): 
    # Calculate y-axis limits 
    EAST_min = min(min(final_consumption_GV_EAST), min(final_recovery_GV_EAST))
    EAST_max = max(max(final_consumption_GV_EAST), max(final_recovery_GV_EAST))
    WEST_min = min(min(final_consumption_GV_WEST), min(final_recovery_GV_WEST))
    WEST_max = max(max(final_consumption_GV_WEST), max(final_recovery_GV_WEST))
    y_min = min(EAST_min, WEST_min)
    y_max = max(EAST_max, WEST_max)
    y_buffer = (y_max - y_min) * 0.1  # Add a 10% buffer for better visualization

    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Create the high-resolution figure for EAST region
    plt.figure(figsize=(8, 6), dpi=300)
    # Plot the EAST Region
    plt.subplot(1, 2, 1)  # Create first subplot occupying 1 row, 2 columns, position 1
    plt.plot(x, final_consumption_GV_EAST, 'r', label='Consumption', linewidth=2)
    plt.plot(x, final_recovery_GV_EAST, 'b', label='Recovery', linewidth=2)
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)  # Adjust rotation if needed
    # Set Y-Axis range and ticks
    plt.ylim(y_min - y_buffer, y_max + y_buffer)
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.ylabel('Cumulative Energy [Wh]')
    plt.title('Eastern Network')
    plt.legend(loc='upper left')
    
    # Create the high-resolution figure for WEST region
    plt.subplot(1, 2, 2)  # Create second subplot occupying 1 row, 2 columns, position 2
    # Plot the WEST Region
    plt.plot(x, final_consumption_GV_WEST, 'r', label='Consumption', linewidth=2)
    plt.plot(x, final_recovery_GV_WEST, 'b', label='Recovery', linewidth=2)
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)  # Adjust rotation if needed
    # Set Y-Axis range and ticks
    plt.ylim(y_min - y_buffer, y_max + y_buffer)
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.ylabel('Cumulative Energy [Wh]')
    plt.title('Western Network')  # Change to 'Central Network' if applicable
    plt.legend(loc='upper left')
    
    # Add main title for the entire figure
    plt.suptitle('Green Valve Energetic Balance', fontsize=14)  # Adjust font size as desired
    # Adjust layout (optional)
    plt.tight_layout()
plot_gvs_energy_bal()

# =============================================================================
# GVS AND OASIS ANALYSIS: PLOTS FOR OASIS ENERGETIC BALANCE IN EACH REGIONS
# =============================================================================
# Define OASIS energetic balances in each region
def oasis_energy_bal_EAST(): 
    global cum_rec_0_50_EAST, cum_rec_50_100_EAST, cum_rec_100_150_EAST, cum_rec_150_200_EAST, cum_rec_200_250_EAST, cum_rec_250_300_EAST, cum_max_consumption_EAST 
    rec_0_50_EAST       = np.zeros(17520, dtype=float)
    rec_50_100_EAST     = np.zeros(17520, dtype=float)
    rec_100_150_EAST    = np.zeros(17520, dtype=float)
    rec_150_200_EAST    = np.zeros(17520, dtype=float)
    rec_200_250_EAST    = np.zeros(17520, dtype=float)
    rec_250_300_EAST    = np.zeros(17520, dtype=float)

    for i in range(num_columns):
        print(i)
        rec_0_50_EAST[i]     = np.nanmean(Recovery_less_than_50_EAST[:, i])
        rec_50_100_EAST[i]   = np.nanmean(Recovery_50_100_EAST[:, i])
        rec_100_150_EAST[i]  = np.nanmean(Recovery_100_150_EAST[:, i])
        rec_150_200_EAST[i]  = np.nanmean(Recovery_150_200_EAST[:, i])
        rec_200_250_EAST[i]  = np.nanmean(Recovery_200_250_EAST[:, i])
        rec_250_300_EAST[i]  = np.nanmean(Recovery_more_than_250_EAST[:,i])
    
    cum_rec_0_50_EAST    = np.cumsum(rec_0_50_EAST)
    cum_rec_50_100_EAST  = np.cumsum(rec_50_100_EAST)
    cum_rec_100_150_EAST = np.cumsum(rec_100_150_EAST)
    cum_rec_150_200_EAST = np.cumsum(rec_150_200_EAST)
    cum_rec_200_250_EAST = np.cumsum(rec_200_250_EAST)
    cum_rec_250_300_EAST = np.cumsum(rec_250_300_EAST)
    
    max_consumption_EAST       = np.zeros(17520)  
    max_consumption_nodes_EAST = np.sum(consumption_EAST, axis=1)
    index_max                  = np.argmax(max_consumption_nodes_EAST)
    max_consumption_EAST       = consumption_EAST[index_max, :]
    cum_max_consumption_EAST   = np.cumsum(max_consumption_EAST)
oasis_energy_bal_EAST()

def plot_oasis_energy_bal_EAST(): 
    # Create the high-resolution figure for EAST region
    plt.figure(figsize=(8, 6), dpi=300)
    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Plot the EAST Region
    plt.plot(x, cum_rec_0_50_EAST, color=(0, 0.4470, 0.7410), linestyle='-', linewidth=1.5, label='Operating Hours < 50')
    plt.plot(x, cum_rec_50_100_EAST, color=(0.8500, 0.3250, 0.0980), linestyle='-', linewidth=1.5, label='Operating Hours between 50-100')
    plt.plot(x, cum_rec_100_150_EAST, color=(0.9290, 0.6940, 0.1250), linestyle='-', linewidth=1.5, label='Operating Hours between 100-150')
    plt.plot(x, cum_rec_150_200_EAST, color=(0.4940, 0.1840, 0.5560), linestyle='-', linewidth=1.5, label='Operating Hours between 150-200')
    plt.plot(x, cum_rec_200_250_EAST, color=(0.4660, 0.6740, 0.1880), linestyle='-', linewidth=1.5, label='Operating Hours between 200-250')
    plt.plot(x, cum_rec_250_300_EAST, color=(0.3010, 0.7450, 0.9330), linestyle='-', linewidth=1.5, label='Operating Hours between 250-300')
    plt.plot(x, cum_max_consumption_EAST, color='red', linestyle='--', linewidth=1.5, label='Maximum Node Consumption')
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)  # Adjust rotation if needed
    # Set Y-Axis range and ticks
    plt.ylim(0, 35000)  # Set y-axis limits (0 to 35000)
    plt.yticks(range(0, 35001, 5000))  # Set y-axis ticks with increment of 5000
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.legend(loc='upper left') 
    plt.title('OAS Energetic Balance within Eastern Network')
    plt.ylabel('Cumulated Energy [Wh]')
    plt.grid(True)
plot_oasis_energy_bal_EAST()

def oasis_energy_bal_WEST(): 
    global cum_rec_0_50_WEST, cum_rec_50_100_WEST, cum_rec_100_150_WEST, cum_rec_150_200_WEST, cum_rec_200_250_WEST, cum_rec_250_300_WEST, cum_max_consumption_WEST 
    rec_0_50_WEST       = np.zeros(17520, dtype=float)
    rec_50_100_WEST     = np.zeros(17520, dtype=float)
    rec_100_150_WEST    = np.zeros(17520, dtype=float)
    rec_150_200_WEST    = np.zeros(17520, dtype=float)
    rec_200_250_WEST    = np.zeros(17520, dtype=float)
    rec_250_300_WEST    = np.zeros(17520, dtype=float)

    for i in range(num_columns):
        print(i)
        rec_0_50_WEST[i]     = np.nanmean(Recovery_less_than_50_WEST[:, i])
        rec_50_100_WEST[i]   = np.nanmean(Recovery_50_100_WEST[:, i])
        rec_100_150_WEST[i]  = np.nanmean(Recovery_100_150_WEST[:, i])
        rec_150_200_WEST[i]  = np.nanmean(Recovery_150_200_WEST[:, i])
        rec_200_250_WEST[i]  = np.nanmean(Recovery_200_250_WEST[:, i])
        rec_250_300_WEST[i]  = np.nanmean(Recovery_more_than_250_WEST[:,i])
    
    cum_rec_0_50_WEST    = np.cumsum(rec_0_50_WEST)
    cum_rec_50_100_WEST  = np.cumsum(rec_50_100_WEST)
    cum_rec_100_150_WEST = np.cumsum(rec_100_150_WEST)
    cum_rec_150_200_WEST = np.cumsum(rec_150_200_WEST)
    cum_rec_200_250_WEST = np.cumsum(rec_200_250_WEST)
    cum_rec_250_300_WEST = np.cumsum(rec_250_300_WEST)
    
    max_consumption_WEST       = np.zeros(17520)  
    max_consumption_nodes_WEST = np.sum(consumption_WEST, axis=1)
    index_max                  = np.argmax(max_consumption_nodes_WEST)
    max_consumption_WEST       = consumption_WEST[index_max, :]
    cum_max_consumption_WEST   = np.cumsum(max_consumption_WEST)
oasis_energy_bal_WEST()

def plot_oasis_energy_bal_WEST(): 
    # Create the high-resolution figure for WEST region
    plt.figure(figsize=(8, 6), dpi=300)
    # Define the X-Axis range as the month
    x = list(range(0, 17520))  # Create list from 1 to 17520
    custom_ticks = [720, 2160, 3600, 5040, 6480, 7920, 9360, 10800, 12240, 13680, 15120, 16560]
    custom_labels = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    # Plot the WEST Region
    plt.plot(x, cum_rec_0_50_WEST, color=(0, 0.4470, 0.7410), linestyle='-', linewidth=1.5, label='Operating Hours < 50')
    plt.plot(x, cum_rec_50_100_WEST, color=(0.8500, 0.3250, 0.0980), linestyle='-', linewidth=1.5, label='Operating Hours between 50-100')
    plt.plot(x, cum_rec_100_150_WEST, color=(0.9290, 0.6940, 0.1250), linestyle='-', linewidth=1.5, label='Operating Hours between 100-150')
    plt.plot(x, cum_rec_150_200_WEST, color=(0.4940, 0.1840, 0.5560), linestyle='-', linewidth=1.5, label='Operating Hours between 150-200')
    plt.plot(x, cum_rec_200_250_WEST, color=(0.4660, 0.6740, 0.1880), linestyle='-', linewidth=1.5, label='Operating Hours between 200-250')
    plt.plot(x, cum_rec_250_300_WEST, color=(0.3010, 0.7450, 0.9330), linestyle='-', linewidth=1.5, label='Operating Hours between 250-300')
    plt.plot(x, cum_max_consumption_WEST, color='red', linestyle='--', linewidth=1.5, label='Maximum Node Consumption')
    # Set X-Axis range and ticks
    plt.xticks(custom_ticks, custom_labels, rotation=90)  # Adjust rotation if needed
    # Set Y-Axis range and ticks
    plt.ylim(0, 35000)  # Set y-axis limits (0 to 35000)
    plt.yticks(range(0, 35001, 5000))  # Set y-axis ticks with increment of 5000
    # Set figure information remaining customizations (e.g., labels, title, legend)
    plt.legend(loc='upper left') 
    plt.title('OAS Energetic Balance within Western Network')
    plt.ylabel('Cumulated Energy [Wh]')
    plt.grid(True)
plot_oasis_energy_bal_WEST()

# =============================================================================
# END PART - CALCULATE PROCESSING TIME
# =============================================================================
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time, "seconds")