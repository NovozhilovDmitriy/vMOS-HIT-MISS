#!/home/uniagent/agent_plugins/OMAgent/modules/python/bin/python

import sys
import csv
import os
import time
from datetime import datetime
start_time=datetime.now()
v = 0;l = 0;t = 0;hv = 0;mv = 0;hl = 0;ml = 0;ht = 0;mt = 0
x = 0;y = 0
hls_v=0;dash_v=0;hls_l=0;dash_l=0;hls_c=0;dash_c=0

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
                   v += 1
                   hv+= 1
                elif j.find('servicetype=0')!=-1 and i.endswith('MISS'):
                   v += 1
                   mv += 1
                elif j.find('servicetype=1')!=-1 and i.endswith('HIT'):
                   l += 1
                   hl+=1
                elif j.find('servicetype=1')!=-1 and i.endswith('MISS'):
                   l += 1
                   ml += 1
                elif j.find('servicetype=3')!=-1 and i.endswith('HIT'):
                   t += 1
                   ht+=1
                elif j.find('servicetype=3')!=-1 and i.endswith('MISS'):
                   t += 1
                   mt += 1

            for a, b in zip(hcs[9:10],hcs[10:11]):
               if j.find('servicetype=0')!=-1 and j.find('PolicyMode')!=-1:
                   hls_v+=1
                   #hls_v+int(a)
               elif j.find('servicetype=0')!=-1 and j.find('PolicyMode')==-1:
                  dash_v+=1
                  #=dash_v+int(a)
               elif j.find('servicetype=1')!=-1 and j.find('PolicyMode')!=-1:
                  hls_l+=1
                  #hls_l+int(a)
               elif j.find('servicetype=1')!=-1 and j.find('PolicyMode')==-1:
                  dash_l+=1
                  #dash_l+int(a)
               elif j.find('servicetype=3')!=-1 and j.find('PolicyMode')!=-1:
                  hls_c+=1
                  #hls_c+int(a)
               elif j.find('servicetype=3')!=-1 and j.find('PolicyMode')==-1:
                  dash_c+=1
                  #dash_c+int(a)
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
print('%14s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('VOD =',(v/(l+v+t)*100),'%','Live =',(l/(l+v+t)*100),'%','CU =',(t/(l+v+t)*100),'%'))
print()
print('2.  % between HLS/Dash of VOD/LIVE/CU')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLS','VOD =',(hls_v/(hls_v+dash_v)*100),'%','Live =',(hls_l/(hls_l+dash_l)*100),'%','CU =',(hls_c/(hls_c+dash_c)*100),'%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('DASH','VOD =',(dash_v/(hls_v+dash_v)*100),'%','Live =',(dash_l/(hls_l+dash_l)*100),'%','CU =',(dash_c/(hls_c+dash_c)*100),'%'))
#print('VOD HLS =',format(hls_v/1000000,'.3f'),'Mb', ' Live HLS =',format(hls_l/1000000,'.3f'),'Mb', 'CU HLS=',format(hls_c/1000000,'.3f'),'Mb')
#print('VOD Dash =',format(dash_v/1000000,'.3f'),'Mb', ' Live Dash =',format(dash_l/1000000,'.3f'),'Mb', 'CU Dash=',format(dash_c/1000000,'.3f'),'Mb')
print()
print('3.  % between HIT/MISS for VOD/LIVE/CU')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HIT','VOD =',(hv/(hv+mv)*100),'%','Live =',(hl/(hl+ml)*100),'%','CU =',(ht/(ht+mt)*100),'%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('MISS','VOD =',(mv/(hv+mv)*100),'%','Live =',(ml/(hl+ml)*100),'%','CU =',(mt/(ht+mt)*100),'%'))
