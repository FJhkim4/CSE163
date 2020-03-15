import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt

# need to create hospital_density, GDP_PER_CAPITA, POP_DENSITY

def area(file):
    data = pd.read_csv(file)
    data['AREA'] = data['SUBHD0303']  # total land area of states, consistent with country land area
    data['STATE'] = data['GCT_STUB.display-label1']
    data['AREA_YEAR'] = 2010
    return data.loc[2::, ['STATE', 'AREA', 'AREA_YEAR']]


def temp(file):  # need to finsih
    data = pd.read_csv(file)
    data = data[data['Country'] == 'United States']
    return data


def shape(file):  # GDP values are in dollars--need to be converted to ints & millions of dollars (*10**-6)
    data = gpd.read_file(file)
    data['STATE'] = data['State_Bo_2']
    data['GDP_MD_EST'] = data['GDP_by_S41']
    data['GDP_YEAR'] = 2016
    data = data[['STATE', 'GDP_MD_EST', 'GDP_YEAR', 'geometry']]

def hospital(file):
    data = gpd.read_file(file)
    data = data.loc[(data['STATUS'] == 'OPEN'), ['NAME', 'STATE']]
    data = data.groupby('STATE')['NAME'].count()
    return data # STATE (e.g. WA) as index, followed by total hospitals per state, need to add HOSP_YEAR = 2019
  

def pop(file):
    # working on it rn


def main():  # temp file for states too big to upload on github, link to data is in limitations doc on drive
    area('https://raw.githubusercontent.com/WarrenHan/CSE163/master/DEC_10_SF1_GCTPH1.US01PR_with_ann.csv')
    temp('/Users/wopr/Documents/Final Project Anne/test/data/GlobalLandTemperaturesByState.csv')
    shape('/Users/wopr/Documents/Final Project Anne/test/data/Gross_Domestic_Product_GDP_by_state_19972016/Gross_Domestic_Product_GDP_by_state_19972016.shp')
    hospital('https://opendata.arcgis.com/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0.geojson')
    pop('https://raw.githubusercontent.com/WarrenHan/CSE163/master/scprc-est2015-18-pop-res.csv')

if __name__ == '__main__':
    main()
