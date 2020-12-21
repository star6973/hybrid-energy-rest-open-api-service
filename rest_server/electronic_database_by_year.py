import time
from datetime import datetime
from pprint import pprint
import pandas as pd
from tabulate import tabulate
# import sys
# sys.path.insert(0, '../rest_server')
from read_electronic_by_day import read_electronic_by_day

def return_electronic_data_by_year():
    location = ['경기도', '강원도', '경상남도', '경상북도', '전라남도', '전라북도', '충청남도', '충청북도', '제주도',
                '서울특별시', '인천광역시', '대전광역시', '광주광역시', '대구광역시', '울산광역시', '부산광역시']

    administrative_area = []
    year_observation = []
    total_p_load = []

    year = ['2017', '2018']

    for y in year:
        year_observation.append(y)
        administrative_area.append('부산광역시')

    for idx, loc in enumerate(location):
        cnt = 0
        year_p_load = [0] * 24

        if loc == '부산광역시':
            electronic_total = read_electronic_by_day(location[idx])

            # 지역별로 나누기
            # 0~364 / 365~729
            for electronic_data in electronic_total:
                for idx, date in enumerate(electronic_data):
                    if cnt == 364:
                        total_p_load.append(year_p_load)
                        year_p_load = [0] * 24

                    cnt += 1

                for kdx in range(len(year_p_load)):
                    year_p_load[kdx] += electronic_data[date][kdx]

            total_p_load.append(year_p_load)

    for p_load in total_p_load:
        for idx, load in enumerate(p_load):
            p_load[idx] /= 365
            p_load[idx] = round(p_load[idx], 4)

    # print(administrative_area)
    # print(year_observation)
    # print(total_p_load)

    data = {
        'Administrative_Area': administrative_area,
        'Observation': year_observation,
        'P_load': total_p_load
    }

    df = pd.DataFrame(data, columns=['Administrative_Area', 'Observation', 'P_load'])
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    return df