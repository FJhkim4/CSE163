# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Allows user to generate and merge DataFrames relating to world countries,
# temperature, population, geometry, Gross Domestic Product, malaria
# incidences, death rates, and hospital bed density. Includes data collection
# years for all features for reference.
import pandas as pd
import geopandas as gpd
from functools import reduce


# TO DO:
# get HOSP_YEAR for bed density from CSV (manual input)
class DataFrameCountry:
    def __init__(self):
        """
        Establishes private files from collected data.
        """
        self._area = 'https://raw.githubusercontent.com/WarrenHan/' + (
                    'CSE163/master/API_AG.LND.TOTL.K2_DS2_en_csv_v' +
                    '2_822348.csv')
        self._temp = 'https://raw.githubusercontent.com/WarrenHan/' + (
                    'CSE163/master/GlobalLandTemperaturesByCountry.csv')
        self._shape = '/Joon Kim/CSE163-project/CSE163/' + (
                     'data/ne_110m_admin_0_countries.shp')
        self._hosp = 'https://raw.githubusercontent.com/WarrenHan/' + (
                    'CSE163/master/Hospital_Beds.csv')
        self._mal = ('https://raw.githubusercontent.com/WarrenHan/' + (
                     'CSE163/master/malaria-death-rates.csv'),
                     'https://raw.githubusercontent.com/WarrenHan/' + (
                     'CSE163/master/incidence-of-malaria.csv'))

    def area(self):
        """
        Parses through 2010 data relating to country area in sq. km.
        Coverts to sq. miles to stay consistent with state data.
        """
        data = pd.read_csv(self._area)
        data.rename(columns={'2010': 'AREA', 'Country Name': 'NAME'},
                    inplace=True)  # renames columns
        data['AREA'] = data['AREA'] * 0.386102  # converts area to sq miles
        data['AREA_YEAR'] = 2010
        return data[['NAME', 'AREA', 'AREA_YEAR']].dropna()

    def temp(self):
        """
        Temperature in Celcius. Mose recent temp data is from 2013. Averages
        monthly temperatures for each country to get average annual temp.
        Degree of error included--TEMP_DEV.
        """
        data = pd.read_csv(self._temp)
        data = data[data['dt'].str.contains('2013', regex=False)].dropna()
        data.rename(columns={'AverageTemperature': 'TEMP', 'AverageTemp' + (
            'eratureUncertainty'): 'TEMP_DEV', 'Country': 'NAME'},
                    inplace=True)
        data = data[['NAME', 'TEMP', 'TEMP_DEV']]
        data = data.groupby('NAME').mean().reset_index()
        data['TEMP_YEAR'] = 2013
        return data

    def shape(self):
        """
        Parses data from CSE 163 regarding world geometry to output a
        dataframe including geometry, GDP in millions of dollars, GDP per
        capita, and population estimates.
        """
        data = gpd.read_file(self._shape)
        data = data[['NAME', 'GDP_MD_EST', 'POP_EST', 'GDP_YEAR',
                    'POP_YEAR', 'CONTINENT', 'geometry']]
        data['GDP_CAPITA'] = data['GDP_MD_EST'] / data['POP_EST']
        return data

    # GET YEARS FOR HOSP BED DENS
    def hospital(self):
        """
        Includes hospital beds available in public, private, general, and
        specilized hospitals & rehab centers. Beds for acute and chronic
        care included. Density is hospital beds per 1000 people.
        """
        data = pd.read_csv(self._hosp)
        return data

    def malaria(self):
        """
        Parses through two malaria datasets: Incidence per 1000 at risk and
        death per 100000 people. Returns a merged dataframe based on country
        name for this global information.
        """
        data1 = pd.read_csv(self._mal[0])
        data2 = pd.read_csv(self._mal[1])
        data1 = data1[data1['Year'] == 2015]
        data2 = data2[data2['Year'] == 2015]
        data = data1.merge(data2, left_on=['Entity', 'Year', 'Code'],
                           right_on=['Entity', 'Year', 'Code']).dropna()
        data.rename(columns={'Incidence of malaria (per 1,000 population' + (
                    ' at risk) (per 1,000 population at risk)'):
                    'INCIDENCE_1000', 'Entity': 'NAME', 'Deaths - Malaria' + (
                    ' - Sex: Both - Age: Age-standardized (Rate) (per 100,0' +
                    '00 people)'): 'DEATH_100000', 'Year': 'MAL_YEAR'},
                    inplace=True)
        return data

    def merged(self, dfs):
        """
        Merges cleaned dataframes from collected data to generate the country
        dataframe to be used in correlation analysis, machine learning, and
        other uses.
        """
        merge = reduce(lambda left, right: pd.merge(left, right, on=['NAME'],
                                                    ), dfs)
        return merge
