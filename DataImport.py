"""
Created on Thu Feb 12 2022

@author: Kawtar

"""

import pandas as pd

emported_data = pd.read_csv('/Users/macbookpro/Desktop/out.csv', delimiter = ';')
emported_data = emported_data.iloc[:,1:]

winners_emported_data = pd.read_csv('/Users/macbookpro/Desktop/winners.csv', delimiter = ';')
# winners_emported_data = winners_emported_data.iloc[1: , :]