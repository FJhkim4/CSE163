# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Descriptiom
import pandas as pd
import geopandas as gpd


# TO DO:
# names of countries work for merge (e.g. S. Sudan vs South Sudan)
# find hospital data/hosp_desnity(merge)
# get malaria data integrated
# get temp data to work

def area(file):
    """
    Description
    """
    data = pd.read_csv(file)
    data.rename(columns={'2010': 'AREA', 'Country Name': 'NAME'},
                inplace=True)  # renames columns
    data['AREA'] = data['AREA'] * 0.386102  # converts area to sq miles
    data['AREA_YEAR'] = 2010
    return data[['NAME', 'AREA', 'AREA_YEAR']].dropna()


def temp(file):
    """
    need to finish, plus TEMP_YEAR
    """
    data = pd.read_csv(file)
    # data = data[data['dt'] is True for 2013 in data['dt']]
    return data


def shape(file):
    """
    Description
    """
    data = gpd.read_file(file)  # gdp in millions of dollars
    data = data[['NAME', 'GDP_MD_EST', 'POP_EST', 'GDP_YEAR',
                 'POP_YEAR', 'CONTINENT', 'geometry']]
    data['GDP_CAPITA'] = data['GDP_MD_EST'] / data['POP_EST']
    return data


def hospital(file):
    """
    find data, hospital_year,hosp_density
    """
    data = pd.read_csv(file)
    return data


def merge(area, temp, shape, hosp, malaria):
    """
    Merges cleaned datasets into mother dataframe for countries
    """
    print('WHOOO')


# I couldn't get all the files to link from the internet
def main():
    d1 = area('https://raw.githubusercontent.com/WarrenHan/CSE163/master' + (
        '/API_AG.LND.TOTL.K2_DS2_en_csv_v2_822348.csv'))
    d2 = temp('https://raw.githubusercontent.com/WarrenHan/CSE163/master/' + (
        'GlobalLandTemperaturesByCountry.csv'))
    d3 = shape('/Users/wopr/Documents/Final Project Anne/test/data/' + (
        'ne_110m_admin_0_countries.shp'))
    # d4 = hospital(file)
    # d5 = malaria shit--warren??
    # merge(d1, d2, d3, d4, d5)


if __name__ == '__main__':
    main()
