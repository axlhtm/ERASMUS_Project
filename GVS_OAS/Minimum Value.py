import pandas as pd
import numpy as np 

data_dict = {
  "df1": pd.DataFrame({"X": [0.2, 0.1], "Y": [0.02, 110]}),
  "df2": pd.DataFrame({"X": [7, 8], "Y": [9, 10]}),
  "df3": pd.DataFrame({"X": [70, 0.001], "Y": [3, 2]}),
}

# List to store minimum values
min_values = []

# Loop through each dataframe in the dictionary
for name, df in data_dict.items():
  # Get the minimum value for each column (Series) and append it to the list
  min_values.append(np.min(df.values.flatten()))

print(min_values)

