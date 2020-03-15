# Warren Han, Joon Ho Kim, Anne Farley
# CSE 163, Mentor: Wen Qiu
# Descriptiom
import pandas as pd
import geopandas as gpd


# TO DO:
# hospital_density(merge)
# GDP_PER_CAPITA(merge/convert str to ints/multiply by 10^-6)
# POP_DENSITY(merge)
# get temp data to work
def area(file):
    """
    Description
    """
    data = pd.read_csv(file)
    data.rename(columns={'GCT_STUB.display-label1': 'STATE',
                'SUBHD0303': 'AREA'}, inplace=True)  # renames columns
    data['AREA_YEAR'] = 2010
    return data.loc[2::, ['STATE', 'AREA', 'AREA_YEAR']]  # no na vals


# need to figure out
def temp(file):
    """
    Description
    """
    data = pd.read_csv(file)
    data = data[data['Country'] == 'United States'].dropna()
    return data


def shape(file):
    """
    GDP_MD_EST needs to be changed from a str into and int & mult. by
    10**-6 (10^-6)
    """
    data = gpd.read_file(file)
    data.rename(columns={'State_Bo_2': 'STATE', 'GDP_by_S41':
                         'GDP_MD_EST'}, inplace=True)
    data['GDP_YEAR'] = 2016
    return data[['STATE', 'GDP_MD_EST', 'GDP_YEAR', 'geometry']]  # no na vals


def hosp(file):
    """
    The STATE IDs need to be chnaged to their full names
    """
    data = gpd.read_file(file)
    data = data.loc[(data['STATUS'] == 'OPEN'), ['NAME', 'STATE']]
    data.rename(columns={'NAME': 'HOSP_COUNT'}, inplace=True)
    data = data.groupby('STATE')['HOSP_COUNT'].count().reset_index()
    data['HOSP_YEAR'] = 2019
    return data


def pop(file):
    """
    This function should be ready to merge
    """
    data = pd.read_csv(file)
    data.rename(columns={'NAME': 'STATE', 'POPESTIMATE2015': 'POP_EST'},
                inplace=True)
    data['POP_YEAR'] = 2015
    data = data[['STATE', 'POP_EST', 'POP_YEAR']]
    return data[1::]  # removes total US POP_EST, no na vals


def merge(area, temp, shape, hosp, pop):
    """
    Returns mother dataframe for states
    """
    print('WOOHOOO')


# temp file for states too big to upload on github
# link to data is in limitations doc on drive
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
    merge(d1, d2, d3, d4, d5)


if __name__ == '__main__':
    main()
