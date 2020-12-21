
# Enter capacity(MW) and daily pattern data of Load

Pload_24 = 10*[1.8, 2.3, 1.8, 2, 1.7, 1.5, 1, 1.2, 1.2, 1.5, 2, 2.5, 1.8, 2, 1.8, 2, 1.55, 1.55, 1.1, 1.2, 1.2, 1.4, 2, 2.7]            # 부하 곡선 [MW]
u = [7.15, 12, 12, 12, 12, 11.64, 11.46, 6.53, 12, 9.87, 12, 12, 12, 10.69, 12, 10.69, 9.21, 9.66, 6.85, 8.74, 9.66, 5.48, 7.15, 7.72]  # 풍속 데이터 [m/s]
rad = [0, 0, 0.22, 0.22, 0.46, 0.46, 0.77, 0.77, 0.91, 0.91, 1, 1, 1, 1, 0.96, 0.96, 0.88, 0.88, 0.66, 0.66, 0.72, 0.42, 0.22, 0.22]    # 일사량 데이터[kW/m2]

# [m,n] = size(Pload_24)
m = 1
n = len(Pload_24)

want_time = [0] * n                 # 데이터를 얼마나 자세히 볼 것인가?
x = 1                               # 신재생 용량 조절
dx = x * 2.5/100                    # 신재생 용량 증감분 [%]

# Enter 제약조건
low_pri = 0.25               # 후순위 부하 비율(Load shifting 가능한 부하) [%/100]
Set_LOLP_HP = 0.05           # 우선순위 부하 허용 LOLP [%/100]
Set_LLP_hour = 24*8          # 허용 LOLP [h]
Set_dummy = 0.05             # 허용 더미 비율 [%/100]

# Enter capacity(MW) and daily pattern data of WT
Pw_24 = [0] * 24
uc = 3              # 최소 발전가능한 풍속 제한 [m/s]
uf = 25             # 최대 발전가능한 풍속 제한 [m/s]
ur = 12             # 정격 풍속 [m/s]
Pr = x * 10 * 3.2   # WT 정격용량[MW]

for t in range(24):
    if (u[t] < uc) or (u[t] > uf):
        Pw_24[t] = 0                                                          # WT 출력 [MW]
    else:
        if uc <= u[t] and u[t] <= ur:
            Pw_24[t] = round(Pr * (u[t]*u[t] - uc*uc) / (ur*ur - uc*uc), 4)   # WT 출력 [MW]
        else:
            if ur <= u[t] and u[t] <= uf:
                Pw_24[t] = Pr                                                 # WT 출력 [MW]

# Cal capacity(MW) and daily pattern data of PV
Ppv_24 = [0] * 24
PVA = x * 9000    # PV 발전 면적[m2]

for t in range(24):
    Ppv_24[t] = PVA * rad[t] / 1000 # PV 출력 [MW]


time = [0] * n

# 24의 길이에서 하나씩 더 추가해서 총 배열의 길이가 25?
Pload_24 = Pload_24
Pw_24 = Pw_24
Ppv_24 = Ppv_24

Pload = [0] * n
Pw = [0] * n
Ppv = [0] * n

for i in range(max(want_time)):
    Pload[i] = interp1d(time, Pload_24, (n*i)/max(want_time))
    Pw[i] = interp1d(time, Pw_24, (n*i)/max(want_time))
    Ppv[i] = interp1d(time, Ppv_24, (n*i)/max(want_time))

# Pload_24(:,25) = []
# Pw_24(:,25) = []
# Ppv_24(:,25) = []
time = want_time


m = 1
n = len(Pload)


# Enter efficiency of inverter (Modeling and Simulation of Smart grid integrated with hybrid renewable energy systems 참고)
n_inv = 0.95    # 인버터 효율 [%/100]

# Enter battery data, , initial SOC(%), SOC_min(%), SOC_max(%), P_bc(MW), P_bd(MW)
C_bat = 30          # 배터리 용량[MWh]
SOC_ini = 0.5       # 초기 SOC [%/100]
SOC_min = 0.1       # minimum SOC of battery [%/100]
SOC_max = 0.85      # maximum SOC of battery [%/100]

P_bc = [0] * n      # output of battery in charge mode
P_bd = [0] * n      # output of battery in discharge mode

n_BC = 0.9          # efficiency of battery in charge mode [%/100]
n_BD = 0.85         # efficiency of battery in discharge mode [%/100]
r_sd = 0.002        # self-discharge rate of battery [%/100]

# Enter diesel generator capacity(MW), output(MW) and efficiency
P_dgr = 10          # DG 정격 용량 [MW]
P_dg = [0] * n      # DG 시간당 출력 [MW]
Ef_dg = 0.95        # DG 효율 [%/100]

# Parameters Calculation
P_LP =  Pload * low_pri             # 후순위 부하 용량 계산
P_HP =  Pload * (1-low_pri)         # 우선순위 부하 용량 계산

P_L_avg = sum(P_LP)/n               # 후순위 부하 평균 용량 계산 [MW]
P_LLP_sum_ref = (8*24)*P_L_avg      # 후순위 부하 용량 계산 [MWh]

Cal_dummy = sum(Pload)*Set_dummy    # 허용 더미 비율 [%/100]

SOC = [0] * n + 1                   # initial SOC of battery at each time
SOC[0] = SOC_ini


# NPPBSG algorithm
want_iter = 100
max_iter = want_iter

for iter in range(want_iter):

        LOLP_HP(iter,:) = [0] * n        # initial LOLP at each time [h]
        P_HPL(iter,:) = [0] * n          # 실제로 우선순위부하에 공급된 전력량 [MWh]
        P_LLP(iter,:) = [0] * n          # 실제로 후순위부하에 공급된 전력량 [MWh]
        P_LLP_sum(iter,:) = [0] * n      # 후순위부하에 공급되지 못한량 누적 [MWh]
        dummy(iter,:) = [0] * n          # 실시간 더미 필요량 [MWh]
        dummy_sum(iter,:) = [0] * n      # 더미 누적량 [MWh]
        P_dg(iter,:) = [0] * n           # 디젤 발전량 [MWh]

        if iter == 1:
           Pw(iter,:) = x(iter,1) * Pw(1,:)     # WT 출력 [MW]
           Ppv(iter,:) = x(iter,1) * Ppv(1,:)   # PV 출력 [MW]
        else:
           Pw(iter,:) = x(iter,1) * Pw(1,:)/x(1,1)      # WT 출력 [MW]
           Ppv(iter,:) = x(iter,1) * Ppv(1,:)/x(1,1)    # PV 출력 [MW]


        Pload(iter,:) =  Pload(1,:)         # 후순위 부하 용량
        P_LP(iter,:) =  P_LP(1,:)           # 후순위 부하 용량
        P_HP(iter,:) =  P_HP(1,:)           # 우선순위 부하 용량

        SOC(iter+1,:) = zeros(1,n+1)        # initial SOC of battery at each time
        SOC(iter,1) = SOC_ini

        P_bc(iter+1,:) = zeros(1,n)         # output of battery in charge mode
        P_bd(iter+1,:) = zeros(1,n)         # output of battery in discharge mode

        E_bat(iter,1) = C_bat*SOC_ini       # initial MWh capacity of battery at each time


    for t = 1:n    # initial time (time step)

        if t == 1:   # 후순위부하 부족량 초기 적산
            P_LLP_sum(iter,t) = P_LP(iter,1)
        else:
            P_LLP_sum(iter,t) = P_LLP_sum(iter,t-1) + P_LP(iter,t)


        if(Pw(iter,t) > P_HP(iter,t)): # 1. 풍력이 우선순위 부하를 모두 감당할 수 있나?

            if(SOC(iter,t) < SOC_max): # 1-1. 풍력이 너무 많은데, 우선순위 부하를 감당하고 남은 양을 배터리에 저장할수 있나?

                if ((Pw(iter,t)-P_HP(iter,t)*n_inv+Ppv(iter,t))*n_BC <= SOC_max*C_bat-E_bat(iter,t)): # 1-1-a. 이번시간에 모든 잉여전력을 배터리가 정말로 감당 가능하나?

                    P_bc(iter,t) = (Pw(iter,t)-P_HP(iter,t)*n_inv+Ppv(iter,t))*n_BC # 1-1-a. 맞다면 잉여전력을 모두 충전하라
                    P_LLP(iter,t) = 0 # 후순위 부하에는 공급하지 않는다.

                else:        # 1-1-b. SOC 여유는 있지만, 이번시간에 잉여전력을  모두 배터리가 감당할 수는 없다.(일부 잉여전력이라도 충전함)

                    P_bc(iter,t) = (SOC_max*C_bat-E_bat(iter,t))    # 1-1-b. 배터리 SOC 최대까지만 충전하라

                    if P_LLP_sum(iter,t) > ((Pw(iter,t)-P_HP(iter,t))+Ppv(iter,t)*n_inv - P_bc(iter,t)):    # 후순위부하(적산치)가 모두 감당할 수 있나?
                        P_LLP(iter,t) = ((Pw(iter,t)-P_HP(iter,t))+Ppv(iter,t)*n_inv - P_bc(iter,t))        # 1-1-b. 나머지는 후순위 부하로 공급하라.
                    else:  # 만약 넘친다면
                        P_LLP(iter,t) = P_LLP_sum(iter,t)   # 1-1-b. 후순위부하(적분치)로 공급하고 더미로 갈 용량 체크
                        dummy(iter,t) =  (Pw(iter,t)-P_HP(iter,t))+Ppv(iter,t)*n_inv - P_bc(iter,t) - P_LLP(iter,t) # 1-4. 더미부하로 태워라

                    P_LLP_sum(iter,t) = P_LLP_sum(iter,t) - P_LLP(iter,t)

                if t == 1:
                       dummy_sum(iter,1) = dummy(iter,1)    # 더미부하 적산
                else:
                       dummy_sum(iter,t) = dummy_sum(iter,t-1) + dummy(iter,t)  # 더미부하 적산


                P_HPL(iter,t) = P_HP(iter,t)    # 우선순위 부하에 공급된 전력량

            else:    # SOC full charge 라면,

                    if  P_LLP_sum(iter,t) > (Pw(iter,t)-P_HP(iter,t))+Ppv(iter,t)*n_inv:      # 후순위부하(적산치)가 모두 감당할 수 있나?
                        P_LLP(iter,t) = ((Pw(iter,t)-P_HP(iter,t))+Ppv(iter,t)*n_inv)       # 1-1-b. 나머지는 후순위 부하로 공급하라.
                    else: # 만약 넘친다면
                        P_LLP(iter,t) =  P_LLP_sum(iter,t)  # 1-1-b. 후순위부하(적산)로 공급하고 더미로 갈 용량 체크
                        dummy(iter,t) =  ((Pw(iter,t)-P_HP(iter,t))+Ppv(iter,t)*n_inv) -  P_LLP_sum(iter,t) # 1-4. 더미부하로 태워라


                    P_LLP_sum(iter,t) = P_LLP_sum(iter,t) - P_LLP(iter,t)

                    if t == 1:
                       dummy_sum(iter,1) = dummy(iter,1)    # 더미부하 적산
                    else:
                       dummy_sum(iter,t) = dummy_sum(iter,t-1) + dummy(iter,t)  # 더미부하 적산

                    P_HPL(iter,t) = P_HP(iter,t)    # 우선순위 부하에 공급된 전력량



        elif (Pw(iter,t) + Ppv(iter,t)*n_inv > P_HP(iter,t)): # 2. 풍력+태양광이 우선순위 부하를 모두 감당할 수 있나?

            if(SOC(iter,t) < SOC_max): # 2-1. 풍력+태양광이 너무 많은데, 우선순위 부하를 감당하고 남은 양을 배터리에 저장할수 있나?

                if ((Ppv(iter,t)-(P_HP(iter,t)-Pw(iter,t))/n_inv)*n_BC <= SOC_max*C_bat-E_bat(iter,t)): # 2-1-a. 이번시간에 모든 잉여전력을 배터리가 정말로 감당 가능하나?
                    P_bc(iter,t) = (Ppv(iter,t)-(P_HP(iter,t)-Pw(iter,t))/n_inv)*n_BC # 2-1-a. 맞다면 잉여전력을 모두 충전하라
                    P_LLP(iter,t) = 0;

                else:        # 2-1-b. SOC 여유는 있지만, 이번시간에 잉여전력을 모두 배터리가 감당할 수는 없다.(일부 잉여전력이라도 충전함)

                    P_bc(iter,t) = SOC_max*C_bat-E_bat(iter,t)  # 2-1-b. 배터리 SOC 최대까지만 충전하라

                    if  P_LLP_sum(iter,t) > ((Ppv(iter,t)-(P_HP(iter,t)-Pw(iter,t))/n_inv)*n_BC - P_bc(iter,t)):
                        P_LLP(iter,t) = ((Ppv(iter,t)-(P_HP(iter,t)-Pw(iter,t))/n_inv)*n_BC - P_bc(iter,t))     # 2-1-b. 나머지는 후순위 부하로 공급하라.
                    else:
                        P_LLP(iter,t) =  P_LLP_sum(iter,t)  # 2-1-b. 후순위부하로 공급하고 더미로 갈 용량 체크
                        dummy(iter,t) = (Ppv(iter,t)-(P_HP(iter,t)-Pw(iter,t))/n_inv)*n_BC - P_bc(iter,t) -  P_LLP_sum(iter,t)  # 2-4. 더미부하로 태워라

                P_LLP_sum(iter,t) = P_LLP_sum(iter,t) - P_LLP(iter,t)

                if t == 1:
                       dummy_sum(iter,1) = dummy(iter,1)    # 더미부하 적산
                else:
                       dummy_sum(iter,t) = dummy_sum(iter,t-1) + dummy(iter,t)  # 더미부하 적산

                P_HPL(iter,t) = P_HP(iter,t)    # 우선순위 부하에 공급된 전력량

            else:   # SOC full charge 라면,

                    if  P_LLP_sum(iter,t) > (Ppv(iter,t)-(P_HP(iter,t)-Pw(iter,t))/n_inv):      #  후순위부하가 모두 감당할수 있다면
                        P_LLP(iter,t) = ((Ppv(iter,t)-(P_HP(iter,t)-Pw(iter,t))/n_inv))         # 2-1-b. 나머지는 후순위 부하로 공급하라.
                    else:
                        P_LLP(iter,t) =  P_LLP_sum(iter,t)  # 2-1-b. 후순위부하로 공급하고 더미로 갈 용량 체크
                        dummy(iter,t) =  (Ppv(iter,t)-(P_HP(iter,t)-Pw(iter,t))/n_inv) - P_LLP_sum(iter,t)  # 2-4. 더미부하로 태워라

                    P_LLP_sum(iter,t) = P_LLP_sum(iter,t) - P_LLP(iter,t)

                    if t == 1:
                        dummy_sum(iter,1) = dummy(iter,1)   # 더미부하 적산
                    else:
                       dummy_sum(iter,t) = dummy_sum(iter,t-1) + dummy(iter,t)  # 더미부하 적산

                    P_HPL(iter,t) = P_HP(iter,t)    # 우선순위 부하에 공급된 전력량


        elif (SOC(iter,t) > SOC_min):    # 3. 공급부족인데, 배터리가 방전 가능한가?

            if E_bat(iter,t)*n_BD > (P_HP(iter,t) - Pw(iter,t)-Ppv(iter,t)*n_inv)   # 3-1-a. 배터리 잔량이 부족량을 모두 감당 가능한가?
                P_bd(iter,t) = (P_HP(iter,t) - Pw(iter,t)-Ppv(iter,t)*n_inv)/n_BD   # 그렇다면 모두 감당하라
                P_HPL(iter,t) = P_HP(iter,t)   # 우선순위 부하에 공급된 전력량
            else:
                P_bd(iter,t) = E_bat(iter,t) - C_bat*0.1        # 3-1-b. 아니라면 하한치까지라도 방전하라
                P_HPL(iter,t) = Pw(iter,t) + Ppv(iter,t)*n_inv + P_bd(iter,t)*n_BD  # 우선순위 부하에 공급된 전력량

                if  (P_dgr > (P_HP(iter,t) - Pw(iter,t)-Ppv(iter,t)*n_inv) - P_bd(iter,t)*n_BD):        # 4. 디젤 발전기로 충당 가능하나?
                    P_dg(iter,t) =  P_HP(iter,t) - Pw(iter,t)-Ppv(iter,t)*n_inv - P_bd(iter,t)*n_BD     # 가능하다면 디젤을 운용하라
                    P_HPL(iter,t) = P_HP(iter,t)    # HP 공급완료
                else:
                    LOLP_HP(iter,t) = 1


                    if t == 1:
                       dummy_sum(iter,1) = dummy(iter,1)    # 더미부하 적산
                    else:
                       dummy_sum(iter,t) = dummy_sum(iter,t-1) + dummy(iter,t)  # 더미부하 적산

        else:         #   4. 최후의 수단으로 디젤 운용

            if  (P_dgr > P_HP(iter,t)-Pw(iter,t)-Ppv(iter,t)*n_inv):            # 4. 디젤 발전기로 충당 가능하나?
                P_dg(iter,t) =  P_HP(iter,t)-Pw(iter,t)-Ppv(iter,t)*n_inv       # 가능하다면 디젤을 운용하라
                P_HPL(iter,t) = P_HP(iter,t)                                    # HP 공급완료
            else:
                P_dg(iter,t) = P_dgr                                            # 디젤공급으로도 우선순위부하를 충족해줄수 없다면
                LOLP_HP(iter,t) = 1                                             # LOLP 카운트 +1


                P_LLP_sum(iter,t) = P_LLP_sum(iter,t) - P_LLP(iter,t)

                if t == 1
                       dummy_sum(iter,1) = dummy(iter,1) # 더미부하 적산
                    else
                       dummy_sum(iter,t) = dummy_sum(iter,t-1) + dummy(iter,t) # 더미부하 적산
                end

        end


         E_bat(iter,t+1) = E_bat(iter,t) + P_bc(iter,t)     # 충전
         E_bat(iter,t+1) = E_bat(iter,t+1) - P_bd(iter,t)   # 방전

         E_bat(iter,t+1) = E_bat(iter,t+1)*(1-r_sd)         # 자가방전 0.02 [%]
         SOC(iter,t+1) = E_bat(iter,t+1)/C_bat              # SOC 재계산


# iteration + 1 직전 계산

    if iter < 3: # dx 정밀화

    elif (x(iter,1)-x(iter-1,1))/(x(iter-1,1)-x(iter-2,1)) < 0:

        dx=dx/2

    else:

         if dummy_sum(iter,t) == 0:   # 더미 필요없나?
            x(iter+1,1) = x(iter,1) + dx # 그렇다면 신재생발전원 늘려라
         elif dummy_sum(iter,t)/sum(Pload(iter,:)) > Set_dummy:  # 더미가 총 부하 소모량의 설정값(6%)를 넘는가?
            x(iter+1,1) = x(iter,1) - dx # 그렇다면 신재생발전원 줄여라
         else:

            if P_LLP_sum(iter,t) >= P_LLP_sum_ref:  # 후순위부하 신뢰도는 적정한가?
                x(iter+1,1) = x(iter,1) + dx:       # 아니라면 신재생발전원 늘려라
            else:

                if sum(LOLP_HP(iter,:))/t > Set_LOLP_HP:        # 우선순위 부하 LOLP는 적정한가?
                    x(iter+1,1) = x(iter,1) + dx                # 아니라면 신재생발전원 늘려라
                else:
                     want_iter = iter
                     break

x(iter,2) = dx


# E_bat = E_bat*(1-r_sd)+P_bc(iter,t)*n_BC  # accumulate capacity of battery



# NPPBSG algorithm Check(Text)
disp('           iteration        HP_demand [MWh]         LOLP_HP [%]            LP_demand [MWh]          LP_unmet [%]         Dummy [%]      WP [MWh]       PV [MWh]     DG [MWh]')
disp('          _________________________________________________________________________________________________________________________________________________________________________')

for m=1:want_iter:
    fprintf('             %2d                  %5.2f             %5.2f                          %5.2f             %5.2f             %5.2f           %5.2f        %5.2f       %5.2f \n', m, sum(P_HP(1,:)), 100*sum(LOLP_HP(m,:))/t, sum(P_LP(1,:)),  100*P_LLP_sum(m,t)/P_LLP_sum_ref, 100*dummy_sum(m,t)/sum(Pload(m,:)), sum(Pw(m,:)), sum(Ppv(m,:)), sum(P_dg(m,:)))


# NPPBSG algorithm Check(Graph)

view = want_iter    # 몇 번쨰 iteration 데이터를 그래프로 보고 싶은가?


figure(1)                               # Load plot
subplot(5,1,1)

plot(time,Pload(view,:),'k-o');
hold on
plot(time,P_HP(view,:),'b-*');
grid on

xlabel('time [h]')
ylabel('Load power [MW]')
legend('Pload = P_H_P + P_L_P','P_H_P', 'Orientation', 'horizontal')

xlim([1,n])

bar(time,dummy(view,:),'r')
alpha(0.5)

hold off


subplot(5,1,2)

plot(time,Pw(view,:)+Ppv(view,:),'k-o');
hold on
plot(time,Pw(view,:),'b-*');
hold off
grid on

xlabel('time [h]')
ylabel('Renewable Energy [MW]')
legend('P_w + P_p_v', 'P_w', 'Orientation', 'horizontal')

xlim([1,n])

subplot(5,1,3)

bar(time,P_bc(view,:))
alpha(0.5)
hold on
bar(time,-P_bd(view,:),'r')
grid on

plot(time,E_bat(view,1:n),'k-o');

xlabel('time [h]')
ylabel('Battery Output [MW]')
legend('B_c','B_d', 'Orientation', 'horizontal')

xlim([1,n])

hold off

subplot(5,1,4)

bar(time,P_dg(view,:),'k');
alpha(0.5)
grid on
hold on

xlabel('time [h]')
ylabel('DG Output [MW]')
legend('P_dg', 'Orientation', 'horizontal')

xlim([1,n])

hold off

subplot(5,1,5)



plot(time,P_LLP_sum(view,:),'k-o');
hold on
grid on

xlabel('time [h]')
ylabel('P_L_L_P Output [MW]')
legend('P_L_L_P_s_u_m', 'Orientation', 'horizontal')

xlim([1,n])

hold off




figure(2)

subplot(4,1,1)  # 우선순위부하와 신재생 출력, 배터리 방전을 포함한 신재생 출력 비교(우선순위부하 체크)

plot(time,P_HP(view,:),'b-*');
hold on
plot(time,Ppv(view,:)+Pw(view,:),'k-o');
plot(time,Ppv(view,:)+Pw(view,:)+(P_bd(view,:)*n_BD),'-.rs');
bar(time,dummy(view,:),'r');
alpha(0.5)
grid on

xlabel('time [h]')
ylabel('power [MW]')
legend('P_H_P', 'Ppv+Pw', 'Ppv+Pw+Pbd', 'Orientation', 'horizontal')

xlim([1,n])

hold off

subplot(4,1,2)  # 후순위 부하와 후순위부하 부족량 누적 관계

plot(time,P_LP(view,:),'b-*');
hold on
plot(time,P_LLP_sum(view,:),'-.rs');
grid on
bar(time,P_LLP(view,:));
alpha(0.5)

xlabel('time [h]')
ylabel('power [MW]')
legend('P_L_P', 'P_L_L_P_s_u_m', 'Orientation', 'horizontal')

xlim([1,n])

hold off

subplot(4,1,3)  # 후 순위 부하의 로드시프팅 결과

plot(time,P_LP(view,:),'k-o');
hold on
plot(time,P_LLP(view,:),'r-*');
alpha(0.5)
grid on

xlabel('time [h]')
ylabel('power [MW]')
legend('P_L_P', 'Shift P_L_P', 'Orientation', 'horizontal')

xlim([1,n])

hold off

subplot(4,1,4)  # 로드시프팅 결과


plot(time,P_HP(view,:)+P_LP(view,:),'k-o');
hold on
plot(time,P_HP(view,:)+P_LLP(view,:),'r-*');
alpha(0.5)
grid on

xlabel('time [h]')
ylabel('power [MW]')
legend('Pload', 'Pload_s_h_i_f_t' ,'Orientation', 'horizontal')

xlim([1,n])

hold off

% plot(time,Ppv+Pw+(P_bd*n_BD)-(P_bc*n_BC),'-.rs')