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