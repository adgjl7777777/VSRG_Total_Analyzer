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

playtime = 0
whattimeset = [[] for i in range(18)] #언제 키를 눌렀다 뗐나?
realpressset = [[] for i in range(18)] #키를 몇ms동안 눌렀다 뗐나?
fakepressset = [[] for i in range(18)] #150ms 이상일 땐 제거
onset = np.zeros(18) #시간대 바로 전의 키를 누를 때의 정보 저장
timeset = np.zeros(18) #총 키를 누른 시간 정보 저장

for i, j in enumerate(info.play_data): # 각 키가 누른 시간 구하기
    playtime += j.time_delta
    if j.time_delta == 0 or i < 2 :
        continue
    r_onset=divider(j.keys)
    timeset += onset*j.time_delta
    for k,l in enumerate(r_onset):
        if onset[k] != 0 and l == 0:
            realpressset[k].append(int(timeset[k]))
            fakepressset[k].append(int(min(150,timeset[k])))
            timeset[k] = 0
            whattimeset[k].append(int(playtime))
    onset = r_onset


plt.figure(figsize=(50,3))
for i in range(18):
    if whattimeset[i] != []:
        plt.plot(whattimeset[i], fakepressset[i], label= "key "+str(i+1))
plt.grid()
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylim(0,150)
plt.xlabel('play time(ms)',fontsize=15)
plt.ylabel('pressing time(ms)',fontsize=15)
plt.legend(shadow=True, fontsize=10, ncol=1)
plt.tight_layout()
plt.show