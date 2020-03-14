import matplotlib.pyplot as plt
import pandas as pd
import math

# Will need to change the filepath to github data
set1 = pd.read_csv('/Users/warrenhan/Downloads/malaria-death-rates.csv')
set2 = pd.read_csv('/Users/warrenhan/Downloads/incidence-of-malaria.csv')
set3 = pd.read_csv('/Users/warrenhan/Downloads/global-malaria-deaths-by-world-region.csv')
data = set1.merge(set2, left_on = ['Entity', 'Year'], right_on = ['Entity', 'Year'], how='outer')
data = data.merge(set3, left_on = ['Entity', 'Year'], right_on = ['Entity', 'Year'], how='outer')
set2 = set2[(set2['Year'] == 2014) | (set2['Year'] == 2015)]
set1 = set1[(set1['Year'] == 2014) | (set1['Year'] == 2015)]

data = set1.merge(set2, left_on = ['Entity', 'Year', 'Code'], right_on = ['Entity', 'Year', 'Code'], how='left')
data = data.dropna()
