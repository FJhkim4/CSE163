import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# need to create hosp_desnity, GDP_PER_CAPITA
def area(file):
    data = pd.read_csv(file)
    data['2010'] = data['2010'] * 0.386102  # converts area to sq miles
    data['AREA'] = data['2010']
    data['AREA_YEAR'] = 2010
    data['NAME'] = data['Country Name']
    return data[['NAME', 'AREA', 'AREA_YEAR']]


def temp(file):  # need to finish
    data = pd.read_csv(file)
    # data = data[data['dt'] is True for 2013 in data['dt']] #idk wtf im doing here, just trying to make something work


def shape(file):
    data = gpd.read_file(file)  # gdp in millions of dollars
    data = data[['NAME', 'GDP_MD_EST', 'POP_EST', 'GDP_YEAR', 'POP_YEAR', 'CONTINENT', 'geometry']]
    data['GDP_CAPITA'] = data['GDP_MD_EST'] / data['POP_EST']
    return data


def hospital(file):
    data = pd.read_csv(file)


# I couldn't get all the files to link from the internet...you'll have to download some
def main():
    area('https://raw.githubusercontent.com/WarrenHan/CSE163/master/API_AG.LND.TOTL.K2_DS2_en_csv_v2_822348.csv')
    temp('https://raw.githubusercontent.com/WarrenHan/CSE163/master/GlobalLandTemperaturesByCountry.csv')
    shape('/Users/wopr/Documents/Final Project Anne/test/data/ne_110m_admin_0_countries.shp')
    # hospital(file) need hospital data

if __name__ == '__main__':
    main()
