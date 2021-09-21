# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 00:32:44 2021

@author: Transcendence
"""

import osrparse
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import os
import glob

def findkey(x = 0):
    keyset = [0 for i in range(18)]
    (a, keyset[0]) = (x//2, x%2)
    j = 1
    while a != 0:
        (a, keyset[j]) = (a//2, a%2)
        j += 1
    return np.array(keyset)

def presssaver(mapdir):
    info = osrparse.parse_replay_file(mapdir+'.osr') #read replay file
    print(info.player_name)
    onset = np.zeros(18) #infornation about previous key pressing
    timeset = np.zeros(18) #milisecond time that keyboard pressed
    pressset = [[] for i in range(18)] # save all data of timeset
    
    for i, j in enumerate(info.play_data): # get infornation about key pressing time
        if (j.time_delta == 0 and j.keys == 0) or i < 3 : #there are dummy replay whose timing is zero. We should remove this. and, I deleted first three data because thet data does not indicate real press time.
            continue
        r_onset=findkey(j.keys) #infornation about "Present" key pressing
        timeset += onset*j.time_delta
        for k,l in enumerate(r_onset):
            if onset[k] != 0 and l == 0:
                pressset[k].append(int(timeset[k]))
                timeset[k] = 0
        onset = r_onset
    
    #making plot
    basetime = [] #press time
    presstime = [] #press count
    bin(info.mod_combination)

    corrector = 1
    if info.mod_combination == 0:
        pass
    elif (bin(info.mod_combination)[2:].zfill(32))[-7] =='1':
        corrector = 2/3
    elif (bin(info.mod_combination)[2:].zfill(32))[-9] =='1':
        corrector = 4/3    
    
    for i in pressset: # press count vs press time
        if i != []:
            presstime.append([])
            basetime.append([])
            maxpress = max(i)
            basetime[-1] = np.linspace(0, maxpress, maxpress+1)
            presstime[-1] = np.zeros(maxpress+1)
            for j in i:
                if j >=0:
                    presstime[-1][j] += 1
    for i in basetime:
        i *=corrector
    keyc = len(basetime)
    for i in range(len(basetime)):
        rgbcolor = colors.hsv_to_rgb((i/keyc,1,1))*255
        colorst = "#"+hex(int(rgbcolor[0]))[2:].zfill(2)+hex(int(rgbcolor[1]))[2:].zfill(2)+hex(int(rgbcolor[2]))[2:].zfill(2)
        plt.plot(basetime[i], presstime[i], label= 'key '+str(i+1), color = colorst)
    pressacc = '320='+str(info.gekis)+', 300='+str(info.number_300s)+'\n200='+str(info.katus)+', 100='+str(info.number_100s)+'\n50='+str(info.number_50s)+', 0='+str(info.misses)
    plt.grid()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlim(0,160)
    plt.xlabel('pressing time(ms)',fontsize=15)
    plt.ylabel(r'count',fontsize=15)
    plt.legend(shadow=True, fontsize=10, ncol=2)
    plt.text(0.5, 0.5, str(osrparse.Mod(info.mod_combination))[4:].replace("|","\n")+"\nscores="+str(info.score), va='bottom')
    plt.text(159.5, 0.5, pressacc+"\nRI="+format(corrector,"0.2f"), ha='right', va='bottom')
    plt.title(mapdir[10:]+"\n,"+info.player_name+","+str(info.timestamp))
    plt.tight_layout()
    plt.savefig("graph results/"+mapdir[10:])
    plt.clf()
if not os.path.isdir("osr files"):
    os.mkdir("osr files")
if not os.path.isdir("graph results"):
    os.mkdir("graph results")
all_dir = glob.glob('osr files/*.osr')  
for i in all_dir:
    presssaver(i[:-4])