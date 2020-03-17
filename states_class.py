# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Allows user to generate and merge DataFrames relating to US state
# area, temperature, population, geometry, Gross Domestic Product, and
# hospital bed density. Includes data collection years for all features
# for reference.
import pandas as pd
import geopandas as gpd
from switch_class import IdSwitch
from functools import reduce


# TO DO:
# deal with flake8 warning thrown when using the IdSwitch class
class DataFrameState:
    def __init__(self):
        """
        Establishes private files from collected data.
        """
        self._area = 'https://raw.githubusercontent.com/WarrenHan/' + (
                    'CSE163/master/DEC_10_SF1_GCTPH1.US01PR_with_ann.csv')
        self._temp = '/Users/wopr/Documents/Final Project Anne/test/data/' + (
                    'GlobalLandTemperaturesByState.csv')
        self._shape = '/Users/wopr/Documents/Final Project Anne/test/' + (
                     'data/Gross_Domestic_Product_GDP_by_state_19972016/' +
                     'Gross_Domestic_Product_GDP_by_state_19972016.shp')
        self._hosp = 'https://opendata.arcgis.com/datasets/6ac5e325468' + (
                    'c4cb9b905f1728d6fbf0f_0.geojson')
        self._pop = 'https://raw.githubusercontent.com/WarrenHan/' + (
                'CSE163/master/scprc-est2015-18-pop-res.csv')

    def area(self):
        """
        Parses through 2010 census data relating to state area in sq. miles.
        land area included rather than total to stay consistent with global
        data and temperature data (land temp).
        """
        data = pd.read_csv(self._area)
        data.rename(columns={'GCT_STUB.display-label1': 'STATE',
                    'SUBHD0303': 'AREA'}, inplace=True)  # renames columns
        data['AREA_YEAR'] = 2010
        return data.loc[2::, ['STATE', 'AREA', 'AREA_YEAR']]  # no na vals

    def temp(self):
        """
        Temperature in Celcius. Mose recent temp data is from 2013. Averages
        monthly temperatures for each US state to get average annual temp.
        Degree of error included--TEMP_DEV.
        """
        data = pd.read_csv(self._temp)
        data = data[data['Country'] == 'United States']
        data = data[data['dt'].str.contains('2013', regex=False)].dropna()
        data.rename(columns={'AverageTemperature': 'TEMP', 'AverageTemp' + (
                    'eratureUncertainty'): 'TEMP_DEV', 'State': 'STATE'},
                    inplace=True)
        data = data[['STATE', 'TEMP', 'TEMP_DEV']]
        data = data.groupby('STATE').mean().reset_index()
        data['TEMP_YEAR'] = 2013
        # ensures Georgia stats merge properly
        data.loc[(data['STATE'].str.contains('Georgia')), 'STATE'] = 'Georgia'
        return data

    def shape(self):
        """
        Generates a GeoDataFrame that includes state GDP estimates in
        millions of dollars--to keep consistent with country GDP units.
        This conversion was accomplished via *10**-6.
        """
        data = gpd.read_file(self._shape)
        data.rename(columns={'State_Bo_2': 'STATE', 'GDP_by_S41':
                    'GDP_MD_EST'}, inplace=True)
        data['GDP_YEAR'] = 2016
        data['GDP_MD_EST'] = data['GDP_MD_EST'].astype(float) * 10**-6
        return data[['STATE', 'GDP_MD_EST', 'GDP_YEAR', 'geometry']]  # no na

    # DEAL WITH WARNING flake8 throws when using the class IdSwitch
    def hospital(self):
        """
        Calculates the total amount of hospital beds available in each state
        and returns a dataframe with this information along with state name.
        Hospitals with negative values for bed count were not considered.
        """
        data = gpd.read_file(self._hosp)
        data = data.loc[(data['STATUS'] == 'OPEN') & (data['BEDS'] > 0),
                        ['BEDS', 'STATE']]
        data.rename(columns={'BEDS': 'HOSP_BEDS'}, inplace=True)
        data = data.groupby('STATE')['HOSP_BEDS'].sum().reset_index()
        data['HOSP_YEAR'] = 2019

        # switches the STATE col from ID to state name
        states = IdSwitch(data['STATE'])
        states.add('DC', 'District of Columbia')
        states.add('GU', 'Guam')
        states.add('PR', 'Puerto Rico')
        states.add('PW', 'Palau')
        states.add('VI', 'Virgin Islands')
        states = states.switch()
        data['STATE'] = states
        return data

    def population(self):
        """
        Calculates the population estimate for each state (incuding
        Puerto Rico) and returns this as dataframe with the corresponding
        year the data was collected.
        """
        data = pd.read_csv(self._pop)
        data.rename(columns={'STATE': 'ID', 'NAME': 'STATE',
                    'POPESTIMATE2015': 'POP_EST'}, inplace=True)
        data['POP_YEAR'] = 2015
        data = data[['STATE', 'POP_EST', 'POP_YEAR']]
        data.loc[(data['STATE'].str.contains('Puerto Rico')), 'STATE'] = (
                'Puerto Rico')
        return data[1::]  # removes total US POP_EST, no na vals

    def merged(self, dfs):
        """
        Merges cleaned dataframes from collected data to generate the state
        dataframe to be used in correlation analysis, machine learning, and
        other uses.
        """
        merge = reduce(lambda left, right: pd.merge(left, right, on=['STATE'],
                                                    ), dfs)
        merge['GDP_CAPITA'] = merge['GDP_MD_EST'] / merge['POP_EST']
        # calculates hospital beds available per 1000 people
        merge['HOSP_BEDS_DENS'] = merge['HOSP_BEDS'] / merge['POP_EST'] * 1000
        return merge
