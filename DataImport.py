"""
Created on Thu Feb 12 2022

@author: Kawtar

"""

import pandas as pd

emported_data = pd.read_csv('/Users/macbookpro/Documents/IMT-S8/DOE/DataBaseProject/TL_C_4541.csv', delimiter = ';')
emported_data = emported_data.iloc[:,1:]

winners_emported_data = pd.read_csv('/Users/macbookpro/Documents/IMT-S8/DOE/DataBaseProject/W_C_4541.csv', delimiter = ';')
# winners_emported_data = winners_emported_data.iloc[1: , :]
