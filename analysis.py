# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Description
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from states_class import DataFrameState
from countries_class import DataFrameCountry
from scipy.stats import pearsonr


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


def plot(df):
    """
    Plots all the merged data as scatter plots.
    """
    fig_d, [axd1, axd2, axd3, axd4, axd5] = plt.subplots(5)
    fig_i, [axi1, axi2, axi3, axi4, axi5] = plt.subplots(5)

    df.plot.scatter(x=df['POP_EST'], y=df['DEATH_100000'], ax=axd1)
    df.plot.scatter(x=df['GDP_CAPITA'], y=df['DEATH_100000'], ax=axd2)
    df.plot.scatter(x=df['HOSP_BEDS_DENS'], y=df['DEATH_100000'], ax=axd3)
    df.plot.scatter(x=df['AREA'], y=df['DEATH_100000'], ax=axd4)
    df.plot.scatter(x=df['TEMP'], y=df['DEATH_100000'], ax=axd5)

    axd1.set_title('Population Estimate vs Death Rates')
    axd2.set_title('GDP per Capita vs Death Rates')
    axd3.set_title('Hospital Beds Density vs Death Rates')
    axd4.set_title('Area vs Death Rates')
    axd5.set_title('Temperature vs Death Rates')

    df.plot.scatter(x=df['POP_EST'], y=df['INCIDENCE_1000'], ax=axi1)
    df.plot.scatter(x=df['GDP_CAPITA'], y=df['INCIDENCE_1000'], ax=axi2)
    df.plot.scatter(x=df['HOSP_BEDS_DENS'], y=df['INCIDENCE_1000'], ax=axi3)
    df.plot.scatter(x=df['AREA'], y=df['INCIDENCE_1000'], ax=axi4)
    df.plot.scatter(x=df['TEMP'], y=df['INCIDENCE_1000'], ax=axi5)

    axi1.set_title('Population Estimate vs Incident Rates')
    axi2.set_title('GDP per Capita vs Incident Rates')
    axi3.set_title('Hospital Beds Density vs Incident Rates')
    axi4.set_title('Area vs Incident Rates')
    axi5.set_title('Temperature vs Incident Rates')

    fig_d.savefig("death_rates.png")
    fig_i.savefig("inc_rates.png")


def main():
    state_df = state()  # creates states main dataframe
    print(state_df)
    country_df = country()  # creates countries main dataframe
    print(country_df)
    correlation(country_df)  # determines feature correlation to labels
    plot(country_df)


if __name__ == '__main__':
    main()
