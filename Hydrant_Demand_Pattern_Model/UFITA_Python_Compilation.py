# =============================================================================
# UFITA IRRIGATION NETWORKS - PYTHON COMPILATION 
# =============================================================================
'''
- PART I.   DATA CLEANSING 
- PART II  .DATA PRE-PROCESSING
- PART III  DATA PROCESSING
- PART IV. EXPORT HYDRAULIC SIMULATION RESULTS
- PART V   DATA VISUALIZATION
'''

# Import Python Libraries
import glob
import numpy as np
import os 
import pandas as pd
import wntr 

# =============================================================================
# PART I. DATA CLEANSING 
# =============================================================================

# I. 1. Change Working Directory
os.chdir('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Hydrant_Historical_Operation_Excel/') 

# I. 2. Import Historical Hydrant Usage in 2007
data_2007_CEW = pd.read_excel('Esercizio_irriguo_anno_2007.xlsx', sheet_name = '2007_CEW_Raw') # Dataset 2007 wtih Central, East and West Region
data_2007_CE  = pd.read_excel('Esercizio_irriguo_anno_2007.xlsx', sheet_name = '2007_CE_Raw')  # Dataset 2007 wtih Central and East Region

# I. 3. Slice Historical Hydrant Usage Based on Zone and Month
id_hydrant_2007_CEW = data_2007_CEW['Idrante'].drop_duplicates() # ID of active hydrant in dataset 2007 CEW
id_hydrant_2007_CE  = data_2007_CE['Idrante'].drop_duplicates()  # ID of active hydrant in dataset 2007 CE
id_hydrant_2007_W   = id_hydrant_2007_CEW[~id_hydrant_2007_CEW.isin(id_hydrant_2007_CE)] # ID of active hydrant in dataset 2007 W
data_2007_CE['month'] = pd.to_datetime(data_2007_CE['Inizio']).dt.month # Extract the month as a numerical value (1-12)
monthly_data_2007_CE  = [data_2007_CE[data_2007_CE['month'] == month] for month in data_2007_CE['month'].unique()]
aug_data_2007_CE = monthly_data_2007_CE[0] # Historical data in August 2007
jun_data_2007_CE = monthly_data_2007_CE[1] # Historical data in June 2007
jul_data_2007_CE = monthly_data_2007_CE[2] # Historical data in July 2007
may_data_2007_CE = monthly_data_2007_CE[3] # Historical data in May 2007
oct_data_2007_CE = monthly_data_2007_CE[4] # Historical data in October 2007
sep_data_2007_CE = monthly_data_2007_CE[5] # Historical data in September 2007

# I. 4. Analyzing Dominant Hydrant in a Month
def dp_aug_2007(): 
    global summary_aug_2007_data 
    'This def function is used to do data preprocessing on selected monthly hydrant historical data.'
    'It produces a data frame variable which contains a summary of each hydrant usage within a month.'
    # Part 1 - 
    'This part lists all hydrants operating this month'
    id_hydrant_aug_2007_CE = aug_data_2007_CE['Idrante'].drop_duplicates().tolist() # ID of active hydrant in during August 2007 CE
    # Part 2 - The sum of Hydrant Discharge  
    'This part analyzes the total sum of hydrant discharge'
    monthly_historical_data = aug_data_2007_CE
    monthy_hydrant_name     = id_hydrant_aug_2007_CE
    
    temp_result = {x: monthly_historical_data[monthly_historical_data['Idrante'] == x]['Q'].sum() for x in monthy_hydrant_name}
    temp_result_df = pd.DataFrame.from_dict(temp_result, orient='index', columns=['Q_Total'])
    temp_result_df.reset_index(inplace=True)
    temp_result_df.rename(columns={'index': 'Idrante'}, inplace=True)
    # Part 3 - The hydrant summary
    'This part merges 2 dataframe, one is a matemathical summary, while the other is a sum of hydrant discharge'
    summary_monthly_data  = monthly_historical_data.groupby('Idrante')['Q'].describe()
    summary_aug_2007_data = temp_result_df.merge(summary_monthly_data, on='Idrante', how='inner')
def dp_jun_2007(): 
    global summary_jun_2007_data 
    'This def function is used to do data preprocessing on selected monthly hydrant historical data.'
    'It produces a data frame variable which contains a summary of each hydrant usage within a month.'
    # Part 1 - 
    'This part lists all hydrants operating this month'
    id_hydrant_jun_2007_CE = jun_data_2007_CE['Idrante'].drop_duplicates().tolist() # ID of active hydrant in during August 2007 CE
    # Part 2 - The sum of Hydrant Discharge  
    'This part analyzes the total sum of hydrant discharge'
    monthly_historical_data = jun_data_2007_CE
    monthy_hydrant_name     = id_hydrant_jun_2007_CE
    
    temp_result = {x: monthly_historical_data[monthly_historical_data['Idrante'] == x]['Q'].sum() for x in monthy_hydrant_name}
    temp_result_df = pd.DataFrame.from_dict(temp_result, orient='index', columns=['Q_Total'])
    temp_result_df.reset_index(inplace=True)
    temp_result_df.rename(columns={'index': 'Idrante'}, inplace=True)
    # Part 3 - The hydrant summary
    'This part merges 2 dataframe, one is a matemathical summary, while the other is a sum of hydrant discharge'
    summary_monthly_data  = monthly_historical_data.groupby('Idrante')['Q'].describe()
    summary_jun_2007_data = temp_result_df.merge(summary_monthly_data, on='Idrante', how='inner')
def dp_jul_2007(): 
    global summary_jul_2007_data 
    'This def function is used to do data preprocessing on selected monthly hydrant historical data.'
    'It produces a data frame variable which contains a summary of each hydrant usage within a month.'
    # Part 1 - 
    'This part lists all hydrants operating this month'
    id_hydrant_jul_2007_CE = jul_data_2007_CE['Idrante'].drop_duplicates().tolist() # ID of active hydrant in during August 2007 CE
    # Part 2 - The sum of Hydrant Discharge  
    'This part analyzes the total sum of hydrant discharge'
    monthly_historical_data = jul_data_2007_CE
    monthy_hydrant_name     = id_hydrant_jul_2007_CE
    
    temp_result = {x: monthly_historical_data[monthly_historical_data['Idrante'] == x]['Q'].sum() for x in monthy_hydrant_name}
    temp_result_df = pd.DataFrame.from_dict(temp_result, orient='index', columns=['Q_Total'])
    temp_result_df.reset_index(inplace=True)
    temp_result_df.rename(columns={'index': 'Idrante'}, inplace=True)
    # Part 3 - The hydrant summary
    'This part merges 2 dataframe, one is a matemathical summary, while the other is a sum of hydrant discharge'
    summary_monthly_data  = monthly_historical_data.groupby('Idrante')['Q'].describe()
    summary_jul_2007_data = temp_result_df.merge(summary_monthly_data, on='Idrante', how='inner')
def dp_may_2007(): 
    global summary_may_2007_data 
    'This def function is used to do data preprocessing on selected monthly hydrant historical data.'
    'It produces a data frame variable which contains a summary of each hydrant usage within a month.'
    # Part 1 - 
    'This part lists all hydrants operating this month'
    id_hydrant_may_2007_CE = may_data_2007_CE['Idrante'].drop_duplicates().tolist() # ID of active hydrant in during August 2007 CE
    # Part 2 - The sum of Hydrant Discharge  
    'This part analyzes the total sum of hydrant discharge'
    monthly_historical_data = may_data_2007_CE
    monthy_hydrant_name     = id_hydrant_may_2007_CE
    
    temp_result = {x: monthly_historical_data[monthly_historical_data['Idrante'] == x]['Q'].sum() for x in monthy_hydrant_name}
    temp_result_df = pd.DataFrame.from_dict(temp_result, orient='index', columns=['Q_Total'])
    temp_result_df.reset_index(inplace=True)
    temp_result_df.rename(columns={'index': 'Idrante'}, inplace=True)
    # Part 3 - The hydrant summary
    'This part merges 2 dataframe, one is a matemathical summary, while the other is a sum of hydrant discharge'
    summary_monthly_data  = monthly_historical_data.groupby('Idrante')['Q'].describe()
    summary_may_2007_data = temp_result_df.merge(summary_monthly_data, on='Idrante', how='inner')
def dp_oct_2007(): 
    global summary_oct_2007_data 
    'This def function is used to do data preprocessing on selected monthly hydrant historical data.'
    'It produces a data frame variable which contains a summary of each hydrant usage within a month.'
    # Part 1 - 
    'This part lists all hydrants operating this month'
    id_hydrant_oct_2007_CE = oct_data_2007_CE['Idrante'].drop_duplicates().tolist() # ID of active hydrant in during August 2007 CE
    # Part 2 - The sum of Hydrant Discharge  
    'This part analyzes the total sum of hydrant discharge'
    monthly_historical_data = oct_data_2007_CE
    monthy_hydrant_name     = id_hydrant_oct_2007_CE
    
    temp_result = {x: monthly_historical_data[monthly_historical_data['Idrante'] == x]['Q'].sum() for x in monthy_hydrant_name}
    temp_result_df = pd.DataFrame.from_dict(temp_result, orient='index', columns=['Q_Total'])
    temp_result_df.reset_index(inplace=True)
    temp_result_df.rename(columns={'index': 'Idrante'}, inplace=True)
    # Part 3 - The hydrant summary
    'This part merges 2 dataframe, one is a matemathical summary, while the other is a sum of hydrant discharge'
    summary_monthly_data  = monthly_historical_data.groupby('Idrante')['Q'].describe()
    summary_oct_2007_data = temp_result_df.merge(summary_monthly_data, on='Idrante', how='inner')
def dp_sep_2007(): 
    global summary_sep_2007_data 
    'This def function is used to do data preprocessing on selected monthly hydrant historical data.'
    'It produces a data frame variable which contains a summary of each hydrant usage within a month.'
    # Part 1 - 
    'This part lists all hydrants operating this month'
    id_hydrant_sep_2007_CE = sep_data_2007_CE['Idrante'].drop_duplicates().tolist() # ID of active hydrant in during August 2007 CE
    # Part 2 - The sum of Hydrant Discharge  
    'This part analyzes the total sum of hydrant discharge'
    monthly_historical_data = sep_data_2007_CE
    monthy_hydrant_name     = id_hydrant_sep_2007_CE
    
    temp_result = {x: monthly_historical_data[monthly_historical_data['Idrante'] == x]['Q'].sum() for x in monthy_hydrant_name}
    temp_result_df = pd.DataFrame.from_dict(temp_result, orient='index', columns=['Q_Total'])
    temp_result_df.reset_index(inplace=True)
    temp_result_df.rename(columns={'index': 'Idrante'}, inplace=True)
    # Part 3 - The hydrant summary
    'This part merges 2 dataframe, one is a matemathical summary, while the other is a sum of hydrant discharge'
    summary_monthly_data  = monthly_historical_data.groupby('Idrante')['Q'].describe()
    summary_sep_2007_data = temp_result_df.merge(summary_monthly_data, on='Idrante', how='inner')
dp_aug_2007() 
dp_jun_2007()
dp_jul_2007()
dp_may_2007()
dp_oct_2007()
dp_sep_2007()

# I. 5. Analyzing Hydrants Daily Usage
Hydrant_Operational_Date  = '2007-05-01'         # Input date of interest
Hydrant_Operational_Month =  may_data_2007_CE    # Input month of interest
def daily_data(month_df, date): 
    global spesific_day_data
    month_df['date'] = pd.to_datetime(month_df['Inizio']).dt.strftime('%Y-%m-%d')
    month_df['time'] = pd.to_datetime(month_df['Inizio']).dt.time
    daily_data = month_df.groupby('date')
    spesific_day_data = daily_data.get_group(date)
    columns_to_drop = ['Column1', 'Derivazione', 'AcquaFix', 'Superficie irrigua', 'Coltura', 
                       'Sistema Irriguo', 'Consumo', 'month', 'Fine', 'Q', 'time', 'date']
    spesific_day_data = spesific_day_data.drop(columns_to_drop, axis=1)
    spesific_day_data = spesific_day_data.set_index('Idrante')
daily_data(Hydrant_Operational_Month, Hydrant_Operational_Date)

# =============================================================================
# PART II - DATA PRE-PROCESSING
# =============================================================================

# II. 1. Create a Def Function for Hydrant Demand
def create_hydrant_demand(df):
    """
    This function takes a pandas dataframe containing timestamps and durations
    of hydrant operations and creates a new dataframe `BIN_Hydrant` with time bins
    and hydrant status.

    Args:
        df (pandas.DataFrame): Dataframe containing historical hydrant usage data.

    Returns:
        pandas.DataFrame: A new dataframe `BIN_Hydrant` with time bins and hydrant status.
    """

    # Create time index from 0 to 86400 with 1800 seconds increment
    time_index = pd.RangeIndex(start=0, stop=84601, step=1800)

    # Initialize dictionary to store hydrant statuses for each hydrant
    hydrant_demand_dict = {}

    # Iterate through each hydrant usage data
    for idx, row in df.iterrows():
        timestamp = pd.to_datetime(row['Inizio'], format='%H:%M:%S').time()  # Extract time from timestamp
        duration = row['Seconds interval']

        # Set hydrant status to 1 within the usage time window
        start_bin = timestamp.hour * 3600 + timestamp.minute * 60  # Convert time to seconds
        end_bin = start_bin + duration

        if idx not in hydrant_demand_dict:
            hydrant_demand_dict[idx] = pd.Series(index=time_index, dtype=float)

        hydrant_demand_dict[idx].loc[start_bin:end_bin] = 0.005  # 5 L/s

    # Combine hydrant demand series into a single dataframe
    hydrant_demand = pd.DataFrame(hydrant_demand_dict)

    # Fill all remaining NaN values with 0 (not in use)
    hydrant_demand = hydrant_demand.fillna(0)

    return hydrant_demand
hydrant_demand = create_hydrant_demand(spesific_day_data.copy())

# II. 2. Delete the Absent Nodes
absent_node_list = ["027bis","263tris","B034","B272bis","B297bis","B300","B302"
                    , "B303","B401","B402","B403","B404","B60bis","B62bis"]

node_id_to_delete = [col for col in hydrant_demand.columns if col in absent_node_list]

if node_id_to_delete:
    hydrant_demand = hydrant_demand.drop(node_id_to_delete, axis=1)
else:
    pass

# II. 3. Create Hydrant Nomenclature Reference
hydrant_reference = pd.read_excel('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Data Cleansing & PreProcessing/Data Cleansing - UFITA - Historical Hydrant Usage 2007.xlsx',
                                sheet_name = 'DC - Hydrant (Model+Historical)')
hydrant_reference.columns = hydrant_reference.iloc[3]
hydrant_reference = hydrant_reference.iloc[4:]
hydrant_reference = hydrant_reference.iloc[:, 2:4] 

# II. 4. Adjust Hydrant Nomenclature in the Historical Data and Model 
mapping_dict = dict(zip(hydrant_reference['HISTORICAL RECORD'], hydrant_reference['HYDRAULIC MODEL']))
hydrant_demand_temp = hydrant_demand.rename(columns=mapping_dict)

# =============================================================================
# PART III - DATA PROCESSING
# =============================================================================

# III. 1. Change Working Directory
os.chdir('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/EPANET/') 

# III. 2 Load EPANET Model
inp_file = 'Rete_INPUTtag_1_CENTER+EAST_B.inp'

# III. 3. Create EPANET Simulator Object
wn = wntr.network.WaterNetworkModel(inp_file)                                  # WNTR model
sim = wntr.sim.EpanetSimulator(wn)

# III. 4. Set Hydraulic Parameter
dt = 1800                                                                      # Timestep (dt) in seconds
wn.options.time.hydraulic_timestep = dt                                        # Timestep (dt) settings in WNTR
wn.options.time.duration = 47 * dt                                              # End time of the model 
wn.options.time.report_timestep = dt                                           # End report of the model
reservoir = wn.get_node('VASCA_GRANDE')                                        # Set the reservoir node in the WDN
reservoir.base_head = 465                                                      # Set the water level in the tank 
wn.options.hydraulic.demand_model = 'DD'                                       # Set for Demand Driven approach

# III. 5. Run the Hydraulic Model
results_base = sim.run_sim()

# III. 6. Records the Hydraulic Simmulation Result 
demand_base_model   = results_base.node['demand']   # Demand at nodes with the original demand data
pressure_base_model = results_base.node['pressure'] # Pressure at nodes with the original demand data

# III. 7. Apply the Hydrant Demand Pattern to the node
wn.assign_demand(hydrant_demand_temp)

# III. 8. Run the Hydraulic Model with New Demand Pattern
results_hydrant = sim.run_sim()                   # Epanet simulation with the costum demand data

# III. 9. Records the Hydraulic Simmulation Result with New Demand Pattern
demand_hydrant_model   = results_hydrant.node['demand']   # Demand at nodes with the original demand data
pressure_hydrant_model = results_hydrant.node['pressure'] # Pressure at nodes with the original demand data

# III. 10. Create Data Frame to Represent Hydrant Status
status_hydrant_model = demand_hydrant_model.copy()
def hydrant_status_def(x):
    if x > 0 :
        return 1
    else:
        return 0
status_hydrant_model  = status_hydrant_model.applymap(hydrant_status_def) # Hydrant opening/closing status (1/0)

# III. 11. Create a Series of Active Hydrants ID
day_index = spesific_day_data.reset_index()
id_hydrant = day_index['Idrante'].drop_duplicates().to_frame() # ID of active hydrant in during August 2007 CE
id_hydrant2 = id_hydrant.rename(columns=mapping_dict)

# III. 12. Analyzing the Amount of Water Withdrawn from the System
def water_withdrawn(): 
    global water_withdrawn_hydrant_model
    'This def function is used to do analyze the amount of water withdran from the system.'
    'The mathematical operation that being used is the sum of duration in one hydrant times the dischrage.'
    'The discharge is set 0.005 m3/s'
    # Part 1 - 
    temp_daily_hydrant = day_index['Idrante'].drop_duplicates().tolist() # ID of active hydrant in during August 2007 CE
    # Part 2 - The sum of Hydrant Discharge  
    'This part analyzes the total sum of hydrant duration'
    temp_result = {x: day_index[day_index['Idrante'] == x]['Seconds interval'].sum() for x in temp_daily_hydrant}
    temp_result_df = pd.DataFrame.from_dict(temp_result, orient='index', columns=['Duration(s)'])
    temp_result_df.reset_index(inplace=True)
    temp_result_df.rename(columns={'index': 'Idrante'}, inplace=True)
    # Part 3 - The hydrant summary
    'This part merges 2 dataframe, one is a matemathical summary, while the other is a sum of hydrant discharge'
    summary_daily_data            = day_index.groupby('Idrante')['Seconds interval'].describe()
    water_withdrawn_hydrant_model_temp = temp_result_df.merge(summary_daily_data, on='Idrante', how='inner')
    water_withdrawn_hydrant_model_temp = water_withdrawn_hydrant_model_temp.iloc[:, :2]
    water_withdrawn_hydrant_model_temp['V(m3)'] = water_withdrawn_hydrant_model_temp['Duration(s)'] * 0.005
    # Part 4 - Adjusting the hydrant nomenclature
    mapping_dict = dict(zip(hydrant_reference['HISTORICAL RECORD'], hydrant_reference['HYDRAULIC MODEL']))
    water_withdrawn_hydrant_model_temp['Idrante'] = water_withdrawn_hydrant_model_temp['Idrante'].map(mapping_dict)
    water_withdrawn_hydrant_model = water_withdrawn_hydrant_model_temp.dropna()
    water_withdrawn_hydrant_model = water_withdrawn_hydrant_model.reset_index(drop=True)
        
water_withdrawn()
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
Excel_Writer()

# =============================================================================
# PART V   DATA VISUALIZATION
# =============================================================================
