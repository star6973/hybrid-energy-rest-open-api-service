import time
from datetime import datetime
from pprint import pprint
import pandas as pd
from tabulate import tabulate
# import sys
# sys.path.insert(0, '../rest_server')
from read_electronic_by_day import read_electronic_by_day

def return_electronic_data_by_month():
    location = ['경기도', '강원도', '경상남도', '경상북도', '전라남도', '전라북도', '충청남도', '충청북도', '제주도',
                '서울특별시', '인천광역시', '대전광역시', '광주광역시', '대구광역시', '울산광역시', '부산광역시']


    administrative_area = []
    month_observation = []
    month_p_load = []

    year = ['2017', '2018']
    month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    for y in year:
        for m in month:
            observation = y + '-' + m
            month_observation.append(observation)
            administrative_area.append('부산광역시')

    sum_electronic = [[0] * 24 for i in range(24)]

    for idx, loc in enumerate(location):
        if loc == '부산광역시':
            electronic_total = read_electronic_by_day(location[idx])
            # 지역별로 나누기
            for electronic_data in electronic_total:
                cnt = [0] * 24
                for idx, date in enumerate(electronic_data):

                    y = str(date)[:4]
                    m = str(date)[4:6]
                    d = str(date)[6:]

                    if y == '2017':
                        if m == '01':
                            cnt[idx] += 1
                            for jdx in range(len(sum_electronic[0])):
                                sum_electronic[0][jdx] += electronic_data[date][jdx]
                        elif m == '02':
                            for jdx in range(len(sum_electronic[1])):
                                sum_electronic[1][jdx] += electronic_data[date][jdx]
                        elif m == '03':
                            for jdx in range(len(sum_electronic[2])):
                                sum_electronic[2][jdx] += electronic_data[date][jdx]
                        elif m == '04':
                            for jdx in range(len(sum_electronic[3])):
                                sum_electronic[3][jdx] += electronic_data[date][jdx]
                        elif m == '05':
                            for jdx in range(len(sum_electronic[4])):
                                sum_electronic[4][jdx] += electronic_data[date][jdx]
                        elif m == '06':
                            for jdx in range(len(sum_electronic[5])):
                                sum_electronic[5][jdx] += electronic_data[date][jdx]
                        elif m == '07':
                            for jdx in range(len(sum_electronic[6])):
                                sum_electronic[6][jdx] += electronic_data[date][jdx]
                        elif m == '08':
                            for jdx in range(len(sum_electronic[7])):
                                sum_electronic[7][jdx] += electronic_data[date][jdx]
                        elif m == '09':
                            for jdx in range(len(sum_electronic[8])):
                                sum_electronic[8][jdx] += electronic_data[date][jdx]
                        elif m == '10':
                            for jdx in range(len(sum_electronic[9])):
                                sum_electronic[9][jdx] += electronic_data[date][jdx]
                        elif m == '11':
                            for jdx in range(len(sum_electronic[10])):
                                sum_electronic[10][jdx] += electronic_data[date][jdx]
                        elif m == '12':
                            for jdx in range(len(sum_electronic[11])):
                                sum_electronic[11][jdx] += electronic_data[date][jdx]
                    # 2018년
                    else:
                        if m == '01':
                            for jdx in range(len(sum_electronic[0])):
                                sum_electronic[12][jdx] += electronic_data[date][jdx]
                        elif m == '02':
                            for jdx in range(len(sum_electronic[1])):
                                sum_electronic[13][jdx] += electronic_data[date][jdx]
                        elif m == '03':
                            for jdx in range(len(sum_electronic[2])):
                                sum_electronic[14][jdx] += electronic_data[date][jdx]
                        elif m == '04':
                            for jdx in range(len(sum_electronic[3])):
                                sum_electronic[15][jdx] += electronic_data[date][jdx]
                        elif m == '05':
                            for jdx in range(len(sum_electronic[4])):
                                sum_electronic[16][jdx] += electronic_data[date][jdx]
                        elif m == '06':
                            for jdx in range(len(sum_electronic[5])):
                                sum_electronic[17][jdx] += electronic_data[date][jdx]
                        elif m == '07':
                            for jdx in range(len(sum_electronic[6])):
                                sum_electronic[18][jdx] += electronic_data[date][jdx]
                        elif m == '08':
                            for jdx in range(len(sum_electronic[7])):
                                sum_electronic[19][jdx] += electronic_data[date][jdx]
                        elif m == '09':
                            for jdx in range(len(sum_electronic[8])):
                                sum_electronic[20][jdx] += electronic_data[date][jdx]
                        elif m == '10':
                            for jdx in range(len(sum_electronic[9])):
                                sum_electronic[21][jdx] += electronic_data[date][jdx]
                        elif m == '11':
                            for jdx in range(len(sum_electronic[10])):
                                sum_electronic[22][jdx] += electronic_data[date][jdx]
                        elif m == '12':
                            for jdx in range(len(sum_electronic[11])):
                                sum_electronic[23][jdx] += electronic_data[date][jdx]

    for kdx, sum_ele in enumerate(sum_electronic):
        new_ele = []
        for ele in sum_ele:
            ele /= 31
            ele = round(ele, 3)
            new_ele.append(ele)

        month_p_load.append(new_ele)


    data = {
        'Administrative_Area': administrative_area,
        'Observation': month_observation,
        'P_load': month_p_load
    }

    df = pd.DataFrame(data, columns=['Administrative_Area', 'Observation', 'P_load'])
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    return df