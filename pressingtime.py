# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 00:32:44 2021

@author: Transcendence
"""

import osrparse
import numpy as np
from matplotlib import pyplot as plt

def divider(x = 0): #그 시간대에 어떤 키를 눌렀나 보는 함수
    keyset = [0 for i in range(18)]
    (a, keyset[0]) = (x//2, x%2)
    j = 1
    while a != 0:
        (a, keyset[j]) = (a//2, a%2)
        j += 1
    return np.array(keyset)

info = osrparse.parse_replay_file('sample.osr') #리플레이파일 분해

playtime = -1
pressset = [[] for i in range(18)]
onset = np.zeros(18)
timeset = np.zeros(18)

for i, j in enumerate(info.play_data): # 각 키가 누른 시간 구하기
    if j.time_delta == 0 or i < 2 :
        continue
    r_onset=divider(j.keys)
    timeset += onset*j.time_delta
    for k,l in enumerate(r_onset):
        if onset[k] != 0 and l == 0:
            pressset[k].append(int(timeset[k]))
            timeset[k] = 0
    onset = r_onset

basetime = []
presstime = []

for i in pressset: # 시간에 따른 각 키 누른 횟수 계산
    if i != []:
        presstime.append([])
        basetime.append([])
        maxpress = max(i)
        basetime[-1] = np.linspace(0, maxpress, maxpress+1)
        presstime[-1] = np.zeros(maxpress+1)
        for j in i:
            presstime[-1][j] += 1
for i in range(len(basetime)):
    plt.plot(basetime[i], presstime[i], label= "key "+str(i+1))
plt.grid()
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(0,150)
plt.xlabel('pressing time(ms)',fontsize=15)
plt.ylabel(r'count',fontsize=15)
plt.legend(shadow=True, fontsize=10, ncol=1)
plt.tight_layout()
plt.show