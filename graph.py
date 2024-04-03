# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 01:31:31 2022

@author: Transcendence
"""

import osrparse
from matplotlib import pyplot as plt
from matplotlib import colors

MAX_SHOWTIME = 160
DPI = 300

#%% mapdir, keyc, info, corrector, x_results, y_results, mode_1
def press_draw(mapdir, keyc, info, corrector, x_results, y_results, mode_1, totf):
    for i in range(keyc):
        rgbcolor = colors.hsv_to_rgb((i/keyc,1,1))*255
        colorst = "#"+hex(int(rgbcolor[0]))[2:].zfill(2)+hex(int(rgbcolor[1]))[2:].zfill(2)+hex(int(rgbcolor[2]))[2:].zfill(2)
        plt.plot(x_results[i], y_results[i], label= 'key '+str(i+1), color = colorst)
    
    pressacc = '320='+str(info.count_geki)+', 300='+str(info.count_300)+'\n200='+str(info.count_katu)+', 100='+str(info.count_100)+'\n50='+str(info.count_50)+', 0='+str(info.count_miss)
    plt.grid()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlim(0,MAX_SHOWTIME)
    plt.xlabel('pressing time(ms)',fontsize=15)
    plt.ylabel(r'count',fontsize=15)
    plt.legend(fontsize=10, ncol=2, fancybox=True, framealpha=0.7)
    plt.text(0.5, 0.5, str(osrparse.Mod(info.mods))[4:].replace("|","\n")+"\nscores="+str(info.score), va='bottom')
    plt.text(MAX_SHOWTIME, 0.5, pressacc+"\nRI="+format(corrector,"0.2f"), ha='right', va='bottom')
    plt.title(info.username+","+str(info.timestamp))
    plt.suptitle(mapdir[13:-4]+"\n"+totf,fontsize=5, ha='left', x = 0.03, y = 0.97)
    plt.tight_layout()
    plt.savefig(f"../graph results {mode_1}/"+info.username+"_"+str(info.timestamp).replace(':',';').replace('.',';')+"_"+mapdir[13:-4].replace('.',','),dpi=DPI)
    plt.clf()
#%% mapdir, keyc, info, corrector, x_results, y_results, maxtime, mode_1
def realtime_press_draw(mapdir, keyc, info, corrector, x_results, y_results, maxtime, mode_1, totf):
    for i in range(keyc):
        rgbcolor = colors.hsv_to_rgb((i/keyc,1,1))*255
        colorst = "#"+hex(int(rgbcolor[0]))[2:].zfill(2)+hex(int(rgbcolor[1]))[2:].zfill(2)+hex(int(rgbcolor[2]))[2:].zfill(2)
        plt.plot(x_results[i], y_results[i], label= 'key '+str(i+1), color = colorst)
    
    
    pressacc = '320='+str(info.count_geki)+', 300='+str(info.count_300)+'\n200='+str(info.count_katu)+', 100='+str(info.count_100)+'\n50='+str(info.count_50)+', 0='+str(info.count_miss)
    plt.grid()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylim(0,MAX_SHOWTIME)
    plt.xlim(0,maxtime)
    plt.xlabel('play time(s)',fontsize=15)
    plt.ylabel(r'pressing time(ms)',fontsize=15)
    plt.legend(fontsize=10, ncol=2, fancybox=True, framealpha=0.7)
    plt.text(maxtime*0.5/MAX_SHOWTIME, 0.5, str(osrparse.Mod(info.mods))[4:].replace("|","\n")+"\nscores="+str(info.score), va='bottom')
    plt.text(maxtime*(MAX_SHOWTIME-0.5)/MAX_SHOWTIME, 0.5, pressacc+"\nRI="+format(corrector,"0.2f"), ha='right', va='bottom')
    plt.title(info.username+","+str(info.timestamp),fontsize=15)
    plt.suptitle(mapdir[13:]+"\n"+totf,fontsize=5, ha='left', x = 0.03, y = 0.97)
    plt.tight_layout()
    plt.savefig(f"../graph results {mode_1}/"+mapdir[13:].replace('.',','),dpi=300)
    plt.clf()
#%% mapdir, keyc, info, corrector, x_results, y_results, maxtime, mode_1
def kps_press_draw(mapdir, keyc, info, corrector, x_results, y_results, maxtime, mode_1, totf):
    for i in range(keyc):
        rgbcolor = colors.hsv_to_rgb((i/keyc,1,1))*255
        colorst = "#"+hex(int(rgbcolor[0]))[2:].zfill(2)+hex(int(rgbcolor[1]))[2:].zfill(2)+hex(int(rgbcolor[2]))[2:].zfill(2)
        plt.plot(x_results, y_results[i], label= 'key '+str(i+1), color = colorst)
    
    
    pressacc = '320='+str(info.count_geki)+', 300='+str(info.count_300)+'\n200='+str(info.count_katu)+', 100='+str(info.count_100)+'\n50='+str(info.count_50)+', 0='+str(info.count_miss)
    plt.grid()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlim(0,maxtime)
    plt.xlabel('play time(s)',fontsize=15)
    plt.ylabel(r'pressing time(ms)',fontsize=15)
    #plt.text(maxtime*0.5/MAX_SHOWTIME, 0.5, str(osrparse.Mod(info.mods))[4:].replace("|","\n")+"\nscores="+str(info.score), va='bottom')
    #plt.text(maxtime*(MAX_SHOWTIME-0.5)/MAX_SHOWTIME, 0.5, pressacc+"\nRI="+format(corrector,"0.2f"), ha='right', va='bottom')
    plt.title(info.username+","+str(info.timestamp),fontsize=15)
    plt.suptitle(mapdir[13:]+"\n"+totf,fontsize=5, ha='left', x = 0.03, y = 0.97)
    plt.tight_layout()
    plt.savefig(f"../graph results {mode_1}/"+mapdir[13:].replace('.',','),dpi=300)
    plt.clf()
#%% mapdir, keyc, info, corrector, x_results, y_results, maxtime, mode_1
def zero_press_draw(mapdir, keyc, info, corrector, x_results, y_results, maxtime, mode_1, totf):
    
    plt.plot(x_results, y_results)
    
    
    pressacc = '320='+str(info.count_geki)+', 300='+str(info.count_300)+'\n200='+str(info.count_katu)+', 100='+str(info.count_100)+'\n50='+str(info.count_50)+', 0='+str(info.count_miss)
    plt.grid()
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlim(0,maxtime)
    plt.xlabel('play time(s)',fontsize=15)
    plt.ylabel(r'zero',fontsize=15)
    #plt.text(maxtime*0.5/MAX_SHOWTIME, 0.5, str(osrparse.Mod(info.mods))[4:].replace("|","\n")+"\nscores="+str(info.score), va='bottom')
    #plt.text(maxtime*(MAX_SHOWTIME-0.5)/MAX_SHOWTIME, 0.5, pressacc+"\nRI="+format(corrector,"0.2f"), ha='right', va='bottom')
    plt.title(info.username+","+str(info.timestamp),fontsize=15)
    plt.suptitle(mapdir[13:]+"\n"+totf,fontsize=5, ha='left', x = 0.03, y = 0.97)
    plt.tight_layout()
    plt.savefig(f"../graph results {mode_1}/"+mapdir[13:].replace('.',','),dpi=300)
    plt.clf()
   