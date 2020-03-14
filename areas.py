import pandas as pd


# I haven't fixed all the flake8 shit yet
def countries(data):
    data['2010'] = data['2010'] * 0.386102  # converts area to sq miles
    data['AREA_2010'] = data['2010']
    data['AREA_YEAR'] = 2010
    return data[['Country Name', 'AREA_2010', 'AREA_YEAR']]


def state(data):
    data['AREA_2010'] = data['SUBHD0303']  # total land area of states, consistent with country land area
    data['STATE'] = data['GCT_STUB.display-label1']
    data['AREA_YEAR'] = 2010
    return data.loc[1::, ['STATE', 'AREA_2010', 'AREA_YEAR']]  # includes US total land area


def main():
    countries_area = pd.read_csv('https://raw.githubusercontent.com/WarrenHan/CSE163/master/API_AG.LND.TOTL.K2_DS2_en_csv_v2_822348.csv')
    state_area = pd.read_csv('https://raw.githubusercontent.com/WarrenHan/CSE163/master/DEC_10_SF1_GCTPH1.US01PR_with_ann.csv')
    countries(countries_area)
    state(state_area)


if __name__ == '__main__':
    main()
