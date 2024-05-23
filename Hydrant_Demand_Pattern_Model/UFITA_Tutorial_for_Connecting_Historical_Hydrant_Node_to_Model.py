# ====================================================================================
# UFITA Irrigation Networks - Tutorial for Connecting Historical Hydrant Node to Model
# ====================================================================================

# IMPORT PYTHON LIBRARIES
import os 
import pandas as pd

# CHANGE THE WORKING DIRECTORY 
os.chdir('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/') 

# IMPORT HYDRANT DEMAND AND STATUS FILE (Data 2007-10-05 is used as an example)
hydrant_demand = pd.read_excel('Hydrant_Historical_Operation_Excel/hydrant_demand_051007.xlsx', sheet_name = 'Sheet1') 
hydrant_demand = hydrant_demand.set_index('Time')
hydrant_status = pd.read_excel('Hydrant_Historical_Operation_Excel/hydrant_status_051007.xlsx', sheet_name = 'Sheet1') 
hydrant_status = hydrant_status.set_index(hydrant_demand.index)

# IMPORT HYDRANT REFERENCE
hydrant_reference = pd.read_excel('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Data Cleansing & PreProcessing/Data Cleansing - UFITA - Historical Hydrant Usage 2007.xlsx',
                                sheet_name = 'DC - Hydrant (Model+Historical)')
hydrant_reference.columns = hydrant_reference.iloc[3]
hydrant_reference = hydrant_reference.iloc[4:]
hydrant_reference = hydrant_reference.iloc[:, 2:4] 

# CREATE MAPPING DICTIONARY
mapping_dict = dict(zip(hydrant_reference['HISTORICAL RECORD'], hydrant_reference['HYDRAULIC MODEL']))

# RENAME COLUMN USING REFERENCE
hydrant_demand_model = hydrant_demand.rename(columns=mapping_dict)
hydrant_status_model = hydrant_status.rename(columns=mapping_dict)

# =============================================================================
# UFITA Irrigation Networks - Tutorial for Assign Demand at Nodes 
# =============================================================================

'''
This tutorial guides you through overriding specific demand patterns for hydrant 
nodes using the WNTR Python library. We will leverage a DataFrame representing 
daily demand data.

The DataFrame structure is as follows:
A. Index: 
   Named "Time", containing timestamps or time steps representing the simulation 
   period (start to end).

B. Columns: 
    Each column represents a hydrant/node ID based on your naming convention.
    Values: Each cell contains the demand value for a specific time step and 
    corresponding hydrant/node.This DataFrame will be used to replace the 
    original demand values defined in your EPANET model.

'''

# =============================================================================
# STEP I. Import and Run the EPANET Model with the Original Dataset
# =============================================================================
# IMPORT PYTHON LIBRARIES
import os 
import pandas as pd
import wntr 

# CHANGE THE WORKING DIRECTORY 
os.chdir('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/EPANET/') 

# LOAD THE WATER NETWORK MODEL 
inp_file = 'Rete_INPUTtag_1_CENTER+EAST_B.inp'


# CREATE AN EPANET SIMULATOR OBJECT 
wn = wntr.network.WaterNetworkModel(inp_file)                                  # WNTR model
sim = wntr.sim.EpanetSimulator(wn)

## SET THE HYDRAULIC PARAMETER
### SET THE TIMESTEP (dt)
dt = 1800                                                                      # Timestep (dt) in seconds
wn.options.time.hydraulic_timestep = dt                                        # Timestep (dt) settings in WNTR
### SET THE DURATION OF THE MODEL 
wn.options.time.duration = 47 * dt                                              # End time of the model 
wn.options.time.report_timestep = dt                                           # End report of the model
### SET THE INITIAL AND BOUNDARY CONDITIONS
reservoir = wn.get_node('VASCA_GRANDE')                                        # Set the reservoir node in the WDN
reservoir.base_head = 465                                                      # Set the water level in the tank 
### SET THE DEMAND PATERN
### SET THE HYDRAULIC CALCULATION APPROACH (DD or PD)
wn.options.hydraulic.demand_model = 'DD'                                       # Set for Demand Driven approach

# RUN THE SIMULATION
results = sim.run_sim()                   # Epanet simulation with the original demand data

# CHECK DEMAND AT NODES 
demand_at_node = results.node['demand']   # Demand at nodes with the original demand data

# =============================================================================
# STEP II. Costumize Demand Pattern for Particular Hydrant Node
# =============================================================================
# CREATE A DATAFRAME FOR DEMAND AT NODES 
time_index = pd.RangeIndex(start=0, stop=86401, step=1800)  # Identifying daily time index in 24 hours with 3600 sec step
df = pd.DataFrame({'NODOB': 5, 'DERB.13' : 2}, index=time_index)              # Fil the costumize demand patern for particular hydrant node

# ASSIGN DATAFRAME AS A DEMAND AT NODES
wn.assign_demand(hydrant_status_model)

# RUN THE SIMULATION
results2 = sim.run_sim()                   # Epanet simulation with the costum demand data

# CHECK DEMAND AT NODES 
demand_at_node2 = results2.node['demand']  # Demand at nodes with the costum demand data
