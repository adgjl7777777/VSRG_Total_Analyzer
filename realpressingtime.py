# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 00:32:44 2021

@author: Transcendence
"""
#문제. 처음 몇개를 빼는 식으로 진행해야 될 수도 있음. 
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

info = osrparse.parse_replay_file('normal.osr') #리플레이파일 분해

playtime = 0
whattimeset = [[] for i in range(18)] #언제 키를 눌렀다 뗐나?
realpressset = [[] for i in range(18)] #키를 몇ms동안 눌렀다 뗐나?
fakepressset = [[] for i in range(18)] #150ms 이상일 땐 제거
onset = np.zeros(18) #시간대 바로 전의 키를 누를 때의 정보 저장
timeset = np.zeros(18) #총 키를 누른 시간 정보 저장

for i, j in enumerate(info.play_data): # 각 키가 누른 시간 구하기
    if j.time_delta == 0 or i < 3 :
        continue
    playtime += j.time_delta
    print(playtime)
    r_onset=divider(j.keys)
    timeset += onset*j.time_delta
    for k,l in enumerate(r_onset):
        if onset[k] != 0 and l == 0:
            realpressset[k].append(int(timeset[k]))
            fakepressset[k].append(int(min(150,timeset[k])))
            timeset[k] = 0
            whattimeset[k].append(int(playtime))
    onset = r_onset


plt.figure(figsize=(5,3))
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



"""
import requests
import hashlib
keyset = {KeyMania.0 : 0, KeyMania.K1 : 1, KeyMania.K2 : 2, KeyMania.K3 : 3, KeyMania.K4 : 4,
          KeyMania.K5 : 5, KeyMania.K6 : 6, KeyMania.K7 : 7, KeyMania.K8 : 8, KeyMania.K9 : 9,
          KeyMania.K10 : 10, KeyMania.K11 : 11, KeyMania.K12 : 12, KeyMania.K13 : 13, KeyMania.K14 : 14,
          KeyMania.K15 : 15, KeyMania.K16 : 16, KeyMania.K17 : 17, KeyMania.K18 : 18}
"""
"""
print(info.replay_hash)
original = str(info.max_combo)+'osu'+info.player_name+info.beatmap_hash+str(info.score)+str(None)
enc=hashlib.md5()
enc.update(original.encode('utf-8'))
enctext=enc.hexdigest()
print(enctext)
"""
"""
url = 'https://osu.ppy.sh/api/get_beatmaps'
api_f = open('api.txt','r')
api = api_f.readline()
params = {'k' : api, 'h' : 'c63c10215988e8222d7a1b8db48d7192'}
res = requests.get(url=url, params=params)

realbeatmap = res.json()[0]
print(realbeatmap)
"""