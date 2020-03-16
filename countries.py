# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Descriptiom
import pandas as pd
import geopandas as gpd


# TO DO:
# names of countries work for merge (e.g. S. Sudan vs South Sudan)
# hosp bed density for each countries most recent year
def area(file):
    """
    ready to merge
    """
    data = pd.read_csv(file)
    data.rename(columns={'2010': 'AREA', 'Country Name': 'NAME'},
                inplace=True)  # renames columns
    data['AREA'] = data['AREA'] * 0.386102  # converts area to sq miles
    data['AREA_YEAR'] = 2010
    return data[['NAME', 'AREA', 'AREA_YEAR']].dropna()


def temp(file):
    """
    ready to merge; temp in celcius
    includes data from most recent year--2013
    avg. month temps to get annual temps
    """
    data = pd.read_csv(file)
    data = data[data['dt'].str.contains('2013', regex=False)].dropna()
    data.rename(columns={'AverageTemperature': 'TEMP', 'AverageTemp' + (
        'eratureUncertainty'): 'TEMP_DEV', 'Country': 'NAME'}, inplace=True)
    data = data[['NAME', 'TEMP', 'TEMP_DEV']]
    data = data.groupby('NAME').mean().reset_index()
    data['TEMP_YEAR'] = 2013
    return data


def shape(file):
    """
    ready to merge
    """
    data = gpd.read_file(file)  # gdp in millions of dollars
    data = data[['NAME', 'GDP_MD_EST', 'POP_EST', 'GDP_YEAR',
                 'POP_YEAR', 'CONTINENT', 'geometry']]
    data['GDP_CAPITA'] = data['GDP_MD_EST'] / data['POP_EST']
    return data


def hospital(file):
    """
    get most recent hospital density and include year!!
    Includes hospital beds available in public, private, general, and
    specilized hospitals & rehab centers. Beds for acute and chronic
    care included. Density is hospital beds per 1000 people
    """
    data = pd.read_csv(file)
    # data.rename(column={'Country Name': 'NAME'}, inplace=True)
    return data


def malaria(file1, file2):
    """
    ready to merge; incidence per 1000 at risk, death is per 100000 people
    """
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)
    data1 = data1[data1['Year'] == 2015]
    data2 = data2[data2['Year'] == 2015]
    data = data1.merge(data2, left_on=['Entity', 'Year', 'Code'],
                       right_on=['Entity', 'Year', 'Code'].dropna()                   
    data.rename(columns={'Incidence of malaria (per 1,000 population at ' + (
                'risk) (per 1,000 population at risk)'): 'INCIDENCE_1000',
                'Entity': 'NAME', 'Deaths - Malaria - Sex: Both - Age: ' + (
                'Age-standardized (Rate) (per 100,000 people)'):
                'DEATH_100000'}, inplace=True)
    return data


def merge(area, temp, shape, hosp, malaria):
    """
    Merges cleaned datasets into mother dataframe for countries
    """
    print('WHOOO')


def main():
    d1 = area('https://raw.githubusercontent.com/WarrenHan/CSE163/master' + (
        '/API_AG.LND.TOTL.K2_DS2_en_csv_v2_822348.csv'))
    d2 = temp('https://raw.githubusercontent.com/WarrenHan/CSE163/master/' + (
        'GlobalLandTemperaturesByCountry.csv'))
    d3 = shape('/Users/wopr/Documents/Final Project Anne/test/data/' + (
        'ne_110m_admin_0_countries.shp'))
    d4 = hospital('https://raw.githubusercontent.com/WarrenHan/' + (
        'CSE163/master/API_SH.MED.BEDS.ZS_DS2_en_csv_v2_867087.csv'))
    d5 = malaria('https://raw.githubusercontent.com/WarrenHan/CSE163/' + (
        'master/malaria-death-rates.csv'), 'https://raw.githubuser' + (
        'content.com/WarrenHan/CSE163/master/incidence-of-malaria.csv'))
    merge(d1, d2, d3, d4, d5)


if __name__ == '__main__':
    main()
