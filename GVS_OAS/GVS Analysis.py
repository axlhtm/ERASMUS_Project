# =============================================================================
# GVS ANALYSIS
# =============================================================================

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