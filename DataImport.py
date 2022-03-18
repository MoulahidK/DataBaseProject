"""
Created on Thu Feb 12 2022

@author: Kawtar

"""

import pandas as pd
#Importing scraped data of the matches played
emported_data = pd.read_csv('/Users/macbookpro/Documents/IMT-S8/DOE/DataBaseProject/TL_C_4541.csv', delimiter = ';')
emported_data = emported_data.iloc[:,1:]

#Importing scraped data of the winner teams
winners_emported_data = pd.read_csv('/Users/macbookpro/Documents/IMT-S8/DOE/DataBaseProject/W_C_4541.csv', delimiter = ';')

