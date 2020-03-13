import matplotlib.pyplot as plt
import pandas as pd
import math

# Will need to change the filepath to github data
set1 = pd.read_csv('/Users/warrenhan/Downloads/malaria-death-rates.csv')
set2 = pd.read_csv('/Users/warrenhan/Downloads/incidence-of-malaria.csv')
set3 = pd.read_csv('/Users/warrenhan/Downloads/global-malaria-deaths-by-world-region.csv')
data = set1.merge(set2, left_on = ['Entity', 'Year'], right_on = ['Entity', 'Year'], how='outer')
data = data.merge(set3, left_on = ['Entity', 'Year'], right_on = ['Entity', 'Year'], how='outer')
data.drop(columns=['Code_x', 'Code_y'])
