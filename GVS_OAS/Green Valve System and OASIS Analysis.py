# =============================================================================
# GREEN VALVE SYSTEM
# =============================================================================

# IMPORT PYTHON LIBRARIES 
import numpy as np 

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
OAS_size    = np.ones(500, dtype=int) * 2  # Initialize with 2 for all time steps
days_per_month  = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] # No. of days each months 
num_mezzore     = [x * 48 for x in days_per_month] # No of half hours each months

# PART II - IMPORT INPUT DATA FROM HYDRAULIC SIMULATION

# PART III - IMPORT EASTERN NETWORK NODE NAMES
january     = np.zeros((num_nodes, num_mezzore[0]))
february    = np.zeros((num_nodes, num_mezzore[1]))
march       = np.zeros((num_nodes, num_mezzore[2]))
april       = np.zeros((num_nodes, num_mezzore[3]))
may         = np.zeros((num_nodes, num_mezzore[4]))
june        = np.zeros((num_nodes, num_mezzore[5]))
july        = np.zeros((num_nodes, num_mezzore[6]))
august      = np.zeros((num_nodes, num_mezzore[7]))
september   = np.zeros((num_nodes, num_mezzore[8]))
october     = np.zeros((num_nodes, num_mezzore[9]))
november    = np.zeros((num_nodes, num_mezzore[10]))
december    = np.zeros((num_nodes, num_mezzore[11]))
months_names = ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december")


