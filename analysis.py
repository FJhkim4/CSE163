# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Description
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
# **make sure CORRELATIONS & ML work**
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
    compares them to death rates and malaria incidents. Specifically finds
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
    print("Death Rate Correlations:")
    print(rp_d_pop)
    print(rp_d_gdp)
    print(rp_d_hbd)
    print(rp_d_area)
    print(rp_d_temp)

    rp_i_pop = pearsonr(list(df['POP_EST']), list(df['INCIDENCE_1000']))
    rp_i_gdp = pearsonr(list(df['GDP_CAPITA']), list(df['INCIDENCE_1000']))
    rp_i_hbd = pearsonr(list(df['HOSP_BEDS_DENS']), list(df['INCIDENCE_1000']))
    rp_i_area = pearsonr(list(df['AREA']), list(df['INCIDENCE_1000']))
    rp_i_temp = pearsonr(list(df['TEMP']), list(df['INCIDENCE_1000']))
    print("Incidence Correlations:")
    print(rp_i_pop)
    print(rp_i_gdp)
    print(rp_i_hbd)
    print(rp_i_area)
    print(rp_i_temp)
    
    
def ml():
    '''
    This function run a k_nearest_neighbors
    algorithium to determine which countries are most
    similar to States in the US. It then multiplies
    the instances and death rates of malaria in these
    countries and expropolates that onto US state
    populations. This function prints the results to
    maps of the US.
    '''
    state = DataFrameState() 
    st_area = state.area()
    st_temp = state.temp()
    st_shape = state.shape()
    st_hospital = state.hospital()
    st_population = state.population()
    dfs = [st_area, st_temp, st_shape, st_hospital, st_population]
    state_merge = state.merged(dfs)

    c = DataFrameCountry() 
    c_area = c.area()
    c_temp = c.temp()
    c_shape = c.shape()
    c_hospital = c.hospital()
    c_malaria = c.malaria()
    dfs1 = [c_area, c_temp, c_shape, c_hospital, c_malaria]
    country_merge = c.merged(dfs1)


    x = state_merge[['TEMP', 'GDP_CAPITA', 'HOSP_BEDS_DENS', ]].values
    X = country_merge[['TEMP', 'GDP_CAPITA', 'HOSP_BEDS_DENS']].values

    y = ravel(country_merge[['NAME']].values)
    scaler = StandardScaler()
    scaler.fit(X)
    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X, y)

    state_predict = classifier.predict(x)
    state_merge['Closest Country'] = state_predict

    condensed_df = state_merge.merge(country_merge, left_on='Closest Country', right_on='NAME')
    final_df = condensed_df[['STATE', 'geometry_x', 'POP_EST_x', 'DEATH_100000', 'INCIDENCE_1000']]
    final_df['Total_Incidence'] = (final_df['INCIDENCE_1000'] / 1000) * final_df['POP_EST_x']
    final_df['Total_Death'] = (final_df['DEATH_100000'] / 100000) * final_df['POP_EST_x']
    final_df = gpd.GeoDataFrame(final_df, geometry='geometry_x')

    final_df.plot(column='Total_Incidence', legend=True, figsize=(15,15))
    plt.title('Total Incidence of Malaria by State')
    plt.savefig('Instance_Plot.png')

    final_df.plot(column='Total_Death', legend=True, figsize=(15,15))
    plt.title('Total Death by Malaria by State')
    plt.savefig('Death_Plot.png')


def main():
    state_df = state()  # creates states main dataframe
    print(state_df)
    country_df = country()  # creates countries main dataframe
    print(country_df)
    correlation(country_df)  # determines feature correlation to labels


if __name__ == '__main__':
    main()
