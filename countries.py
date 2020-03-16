# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Descriptiom
import pandas as pd
import geopandas as gpd
from functools import reduce


# TO DO:
# names of countries work for merge (e.g. S. Sudan vs South Sudan)
# get the merged function to work!!!
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


# NEEDS TO BE FINISHED--GET HOSP_BEDS_DENS
def hospital(file):
    """
    get most recent hospital density and include year!!
    Includes hospital beds available in public, private, general, and
    specilized hospitals & rehab centers. Beds for acute and chronic
    care included. Density is hospital beds per 1000 people
    """
    data = pd.read_csv(file)
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
                       right_on=['Entity', 'Year', 'Code']).dropna()
    data.rename(columns={'Incidence of malaria (per 1,000 population at ' + (
                'risk) (per 1,000 population at risk)'): 'INCIDENCE_1000',
                'Entity': 'NAME', 'Deaths - Malaria - Sex: Both - Age: ' + (
                'Age-standardized (Rate) (per 100,000 people)'):
                'DEATH_100000', 'Year': 'MAL_YEAR'}, inplace=True)
    return data


def merged(dfs):
    """
    Generates mother country dataframe to be used in correlation analysis,
    machine learning, and generating plots
    """
    merge = reduce(lambda left, right: pd.merge(left, right, on=['NAME'],
                                                ), dfs)
    return merge

def correlation(df):
    """
    Finds the correlation between different variables from each country and
    compares them to death rates and malaria incidents.
    Specifically finding the r value which determines levels of correlation.
    population estimate, GDP capita, Hospital beds density, temp
    Death rates, incident rates
    """
    total_pairs = len(df['DEATH_10000']) - 1 # pairs (used to calculate r value)

    # avgs for all relevant information
    avg_pop = df['POP_EST'].mean() # pop est
    avg_gdp = df['GDP_CAPITA'].mean() # gdp capita
    avg_hbd = df['HOSP_BEDS_DENS'].mean() # hosp beds dens
    avg_temp = df['TEMP'].mean() # temp
    avg_deaths = df['DEATH_100000'].mean() # death rate
    avg_incident = df['INCIDENCE_1000'].mean() # incident  rate

    # standard deviation of all values with numerical data
    std_all = df.std(axis = 0, skipna = True) # Series

    # makes a list of tuples with x -> deathrate. ex.(pop, deathrate)
    pop_d_pairs = list(zip(list(df['POP_EST']), list(df['DEATH_10000'])))
    gdp_d_pairs = list(zip(list(df['GDP_CAPITA']), list(df['DEATH_10000'])))
    hbd_d_pairs = list(zip(list(df['HOSP_BEDS_DENS']), list(df['DEATH_10000'])))
    temp_d_pairs = list(zip(list(df['TEMP']), list(df['DEATH_10000'])))

    # makes a list of tuple with x -> incident rates
    pop_i_pairs = list(zip(list(df['POP_EST']), list(df['INCIDENCE_1000'])))
    gdp_i_pairs = list(zip(list(df['GDP_CAPITA']), list(df['INCIDENCE_1000'])))
    hbd_i_pairs = list(zip(list(df['HOSP_BEDS_DENS']), list(df['INCIDENCE_1000'])))
    temp_i_pairs = list(zip(list(df['TEMP']), list(df['INCIDENCE_1000'])))

    # for each total_pair computes function. (used to calculate r)
    pop_d_sum = reduce(lambda x, y: (x - avg_pop)(y - avg_deaths), pop_d_pairs)
    gdp_d_sum = reduce(lambda x, y: (x - avg_pop)(y - avg_deaths), gdp_d_pairs)
    hbd_d_sum = reduce(lambda x, y: (x - avg_pop)(y - avg_deaths), hbd_d_pairs)
    temp_d_sum = reduce(lambda x, y: (x - avg_pop)(y - avg_deaths), temp_d_pairs)

    pop_i_sum = reduce(lambda x, y: (x - avg_pop)(y - avg_deaths), pop_i_pairs)
    gdp_i_sum = reduce(lambda x, y: (x - avg_pop)(y - avg_deaths), gdp_i_pairs)
    hbd_i_sum = reduce(lambda x, y: (x - avg_pop)(y - avg_deaths), hbd_i_pairs)
    temp_i_sum = reduce(lambda x, y: (x - avg_pop)(y - avg_deaths), temp_i_pairs)

    # R values of all data. d = death rates, i = incident rates 
    r_d_pop = pop_d_sum / std_all['POP_EST'] * std_all['DEATH_100000'] / total_pairs
    r_d_gdp = gdp_d_sum / std_all['GDP_CAPITA'] * std_all['DEATH_100000'] / total_pairs
    r_d_hbd = hbd_d_sum / std_all['HOSP_BEDS_DENS'] * std_all['DEATH_100000'] / total_pairs
    r_d_temp = temp_d_sum / std_all['TEMP'] * std_all['DEATH_100000'] / total_pairs
    r_i_pop = pop_i_sum / std_all['POP_EST'] * std_all['INCIDENCE_1000'] / total_pairs
    r_i_gdp = gdp_i_sum / std_all['GDP_CAPITA'] * std_all['INCIDENCE_1000'] / total_pairs
    r_i_hbd = hbd_i_sum / std_all['HOSP_BEDS_DENS'] * std_all['INCIDENCE_1000'] / total_pairs
    r_i_temp = temp_i_sum / std_all['TEMP'] * std_all['INCIDENCE_1000'] / total_pairs


def main():
    d1 = area('https://raw.githubusercontent.com/WarrenHan/CSE163/master' + (
        '/API_AG.LND.TOTL.K2_DS2_en_csv_v2_822348.csv'))
    d2 = temp('https://raw.githubusercontent.com/WarrenHan/CSE163/master/' + (
        'GlobalLandTemperaturesByCountry.csv'))
    d3 = shape('/Users/wopr/Documents/Final Project Anne/test/data/' + (
        'ne_110m_admin_0_countries.shp'))
    d4 = hospital('https://raw.githubusercontent.com/WarrenHan/' + (
                  'CSE163/master/Hospital_Beds.csv'))
    d5 = malaria('https://raw.githubusercontent.com/WarrenHan/CSE163/' + (
        'master/malaria-death-rates.csv'), 'https://raw.githubuser' + (
        'content.com/WarrenHan/CSE163/master/incidence-of-malaria.csv'))
    dfs = [d1, d2, d3, d4, d5]
    countires_df = merged(dfs)
    print(countries_df)
    correlation(countries_df)


if __name__ == '__main__':
    main()
