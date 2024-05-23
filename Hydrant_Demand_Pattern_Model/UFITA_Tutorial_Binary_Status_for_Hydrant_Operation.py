# =============================================================================
# UFITA Irrigation Networks - Tutorial Binary Status for Hydrant Operational
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
# STEP I. Import Python Libraries and Create Data Frame for Hydrant Usage
# =============================================================================
# IMPORT PYTHON LIBRARIES
import pandas as pd

# CREATE DATA FRAME THAT REPRESENTS HYDRANT USAGE
df = pd.DataFrame({'timestamp': ['06:30:00', '12:10:00', '21:45:00'], 'duration': [7200, 3600, 5000]}, 
                  index=['HydrantA', 'HydrantB', 'HydrantC'])

# =============================================================================
# STEP II. Conversion to Binary Status with Incremental Timestep in Seconds
# =============================================================================
# CREATE DEF FUNCTION TO ITERATE THE DATA IN DF

def create_hydrant_usage_bins(df):
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
  time_index = pd.RangeIndex(start=0, stop=86401, step=900)

  # Initialize new dataframe with all hydrant statuses as NaN (missing values)
  hydrant_status = pd.DataFrame(index=time_index, columns=df.index)

  # Iterate through each hydrant usage data
  for idx, row in df.iterrows():
    timestamp = pd.to_datetime(row['timestamp'], format='%H:%M:%S').time()  # Extract time from timestamp
    duration = row['duration']

    # Set hydrant status to 1 within the usage time window
    start_bin = timestamp.hour * 3600 + timestamp.minute * 60  # Convert time to seconds
    end_bin = start_bin + duration
    hydrant_status.loc[start_bin:end_bin, idx] = 1

  # Fill all remaining NaN values with 0 (not in use)
  hydrant_status = hydrant_status.fillna(0)

  return hydrant_status

hydrant_status = create_hydrant_usage_bins(df.copy())
hydrant_demand = hydrant_status.replace(1, 5)
