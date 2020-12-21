from matplotlib import pyplot as plt
from Optimum_Function import Function1, Function2
from make_excel import make_excel
import pandas as pd
from tabulate import tabulate

# input a efficiency of inverter, constraints of LOLP, constraints ofdummy
print('Enter the efficiency of inverter: ')
Ef_inv = float(input())
print('Enter the constraints of LOLP(0<Con_LOLP<0.1): ')
Con_LOLP = float(input())
print('Enter the constraints of dummy(0<Con_dummy<0.05): ')
Con_dummy = float(input())
print('choice a Types of Load Pattern(P_load(1~5)): ')
prompt3 = int(input()) # prompt3는 1~5까지(P_load 값만 사용자가 입력)

flag = False
prompt1_result = []
prompt2_result = []

prompt1_result, prompt2_result = Function1(Ef_inv, Con_LOLP, Con_dummy, prompt3, flag)

cost = []
min_prompt1 = 0
min_prompt2 = 0
min_cost = 99999999
for prompt1, prompt2 in zip(prompt1_result, prompt2_result):
    IC = 1.4 * 3000 * prompt1 + 1.2 * 2290 * prompt2 * round(prompt2 / 1)
    if min_cost >= IC:
        min_cost = IC
        min_prompt1 = prompt1
        min_prompt2 = prompt2

    cost.append(IC)

# 태양광(pv) = prompt2, 풍력(wind) = prompt1
data = {
    '태양광(pv)' : prompt2_result,
    '풍력(wind)' : prompt1_result,
    'cost' : cost
}

df = pd.DataFrame(data)

print(tabulate(df, headers='keys', tablefmt='psql'))

optimal_prompt1 = min_prompt1
optimal_prompt2 = min_prompt2


P_wind, P_dummy, P_pv, P_bc, P_bd, P_load, SOC = Function2(Ef_inv, Con_LOLP, Con_dummy, optimal_prompt1, optimal_prompt2, prompt3, flag)

y_pos1 = [round(P_wind[idx], 3) for idx, y in enumerate(P_wind)]
y_pos2 = [round(P_dummy[idx], 3) for idx, y in enumerate(P_dummy)]
y_pos3 = [round(P_pv[idx], 3) for idx, y in enumerate(P_pv)]
y_pos4 = [round(bc + bd, 3) for bc, bd in zip(P_bc, P_bd)]
y_pos5 = [round(P_load[idx], 3) for idx, y in enumerate(P_load)]
y_pos6 = [round(SOC[idx], 3) for idx, y in enumerate(SOC)]

# save excel file
make_excel(y_pos1, y_pos2, y_pos3, y_pos4, y_pos5, y_pos6)

# ploting the simulation results
# P_wind 그래프
plt.subplot(3, 2, 1)
x_pos = [x for x in range(24)]
y_pos1 = [round(P_wind[idx], 3) for idx, y in enumerate(P_wind)]
plt.plot(x_pos, y_pos1)
plt.xlabel('t(h)')
plt.ylabel('Power of Wind Turbine(kWh)')

# P_dummy 그래프
plt.subplot(3, 2, 2)
y_pos2 = [round(P_dummy[idx], 3) for idx, y in enumerate(P_dummy)]
plt.plot(x_pos, y_pos2)
plt.xlabel('t(h)')
plt.ylabel('Power of Dummy(kWh)')

# P_pv 그래프
plt.subplot(3, 2, 3)
y_pos3 = [round(P_pv[idx], 3) for idx, y in enumerate(P_pv)]
plt.plot(x_pos, y_pos3)
plt.xlabel('t(h)')
plt.ylabel('Power of Photovoltaic(kWh)')

# Pbat 그래프
plt.subplot(3, 2, 4)
y_pos4 = [round(bc + bd, 3) for bc, bd in zip(P_bc, P_bd)]
plt.plot(x_pos, y_pos4)
plt.xlabel('t(h)')
plt.ylabel('Power of Battery(kWh)')

# P_load 그래프
plt.subplot(3, 2, 5)
y_pos5 = [round(P_load[idx], 3) for idx, y in enumerate(P_load)]
plt.plot(x_pos, y_pos5)
plt.xlabel('t(h)')
plt.ylabel('Power of Load(kWh)')

# SOC 그래프
plt.subplot(3, 2, 6)
y_pos6 = [round(SOC[idx], 3) for idx, y in enumerate(SOC)]
plt.plot(x_pos, y_pos6)
plt.xlabel('t(h)')
plt.ylabel('SOC(%)')

plt.show()