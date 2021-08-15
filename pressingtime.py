# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 00:32:44 2021

@author: Transcendence
"""

import osrparse
import numpy as np
from matplotlib import pyplot as plt
from basictool import key_finder

info = osrparse.parse_replay_file('sample.osr') #read replay file

onset = np.zeros(18) #infornation about previous key pressing
timeset = np.zeros(18) #milisecond time that keyboard pressed
pressset = [[] for i in range(18)] # save all data of timeset

for i, j in enumerate(info.play_data): # get infornation about key pressing time
    if j(j.time_delta == 0 and j.keys == 0) or i < 3 : #there are dummy replay whose timing is zero. We should remove this. and, I deleted first three data because thet data does not indicate real press time.
        continue
    r_onset=key_finder.findkey(j.keys) #infornation about "Present" key pressing
    timeset += onset*j.time_delta
    for k,l in enumerate(r_onset):
        if onset[k] != 0 and l == 0:
            pressset[k].append(int(timeset[k]))
            timeset[k] = 0
    onset = r_onset

#making plot
basetime = [] #press time
presstime = [] #press count

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
for i in range(len(basetime)):
    plt.plot(basetime[i], presstime[i], label= 'key '+str(i+1))
plt.grid()
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlim(0,150)
plt.xlabel('pressing time(ms)',fontsize=15)
plt.ylabel(r'count',fontsize=15) 
plt.legend(shadow=True, fontsize=10, ncol=1)
plt.tight_layout()
plt.show

