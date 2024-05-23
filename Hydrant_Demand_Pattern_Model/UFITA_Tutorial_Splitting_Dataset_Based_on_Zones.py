# Import Python Libraries
import glob
import numpy as np
import os 
import pandas as pd
import wntr 

# =============================================================================
# PART I. - SPLITTING DATASED BASED ON ZONES
# =============================================================================

# I. 1. Change Working Directory
os.chdir('G:/My Drive/Work Data/Politecnico di Milano/Data/UFITA Irrigation Network/Hydrant_Historical_Operation_Excel/') 

# I. 2. Import Historical Hydrant Usage 
data_2005_CEW = pd.read_excel('Esercizio irriguo anno 2005.xlsx', sheet_name = 'data_2005_CEW') # Dataset 2005 wtih Central, East and West Region
data_2006_CEW = pd.read_excel('Esercizio irriguo anno 2006.xlsx', sheet_name = 'data_2006_CEW') # Dataset 2006 wtih Central, East and West Region
data_2007_CEW = pd.read_excel('Esercizio_irriguo_anno_2007.xlsx', sheet_name = 'data_2007_CEW') # Dataset 2007 wtih Central, East and West Region
data_2008_CEW = pd.read_excel('Esercizio irriguo anno 2008.xlsx', sheet_name = 'data_2008_CEW') # Dataset 2008 wtih Central, East and West Region
data_2009_CEW = pd.read_excel('Esercizio irriguo anno 2009.xlsx', sheet_name = 'data_2009_CEW') # Dataset 2009 wtih Central, East and West Region
data_2010_CEW = pd.read_excel('Esercizio irriguo anno 2010.xlsx', sheet_name = 'data_2010_CEW') # Dataset 2010 wtih Central, East and West Region

# I. 3. Splitting Dataset Based on Zones
data_2005_CE  = data_2005_CEW[~data_2005_CEW['Idrante'].str.startswith('A')]
data_2005_CE  = data_2005_CE[~data_2005_CE['Idrante'].str.startswith('a')]
data_2005_CE  = data_2005_CE[~data_2005_CE['Idrante'].str.startswith('M')]
data_2005_CE  = data_2005_CE[~data_2005_CE['Idrante'].str.contains("bis", case=False)]

data_2006_CE  = data_2006_CEW[~data_2006_CEW['Idrante'].str.startswith('A')]
data_2006_CE  = data_2006_CE[~data_2006_CE['Idrante'].str.startswith('a')]
data_2006_CE  = data_2006_CE[~data_2006_CE['Idrante'].str.startswith('M')]
data_2006_CE  = data_2006_CE[~data_2006_CE['Idrante'].str.contains("bis", case=False)]

data_2007_CE  = data_2007_CEW[~data_2007_CEW['Idrante'].str.startswith('A')]
data_2007_CE  = data_2007_CE[~data_2007_CE['Idrante'].str.startswith('a')]
data_2007_CE  = data_2007_CE[~data_2007_CE['Idrante'].str.startswith('M')]
data_2007_CE  = data_2007_CE[~data_2007_CE['Idrante'].str.contains("bis", case=False)]

data_2008_CE  = data_2008_CEW[~data_2008_CEW['Idrante'].str.startswith('A')]
data_2008_CE  = data_2008_CE[~data_2008_CE['Idrante'].str.startswith('a')]
data_2008_CE  = data_2008_CE[~data_2008_CE['Idrante'].str.startswith('M')]
data_2008_CE  = data_2008_CE[~data_2008_CE['Idrante'].str.contains("bis", case=False)]

data_2009_CE  = data_2009_CEW[~data_2009_CEW['Idrante'].str.startswith('A')]
data_2009_CE  = data_2009_CE[~data_2009_CE['Idrante'].str.startswith('a')]
data_2009_CE  = data_2009_CE[~data_2009_CE['Idrante'].str.startswith('M')]
data_2009_CE  = data_2009_CE[~data_2009_CE['Idrante'].str.contains("bis", case=False)]

data_2010_CE  = data_2010_CEW[~data_2010_CEW['Idrante'].str.startswith('A')]
data_2010_CE  = data_2010_CE[~data_2010_CE['Idrante'].str.startswith('a')]
data_2010_CE  = data_2010_CE[~data_2010_CE['Idrante'].str.startswith('M')]
data_2010_CE  = data_2010_CE[~data_2010_CE['Idrante'].str.contains("bis", case=False)]

