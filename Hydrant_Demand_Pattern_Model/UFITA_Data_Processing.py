# Import Python Libraries
import os 
import pandas as pd
import wntr 

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