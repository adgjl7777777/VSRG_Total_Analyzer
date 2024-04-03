# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 01:59:20 2022

@author: user
"""
import numpy as np
import math
MAX_SHOWTIME = 160
KPS_INTERVAL = 1000
CHECK_INTERVAL = 2
INTERVAL_CRITERIA = 100
from scipy.stats import mode
from scipy.interpolate import CubicSpline
ERROR_CRITERIA = 20
#%% x / np.array(keyset)
def find_ind_key(x = 0, keyc = 18):
    """
    find the place the player pressed
    """
    keyset = [0 for i in range(keyc)]
    (a, keyset[0]) = (x//2, x%2)
    j = 1
    
    while a != 0:
        (a, keyset[j]) = (a//2, a%2)
        j += 1
        
    return np.array(keyset)
#%% info / keyc
def find_tot_key(info):
    
    """
    find total key of the map
    """
    keyfindset = np.zeros(18) #find keys
    
    for i,j in enumerate(info.replay_data):
        if (j.time_delta == 0 and j.keys == 0) or i < 3:
            continue
        keyfindset += find_ind_key(j.keys)
        
    return 18-list(keyfindset).count(0)
#%% info / corrector
def dt_ht_finder(info):
    
    bin(info.mods)
    corrector = 1
    
    if info.mods == 0:
        pass
    
    elif (bin(info.mods)[2:].zfill(32))[-7] =='1':
        corrector = 2/3
        
    elif (bin(info.mods)[2:].zfill(32))[-9] =='1':
        corrector = 4/3 
        
    return corrector
#%%
def tot_smoother_function(x_results, y_results, keyc, corrector):
    """
    주기 계산을 위해 합치기
    """
    wholeset = set(np.linspace(0,math.ceil((MAX_SHOWTIME+CHECK_INTERVAL)/corrector),math.ceil((MAX_SHOWTIME+CHECK_INTERVAL)/corrector))*corrector)
    for i in x_results:
        wholeset |= set(i)
    wholelist = list(wholeset)
    wholelist.sort()
    wholedict = dict.fromkeys(wholelist,0)
    for i in range(keyc):
        for j in range(len(x_results[i])):
            wholedict[x_results[i][j]]+=y_results[i][j]
    x_list = list(wholedict.keys())
    y_list = list(wholedict.values())
    local_maximum = []
    """
    극대값 찾기
    """
    for i in range(1,math.ceil(MAX_SHOWTIME/corrector)+1):
        if max(y_list[max(0,(i-CHECK_INTERVAL)):(i+CHECK_INTERVAL+1)]) == y_list[i] and y_list[i] != 0:
            local_maximum.append(x_list[i])
    local_diff = [local_maximum[i+1]-local_maximum[i] for i in range(len(local_maximum)-1)]
    local_diff = [local_maximum[0]]+local_diff
    total_mode = mode(local_diff)[0][0]
    real_local_maximum = []
    before_i = 0
    period_error = 0
    """
    최빈값을 이용해 실제 주기에 속하는 값들 찾기
    """
    if local_maximum[0] > total_mode:
        real_local_maximum.append(local_maximum[0])
        base_diff = [0, 0]
        used_checker = True
    else:
        base_diff = [local_maximum[0], local_maximum[0]]
        used_checker = False
    for i in range(1,len(local_maximum)):
        base_diff[1] += local_diff[i]
        if base_diff[1] <= total_mode:
            base_diff[0] = base_diff[1]
            used_checker = False
            before_i = i
        else:
            if used_checker:
                real_local_maximum.append(local_maximum[i])
                if local_maximum[i] <= INTERVAL_CRITERIA:
                    period_error += base_diff[1] / total_mode
                base_diff = [0, 0]
            else:
                if base_diff[0] < total_mode-corrector*2 and base_diff[1] < total_mode+corrector*3:
                    real_local_maximum.append(local_maximum[i])
                    base_diff = [0, 0]
                    used_checker = True
                elif base_diff[0] > total_mode-corrector*3 and base_diff[1] > total_mode+corrector*2:
                    real_local_maximum.append(local_maximum[before_i])
                    if local_diff[i] > total_mode:
                        real_local_maximum.append(local_maximum[i])
                        if local_maximum[i] <= INTERVAL_CRITERIA and local_diff[i] > total_mode + corrector*2:
                            period_error += base_diff[1] / total_mode
                        base_diff = [0, 0]
                        used_checker = True
                    else:
                        base_diff = [local_diff[i], local_diff[i]]
                        before_i = i
                else:
                    if y_list[x_list.index(local_maximum[before_i])] >= y_list[x_list.index(local_maximum[i])]:
                        real_local_maximum.append(local_maximum[before_i])
                        if local_diff[i] > total_mode:
                            real_local_maximum.append(local_maximum[i])
                            if local_maximum[i] <= INTERVAL_CRITERIA and local_diff[i] > total_mode + corrector*2:
                                period_error += base_diff[1] / total_mode
                            base_diff = [0, 0]
                            used_checker = True
                        else:
                            base_diff = [local_diff[i], local_diff[i]]
                            before_i = i
                    else:
                        real_local_maximum.append(local_maximum[i])
                        base_diff = [0, 0]
                        used_checker = True
    """
    에러가 너무 크면 스무스펑션으로 넘기고, 아니면 비워진 피크 채워주기
    """
    if period_error > ERROR_CRITERIA or total_mode <= corrector*2:
        accurate_peak = 0
        anne_finder = 0
        real_local_maximum = np.array([0,1,2,3,4,5,15,35,55,75,95,115,135,155,175,195,215,235,255,275]) * corrector
        negative_peak = np.array([5,25,45,65,85,105,125,145,165,185,205,225,245,265]) * corrector
        positive_peak = np.array([15,35,55,75,95,115,135,155,175,195,215,235,255,275]) * corrector
        for i in negative_peak:
            min_diff = 1000000
            for j in range(len(x_list)):
                if abs(x_list[j]-i) <min_diff:
                    accurate_peak = j
                    min_diff = abs(x_list[j]-i)
            if y_list[accurate_peak] <= 5:
                anne_finder +=1
        accurate_peak = 0
        for i in positive_peak:
            min_diff = 1000000
            for j in range(len(x_list)):
                if abs(x_list[j]-i) <min_diff:
                    accurate_peak = j
                    min_diff = abs(x_list[j]-i)
            if y_list[accurate_peak] > 5:
                anne_finder +=1
        if anne_finder <= 15:
            return small_smoother_function(x_results, y_results, keyc, corrector)
    else:
        real_local_maximum = [i for i in real_local_maximum if i >5]
        if not 0 in real_local_maximum:
            real_local_maximum = (np.array([0,1,2,3,4,5]) * corrector).tolist()+ real_local_maximum
        last_period = 0
        while (True):
            put_period = last_period
            dummy_period = real_local_maximum[last_period] + total_mode
            min_diff = 1000000
            for i in range(len(real_local_maximum)):
                if abs(real_local_maximum[i] - dummy_period) < min_diff:
                    min_diff = abs(real_local_maximum[i] - dummy_period)
                    last_period = i
            for i in range(len(real_local_maximum)):
                if real_local_maximum[i] > dummy_period:
                    put_period = i
                    break
                put_period = len(real_local_maximum)
            if min_diff > 2*corrector and dummy_period<=MAX_SHOWTIME:
                real_local_maximum = real_local_maximum[:put_period]+[dummy_period]+real_local_maximum[put_period:]
            if dummy_period>MAX_SHOWTIME:
                break
        end_period = 0
        for i in x_list:
            if i >= MAX_SHOWTIME:
                end_period = i
                break
        if not end_period in real_local_maximum:
            real_local_maximum += [end_period]
    """
    스플라인 보간법
    """
    smooth_x_list = [np.array(real_local_maximum) for i in range(keyc)]
    smooth_y_list = [np.zeros(len(real_local_maximum)) for i in range(keyc)]
    real_smooth_x_list = [np.linspace(0, MAX_SHOWTIME+1, 10*(MAX_SHOWTIME+1)+1) for i in range(keyc)]
    real_smooth_y_list = [np.zeros(10*(MAX_SHOWTIME+1)+1) for i in range(keyc)]
    interval_x_list = [(real_local_maximum[i]+real_local_maximum[i+1])/2 for i in range(len(real_local_maximum)-1)]
    for i in range(keyc):
        contain_x = 0
        for j in range(len(x_results[i])):
            if x_results[i][j] < interval_x_list[contain_x]:
                smooth_y_list[i][contain_x]+=y_results[i][j]
            elif x_results[i][j] == interval_x_list[contain_x]:
                smooth_y_list[i][contain_x]+=y_results[i][j]/2
                contain_x += 1
                smooth_y_list[i][contain_x]+=y_results[i][j]/2
                if contain_x == len(interval_x_list)-1:
                    break
            else:
                contain_x += 1
                if contain_x == len(interval_x_list)-1:
                    break
                smooth_y_list[i][contain_x]+=y_results[i][j]
                
        print(smooth_x_list)
        spline_func = CubicSpline(smooth_x_list[i], smooth_y_list[i])
        real_smooth_y_list[i] = spline_func(real_smooth_x_list[i]) / total_mode
    return real_smooth_x_list, real_smooth_y_list
#%%
def small_smoother_function(x_results, y_results, keyc, corrector):
    tot_smooth_y_list = []
    tot_smooth_x_list = []
    for i in range(len(y_results)):
        hidden_y_list = [0] + y_results[i]
        smooth_x_list = x_results[i][:math.ceil(MAX_SHOWTIME/corrector)]
        smooth_y_list = [(hidden_y_list[i]+2*hidden_y_list[i+1]+hidden_y_list[i+2])/4 for i in range(math.ceil(MAX_SHOWTIME/corrector))]
        tot_smooth_x_list.append(np.array(smooth_x_list))
        tot_smooth_y_list.append(np.array(smooth_y_list))
    return tot_smooth_x_list, tot_smooth_y_list
def gradiant_finder(x_list, y_list):
    return x_list, np.gradient(y_list)

def kth_smallest(arr, K):
    """숫자 배열에서 K번째로 작은 값을 구한다.

    이 함수는 고유한 값을 대상으로 한다.
    가령 [2, 1, 1]에서 2번째로 작은 값은 1이 아닌 2이다.

    또한 K가 배열의 고유한 값들의 개수보다 크면 IndexError를 반환한다.

    :input:
      arr | list := 숫자 배열
      K   | int  := 1 이상의 정수를 대상으로 한다.

    :return:
      int := 배열에서 K번째로 작은 값
    """
    # 예외 처리: K는 배열의 고유한 값 개수보다 클 수 없다.
    ORDINAL_MSG = ('st', 'nd', 'rd')[K-1] if K <= 3 else 'th'
    if len(arr) < K:
        raise IndexError(f"There's no {K}{ORDINAL_MSG} value in array")
    elif K <= 0 or not arr:
        raise ValueError("K should be over 0 and arr should not be empty")


    # 상수 및 변수 선언
    INF = float('inf')
    memory = [INF] * K


    # 실제 검색 연산
    for n in arr:
        if n > memory[-1]:
            continue

        for i, m in enumerate(memory):
            if (i == 0 and n <= m) or memory[i-1] <= n <= m:
                for j in range(len(memory)-2, i-1, -1):
                    memory[j+1] = memory[j]
                memory[i] = n
                break

    return memory[-1]
def graph_fft(x_list, y_list):
    return x_list, np.fft.fft(y_list)
def small_filter(x_list, y_list, criteria = 0.4):
    basecount = kth_smallest(y_list[0:MAX_SHOWTIME], int(MAX_SHOWTIME*criteria))
    filter_arr = np.array(y_list) > 0
    outy_map = map(int, filter_arr)
    outy_list = list(outy_map)
    return x_list, outy_list