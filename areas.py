import pandas as pd


def countries(data):
    data['2010'] = data['2010'] * 0.386102  # converts area to sq miles
    data['AREA_2010'] = data['2010']
    return data[['Country Name', 'AREA_2010']]


def state(data):
    data['AREA_2010'] = data['SUBHD0302']  # total land area of states-consistent with country land area
    data['STATE'] = data['GCT_STUB.display-label1']  # can't get rid of US before state bc the original CSV has them labeled as the same :(
    return data.loc[1::, ['STATE', 'AREA_2010']]


def main():
    countries_area = pd.read_csv('https://raw.githubusercontent.com/WarrenHan/CSE163/master/API_AG.LND.TOTL.K2_DS2_en_csv_v2_822348.csv')
    state_area = pd.read_csv('https://raw.githubusercontent.com/WarrenHan/CSE163/master/DEC_10_SF1_GCTPH1.US01PR_with_ann.csv')
    countries(countries_area)
    state(state_area)


if __name__ == '__main__':
    main()  # I haven't fixed all the flake8 shit yet
