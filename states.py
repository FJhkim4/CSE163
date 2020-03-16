# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Descriptiom
import pandas as pd
# import geopandas as gpd
from switch import IdSwitch
from functools import reduce


# TO DO:
# deal with flake8 warning thrown when using the IdSwitch class
def area(file):
    """
    ready to merge
    """
    data = pd.read_csv(file)
    data.rename(columns={'GCT_STUB.display-label1': 'STATE',
                'SUBHD0303': 'AREA'}, inplace=True)  # renames columns
    data['AREA_YEAR'] = 2010
    return data.loc[2::, ['STATE', 'AREA', 'AREA_YEAR']]  # no na vals


def temp(file):
    """
    ready to merge, temp in celcius
    includes data from most recent year--2013
    avg. month temps to get annual temps
    """
    data = pd.read_csv(file)
    data = data[data['Country'] == 'United States']
    data = data[data['dt'].str.contains('2013', regex=False)].dropna()
    data.rename(columns={'AverageTemperature': 'TEMP', 'AverageTemp' + (
        'eratureUncertainty'): 'TEMP_DEV', 'State': 'STATE'}, inplace=True)
    data = data[['STATE', 'TEMP', 'TEMP_DEV']]
    data = data.groupby('STATE').mean().reset_index()
    data['TEMP_YEAR'] = 2013
    # ensures Georgia stats merge properly
    data.loc[(data['STATE'].str.contains('Georgia')), 'STATE'] = 'Georgia'
    return data


def shape(file):
    """
    ready to merge; converts $ to millions of $ for GDP
    """
    data = gpd.read_file(file)
    data.rename(columns={'State_Bo_2': 'STATE', 'GDP_by_S41':
                         'GDP_MD_EST'}, inplace=True)
    data['GDP_YEAR'] = 2016
    data['GDP_MD_EST'] = data['GDP_MD_EST'].astype(float) * 10**-6  # converts
    return data[['STATE', 'GDP_MD_EST', 'GDP_YEAR', 'geometry']]  # no na vals


def hosp(file):
    """
    DEAL WITH WARNING flake8 throws when using the class IdSwitch
    """
    data = gpd.read_file(file)
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


def pop(file):
    """
    ready to merge
    """
    data = pd.read_csv(file)
    data.rename(columns={'STATE': 'ID', 'NAME': 'STATE',
                         'POPESTIMATE2015': 'POP_EST'}, inplace=True)
    data['POP_YEAR'] = 2015
    data = data[['STATE', 'POP_EST', 'POP_YEAR']]
    data.loc[(data['STATE'].str.contains('Puerto Rico')), 'STATE'] = (
            'Puerto Rico')
    return data[1::]  # removes total US POP_EST, no na vals


def merged(dfs):
    """
    Generates mother states dataframe to be used in correlation analysis,
    machine learning, and generating plots
    """
    merge = reduce(lambda left, right: pd.merge(left, right, on=['STATE'],
                                                ), dfs)
    merge['GDP_CAPITA'] = merge['GDP_MD_EST'] / merge['POP_EST']
    # calculates hospital beds available per 1000 people
    merge['HOSP_BEDS_DENS'] = merge['HOSP_BEDS'] / merge['POP_EST'] * 1000
    return merge


def main():
    d1 = area('https://raw.githubusercontent.com/WarrenHan/CSE163/master/' + (
        'DEC_10_SF1_GCTPH1.US01PR_with_ann.csv'))
    d2 = temp('/Users/wopr/Documents/Final Project Anne/test/data/' + (
        'GlobalLandTemperaturesByState.csv'))
    d3 = shape('/Users/wopr/Documents/Final Project Anne/test/data/' + (
        'Gross_Domestic_Product_GDP_by_state_19972016/' +
        'Gross_Domestic_Product_GDP_by_state_19972016.shp'))
    d4 = hosp('https://opendata.arcgis.com/datasets/' + (
        '6ac5e325468c4cb9b905f1728d6fbf0f_0.geojson'))
    d5 = pop('https://raw.githubusercontent.com/WarrenHan/CSE163/' + (
        'master/scprc-est2015-18-pop-res.csv'))
    dfs = [d1, d2, d3, d4, d5]
    merged(dfs)


if __name__ == '__main__':
    main()
