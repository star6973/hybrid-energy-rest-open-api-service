import pandas as pd

electronics_csv = pd.read_csv('../database/electronics.csv', encoding='euc-kr') # 2017, 2018 지역별 시간단위 발전량

def read_electronic_by_day(location):

    electronic_total = []
    cnt = 24
    for idx in range(0, len(electronics_csv), cnt):
        electronic_by_date = {}
        electronic_data = []
        electronic_data_by_loc = electronics_csv.loc[idx:cnt + idx - 1, ['거래일자', '거래시간', location]]
        # print(electronic_data_by_loc)

        observe = electronic_data_by_loc['거래일자'][idx]
        for data in electronic_data_by_loc[location].values:
            data /= 1000
            d = round(data, 4)
            electronic_data.append(d)

        electronic_by_date[observe] = electronic_data
        electronic_total.append(electronic_by_date)

    return electronic_total