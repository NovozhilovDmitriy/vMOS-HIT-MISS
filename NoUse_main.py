#!/home/uniagent/agent_plugins/OMAgent/modules/python/bin/python

import sys
import csv
import os
import time
from datetime import datetime
start_time=datetime.now()
vod = 0;live = 0;cuts = 0;hit_vod = 0;miss_vod = 0;hit_live = 0;miss_live = 0;hit_cuts = 0;miss_cuts = 0
x = 0;y = 0
hls_v=0;dash_vod=0;hlsv7_live=0;dash_live=0;hlsv7_cuts=0;dash_cuts=0

file = sys.argv[1:]
for z in file:
    y = y+ sum(1 for file in open(os.getcwd()+'\/'+z,'r'))

for m in file:
    with open(os.getcwd()+'\/'+m, newline='') as hcs_1:
       hcs_2 = csv.reader(hcs_1, delimiter=' ')
       for hcs in hcs_2:
            x+=1
            for i, j in zip(hcs[3:4], hcs[10:11]):
                if j.find('servicetype=0')!=-1 and i.endswith('HIT'):
                   vod += 1
                   hit_vod+= 1
                elif j.find('servicetype=0')!=-1 and i.endswith('MISS'):
                   vod += 1
                   miss_vod += 1
                elif j.find('servicetype=1')!=-1 and i.endswith('HIT'):
                   live += 1
                   hit_live+=1
                elif j.find('servicetype=1')!=-1 and i.endswith('MISS'):
                   live += 1
                   miss_live += 1
                elif j.find('servicetype=3')!=-1 and i.endswith('HIT'):
                   cuts += 1
                   hit_cuts+=1
                elif j.find('servicetype=3')!=-1 and i.endswith('MISS'):
                   cuts += 1
                   miss_cuts += 1

            for a, b in zip(hcs[9:10],hcs[10:11]):
               if j.find('servicetype=0')!=-1 and j.find('PolicyMode')!=-1:
                   hls_v+=1
                   #hls_v+int(a)
               elif j.find('servicetype=0')!=-1 and j.find('PolicyMode')==-1:
                  dash_vod+=1
                  #=dash_vod+int(a)
               elif j.find('servicetype=1')!=-1 and j.find('PolicyMode')!=-1:
                  hlsv7_live+=1
                  #hlsv7_live+int(a)
               elif j.find('servicetype=1')!=-1 and j.find('PolicyMode')==-1:
                  dash_live+=1
                  #dash_live+int(a)
               elif j.find('servicetype=3')!=-1 and j.find('PolicyMode')!=-1:
                  hlsv7_cuts+=1
                  #hlsv7_cuts+int(a)
               elif j.find('servicetype=3')!=-1 and j.find('PolicyMode')==-1:
                  dash_cuts+=1
                  #dash_cuts+int(a)
            print('\r',end='')
            print('Processed/Total ',x,'/',y,end='')
            end_time=datetime.now()
           # print("--- %.5s seconds ---" % (time.time() - start_time),end='')
            print('      Duration: {}'.format(end_time - start_time),end='')
            #time.sleep(1)

print()
print()
print('1.   % between VOD/LIVE/CU')
print()
print('%14s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('VOD =', (vod / (live + vod + cuts) * 100), '%', 'Live =', (live / (live + vod + cuts) * 100), '%', 'CU =', (cuts / (live + vod + cuts) * 100), '%'))
print()
print('2.  % between HLS/Dash of VOD/LIVE/CU')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLS','VOD =', (hls_v / (hls_v + dash_vod) * 100), '%', 'Live =', (hlsv7_live / (hlsv7_live + dash_live) * 100), '%', 'CU =', (hlsv7_cuts / (hlsv7_cuts + dash_cuts) * 100), '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('DASH','VOD =', (dash_vod / (hls_v + dash_vod) * 100), '%', 'Live =', (dash_live / (hlsv7_live + dash_live) * 100), '%', 'CU =', (dash_cuts / (hlsv7_cuts + dash_cuts) * 100), '%'))
#print('VOD HLS =',format(hls_v/1000000,'.3f'),'Mb', ' Live HLS =',format(hlsv7_live/1000000,'.3f'),'Mb', 'CU HLS=',format(hlsv7_cuts/1000000,'.3f'),'Mb')
#print('VOD Dash =',format(dash_vod/1000000,'.3f'),'Mb', ' Live Dash =',format(dash_live/1000000,'.3f'),'Mb', 'CU Dash=',format(dash_cuts/1000000,'.3f'),'Mb')
print()
print('3.  % between HIT/MISS for VOD/LIVE/CU')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HIT','VOD =', (hit_vod / (hit_vod + miss_vod) * 100), '%', 'Live =', (hit_live / (hit_live + miss_live) * 100), '%', 'CU =', (hit_cuts / (hit_cuts + miss_cuts) * 100), '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('MISS','VOD =', (miss_vod / (hit_vod + miss_vod) * 100), '%', 'Live =', (miss_live / (hit_live + miss_live) * 100), '%', 'CU =', (miss_cuts / (hit_cuts + miss_cuts) * 100), '%'))
