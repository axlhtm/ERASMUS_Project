import pandas as pd

def append_dataframes(data_dict):
  """
  This function takes a dictionary containing DataFrames and appends them
  into a single new DataFrame using pd.concat.

  Args:
      data_dict (dict): A dictionary where keys are arbitrary names and values are DataFrames.

  Returns:
      pandas.DataFrame: The appended DataFrame containing all data from the input dictionary.
  """
  # List to store non-empty DataFrames
  dfs = []

  # Loop through each DataFrame in the dictionary
  for key, df in data_dict.items():
    # Check if DataFrame is empty (skip if empty)
    if not df.empty:
      dfs.append(df)

  # Concatenate the non-empty DataFrames into a new DataFrame (handle pkotential mismatch in column names)
  appended_df = pd.concat(dfs, ignore_index=True)  # Avoid duplicate indexing

  return appended_df

# Example dictionary with multiple DataFrames
data_dict = {
  'df5': pd.DataFrame({'col4': ['a', 'b', 'c']}),
  'df2': pd.DataFrame({'col1': [7, 8, 9], 'col2': [10, 11, 12]}),
  'df1': pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}),
  'df3': pd.DataFrame({'col3': [13, 14, 15]}),  # Example with different column names
  'df4': pd.DataFrame()  # Example with empty DataFrame
}

# Get the appended DataFrame
appended_df = append_dataframes(data_dict.copy())  # Avoid modifying original dictionary

# Print the appended DataFrame
print(appended_df)
