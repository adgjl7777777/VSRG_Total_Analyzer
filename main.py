#%% coding information
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 00:32:44 2021

This is for osu! mania analyzing
@author: Transcendence
"""
#%% import
import osrparse
import binascii

import numpy as np
import math
from os import mkdir
from os.path import isdir
from glob import glob
from scipy.stats import mode
from scipy.interpolate import CubicSpline
from matplotlib import font_manager, rc
from graph import *
from base import *
#%% total setting
#font_path = "../NotoSansCJKkr-Regular.otf"
#font = font_manager.FontProperties(fname=font_path).get_name()
#rc('font', family=font, size=10)
MAX_SHOWTIME = 160
KPS_INTERVAL = 1000
CHECK_INTERVAL = 2
DPI = 300
INTERVAL_CRITERIA = 100
ERROR_CRITERIA = 10

#%% info, keyc, mode_1 / basetime, presstime
def press_analyze(info, keyc, mode_1):
    
    onset = np.zeros(keyc) #infornation about previous key pressing
    timeset = np.zeros(keyc) #milisecond time that keyboard pressed
    pressset = [[] for i in range(keyc)] # save all data of timeset
    basetime = [] #press time
    presstime = [] #press count
    corrector = dt_ht_finder(info)
    
    if mode_1 == 0:
        for i, j in enumerate(info.replay_data): # get infornation about key pressing time
            if (j.time_delta == 0 and j.keys == 0) or i < 3 : #there are dummy replay whose timing is zero. We should remove this. and, I deleted first three data because thet data does not indicate real press time.
                continue
            r_onset = find_ind_key(j.keys, keyc) #infornation about "Present" key pressing
            timeset += onset*j.time_delta
            for k,l in enumerate(r_onset):
                if onset[k] != 0 and l == 0:
                    pressset[k].append(int(timeset[k]))
                    timeset[k] = 0
            onset = r_onset
            
    elif mode_1 == 1:
        for i, j in enumerate(info.replay_data): # get infornation about key pressing time
            if (j.time_delta == 0 and j.keys == 0) or i < 3 : #there are dummy replay whose timing is zero. We should remove this. and, I deleted first three data because thet data does not indicate real press time.
                continue
            r_onset = 1-find_ind_key(j.keys, keyc) #infornation about "Present" key pressing
            timeset += onset*j.time_delta
            for k,l in enumerate(r_onset):
                if onset[k] == 0 and l != 0:
                    pressset[k].append(int(timeset[k]))
                    timeset[k] = 0
            onset = r_onset
        
    for i in pressset: # press count vs press time
        if i != []:
            presstime.append([])
            basetime.append([])
            maxpress = max(i)
            basetime[-1] = np.linspace(0, max(math.ceil((MAX_SHOWTIME+CHECK_INTERVAL)/corrector), maxpress), max(math.ceil((MAX_SHOWTIME+CHECK_INTERVAL)/corrector), maxpress)+1)
            presstime[-1] = np.zeros(max(math.ceil((MAX_SHOWTIME+CHECK_INTERVAL)/corrector), maxpress)+1)
            for j in i:
                if j >=0:
                    presstime[-1][j] += 1
                    
    for i in basetime:
        i *=corrector
        
    return basetime, presstime, corrector
#%% info, keyc, mode_1 / whattimeset, pressset
def realtime_press_analyze(info, keyc, mode_1):
    
    playtime = 0
    onset = np.zeros(keyc) #infornation about previous key pressing
    timeset = np.zeros(keyc) #milisecond time that keyboard pressed
    whattimeset = [[] for i in range(keyc)] #when you pressed keys
    pressset = [[] for i in range(keyc)] #milisecond time that keyboard pressed
    corrector = dt_ht_finder(info)
    maxtime = 0
    
    if mode_1 == 2:
        for i, j in enumerate(info.replay_data): # get infornation about key pressing time
            if (j.time_delta == 0 and j.keys == 0) or i < 3 : #there are dummy replay whose timing is zero. We should remove this. and, I deleted first three data because thet data does not indicate real press time.
                continue
            playtime += j.time_delta
            r_onset=find_ind_key(j.keys, keyc) #infornation about "Present" key pressing
            timeset += onset*j.time_delta
            for k,l in enumerate(r_onset):
                if onset[k] != 0 and l == 0:
                    pressset[k].append(int(timeset[k]))
                    timeset[k] = 0
                    whattimeset[k].append(int(playtime))
            onset = r_onset
    
    elif mode_1 == 3:
        for i, j in enumerate(info.replay_data): # get infornation about key pressing time
            if (j.time_delta == 0 and j.keys == 0) or i < 3 : #there are dummy replay whose timing is zero. We should remove this. and, I deleted first three data because thet data does not indicate real press time.
                continue
            playtime += j.time_delta
            r_onset=1-find_ind_key(j.keys, keyc) #infornation about "Present" key pressing
            timeset += onset*j.time_delta
            for k,l in enumerate(r_onset):
                if onset[k] == 0 and l != 0:
                    pressset[k].append(int(timeset[k]))
                    timeset[k] = 0
                    whattimeset[k].append(int(playtime))
            onset = r_onset        
    
    for i in range(len(whattimeset)):
        if whattimeset[i] != []:
            whattimeset[i] = np.array(whattimeset[i])/1000*corrector
            maxtime = max(maxtime,max(whattimeset[i]))
            keyc +=1
            
    for i in range(len(pressset)):
        if pressset[i] != []:
            pressset[i] = np.array(pressset[i])*corrector
    
    return whattimeset, pressset, corrector, maxtime
#%%
def kps_analyze(info, keyc, mode_1):
    playtime = 0
    whattimeset = [[] for i in range(keyc)] 
    onset = np.zeros(keyc)
    maxtime = 0
    mintime = 0
    corrector = dt_ht_finder(info)
    for i, j in enumerate(info.replay_data):
        if j.time_delta == 0 or i < 3 :
            continue
        playtime += j.time_delta
        r_onset=find_ind_key(j.keys, keyc)
        for k,l in enumerate(r_onset):
            if onset[k] == 0 and l != 0:
                whattimeset[k].append(int(playtime))
                maxtime = max(maxtime, int(playtime))
                mintime = min(mintime, int(playtime))
        onset = r_onset
    interval = KPS_INTERVAL
            
    kpsset = [np.zeros(abs(mintime)+maxtime+interval+1) for i in range(keyc)] #kps 측정 장치
    timeset = np.linspace(mintime, maxtime+interval, abs(mintime)+maxtime+interval+1)
    for i in range(keyc):
        for j in whattimeset[i]:
            for k in range(interval):
                kpsset[i][j+abs(mintime)+k] += 1
            
    totalkpsset = np.zeros(abs(mintime)+maxtime+interval+1)
    for i in kpsset:
        totalkpsset += i
    return timeset, kpsset, corrector, maxtime
#%%
def zero_finder(info, keyc, mode_1):
    playtime = 0
    timeset = []
    zeroset = []
    corrector = dt_ht_finder(info)
    for i, j in enumerate(info.replay_data): # 각 키가 누른 시간 구하기
        if i < 3 :
            continue
        elif j.time_delta == 0:
            timeset.append(playtime)
            zeroset.append(1)
        else:
            playtime += j.time_delta*corrector
            timeset.append(playtime)
            zeroset.append(0)
            
    return timeset, zeroset, corrector, timeset[-1]
    

#%%
def findsong(info, totf = 0x00):
    mysong = info.beatmap_hash
    print(mysong)
    myloc = 0;
    truemyloc = 0;
    myinfo = "";
    if totf != 0x00:
        for i in range(len(totf)-len(mysong)):
            print(totf[i:i+len(mysong)])
            if mysong ==totf[i:i+len(mysong)]:
                myloc = i+len(mysong)+1;
                truemyloc = myloc
                break
        while (myloc - truemyloc) <1000:
            myinfo += totf[myloc]
            if myinfo[-4:] == ".osu":
                break
            myloc += 1
        return myinfo
    else:
        return ""
#%%
def presssaver(mapdir, mode_1 = 0, was = 0x00):
    
    info = osrparse.Replay.from_path(mapdir) #read replay file
    print(info.username)
    keyc=find_tot_key(info)
    """
    totf = findsong(info, was)
    """
    totf = ""
    if mode_1 < 2: #normal
        x_results, y_results, corrector = press_analyze(info, keyc, mode_1)
        press_draw(mapdir, keyc, info, corrector, x_results, y_results, mode_1, totf)
        
    elif mode_1 < 4: #time 
        x_results, y_results, corrector, maxtime = realtime_press_analyze(info, keyc, mode_1)
        realtime_press_draw(mapdir, keyc, info, corrector, x_results, y_results, maxtime, mode_1)
    elif mode_1 == 4: #kps
        x_results, y_results, corrector, maxtime = kps_analyze(info, keyc, mode_1)
        #toty = y_results[0]
        #for i in range(1,keyc):
        #    toty += y_results[i]
        kps_press_draw(mapdir, keyc, info, corrector, x_results, y_results, maxtime, mode_1, totf)
    elif mode_1 == 5: #zero
        x_results, y_results, corrector, maxtime = zero_finder(info, keyc, mode_1)
        zero_press_draw(mapdir, keyc, info, corrector, x_results, y_results, maxtime, mode_1, totf)
    elif mode_1 == 6:
        x_results, y_results, corrector = press_analyze(info, keyc, 0)
        x2, y2 = tot_smoother_function(x_results, y_results, keyc, corrector)
        press_draw(mapdir, keyc, info, corrector, x2, y2, mode_1, totf)
        
        
#%%
totf = open("D:\osu\osu!.db","rb")

osudb = totf.read()
totf.close()
osudb = binascii.b2a_hex(osudb)

if not isdir("./osr files"):
    mkdir("./osr files")
for i in range(7):
    if not isdir(f"./graph results {i}"):
        mkdir(f"./graph results {i}")
all_dir = glob('./osr files/*.osr')
print(all_dir)
a = []
for i in all_dir:
    a.append(presssaver(i, mode_1=0, was = osudb))