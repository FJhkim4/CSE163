# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Generates state and country df objects to be analyzed for correlation
# information between global malaria incidences and deaths. A machine
# learning model is used to predict malaria infection in United States
# if it were to become a problem (would need malaria carrying mosquitos).
# Can be used to output various stats and plots related to malaria
# infection worldwide.
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from states_class import DataFrameState
from countries_class import DataFrameCountry
from scipy.stats import pearsonr
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from numpy import ravel


# TO DO:
# **generate interesting plots from correlation & ML outputs**
def state():
    """
    Parses through selected data to generate a dataframe with all important
    information to be used for further analysis.
    """
    state = DataFrameState()
    d1 = state.area()
    d2 = state.population()
    d3 = state.temp()
    d4 = state.hospital()
    d5 = state.shape()
    dfs = [d1, d2, d3, d4, d5]
    return state.merged(dfs)


def country():
    """
    Parses through selected data to generate a dataframe with all important
    information to be used for further analysis.
    """
    country = DataFrameCountry()
    d1 = country.area()
    d2 = country.temp()
    d3 = country.hospital()
    d4 = country.shape()
    d5 = country.malaria()
    dfs = [d1, d2, d3, d4, d5]
    return country.merged(dfs)


def correlation(df):
    """
    Finds the correlation between different variables from each country and
    compares them to death rates and malaria incidence. Specifically finds
    the r and p value which determines levels of correlation. Population
    estimates, GDP per capita, hospital bed density (per 1000 people), average
    annual temperature were the evaluated factors.
    """
    # creates tuple pairs with (r, p) values for each pair
    rp_d_pop = pearsonr(list(df['POP_EST']), list(df['DEATH_100000']))
    rp_d_gdp = pearsonr(list(df['GDP_CAPITA']), list(df['DEATH_100000']))
    rp_d_hbd = pearsonr(list(df['HOSP_BEDS_DENS']), list(df['DEATH_100000']))
    rp_d_area = pearsonr(list(df['AREA']), list(df['DEATH_100000']))
    rp_d_temp = pearsonr(list(df['TEMP']), list(df['DEATH_100000']))


    rp_i_pop = pearsonr(list(df['POP_EST']), list(df['INCIDENCE_1000']))
    rp_i_gdp = pearsonr(list(df['GDP_CAPITA']), list(df['INCIDENCE_1000']))
    rp_i_hbd = pearsonr(list(df['HOSP_BEDS_DENS']), list(df['INCIDENCE_1000']))
    rp_i_area = pearsonr(list(df['AREA']), list(df['INCIDENCE_1000']))
    rp_i_temp = pearsonr(list(df['TEMP']), list(df['INCIDENCE_1000']))
    
    
def plot(df):
    """
    Plots all the merged data as scatter plots.
    """
    fig_d, [[axd1, axd2, axd3], [axd4, axd5, axd6]] = plt.subplots(nrows=2, ncols=3, figsize=(20,10))
    fig_i, [[axi1, axi2, axi3], [axi4, axi5, axi6]] = plt.subplots(nrows=2, ncols=3, figsize=(20,10))

    df.plot(kind='scatter',x='POP_EST', y='DEATH_100000', ax=axd1, color='red')
    df.plot(kind='scatter', x='GDP_CAPITA', y='DEATH_100000', ax=axd2, color='blue')
    df.plot(kind='scatter', x='HOSP_BEDS_DENS', y='DEATH_100000', ax=axd3, color='green')
    df.plot(kind='scatter', x='AREA', y='DEATH_100000', ax=axd4, color='orange')
    df.plot(kind='scatter', x='TEMP', y='DEATH_100000', ax=axd5, color='purple')

    axd1.set_title('Population Estimate vs Death Rates')
    axd2.set_title('GDP per Capita vs DeaRates')
    axd3.set_title('Hospital Beds Density vs Death Rates')
    axd4.set_title('Area vs Death Rates')
    axd5.set_title('Temperature vs Death Rates')

    df.plot(kind='scatter', x='POP_E', y='INCIDENCE_1000', ax=axi1, color='red')
    df.plot(kind='scatter', x='GDP_CAPITA', y='INCIDENCE_1000', ax=axi2, color='blue')
    df.plot(kind='scatter', x='HOSP_BEDS_DENS', y='INCIDENCE_1000', ax=axi3, color='green')
    df.plot(kind='scatter', x='AREA', y='INCIDENCE_1000', ax=axi4, color='orange')
    df.plot(kind='scatter', x='TEMP', y='INCIDENCE_1000', ax=axi5, color='purple')

    axi1.set_title('Population Estimate vs Incidence Rates')
    axi2.set_title('GDP per Capita vs Incidence Rates')
    axi3.set_title('Hospital Beds Density vs Incidence Rates')
    axi4.set_title('Area vs Incidence Rates')
    axi5.set_title('Temperature vs Incidence Rates')

    fig.delaxes(axd6)
    fig.delaxes(axi6)
    fig_d.savefig("Deathrates_vs.png")
    fig_i.savefig("Incidence_vs.png")
    

def ml(state, country):
    '''
    This function run a k_nearest_neighbors algorithium to determine which
    countries are most similar to States in the US. It then multiplies the
    instances and death rates of malaria in these countries and expropolates
    that onto US state populations. This function prints the results to
    maps of the US.
    '''

    x = state[['TEMP', 'GDP_CAPITA', 'HOSP_BEDS_DENS', ]].values
    X = country[['TEMP', 'GDP_CAPITA', 'HOSP_BEDS_DENS']].values

    y = ravel(country[['NAME']].values)
    scaler = StandardScaler()
    scaler.fit(X)
    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X, y)

    state_predict = classifier.predict(x)
    state['Closest Country'] = state_predict

    condensed_df = state.merge(country, left_on='Closest Country',
                               right_on='NAME')
    final_df = condensed_df[['STATE', 'geometry_x', 'POP_EST_x',
                             'DEATH_100000', 'INCIDENCE_1000']]
    final_df['Total_Incidence'] = (final_df['INCIDENCE_1000'] / 1000) * (
                                   final_df['POP_EST_x'])
    final_df['Total_Death'] = (final_df['DEATH_100000'] / 100000) * (
                               final_df['POP_EST_x'])
    final_df = gpd.GeoDataFrame(final_df, geometry='geometry_x')

    final_df.plot(column='Total_Incidence', legend=True, figsize=(10, 5))
    plt.title('Total Incidence of Malaria by State')
    plt.savefig('Instance_Plot.png')

    final_df.plot(column='Total_Death', legend=True, figsize=(10, 5))
    plt.title('Total Death by Malaria by State')
    plt.savefig('Death_Plot.png')


def main():
    state_df = state()  # creates states main dataframe
    # print(state_df)
    country_df = country()  # creates countries main dataframe
    # print(country_df)
    # correlation(country_df)  # determines feature correlation to labels
    ml(state_df, country_df)


if __name__ == '__main__':
    main()
    