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
s_hls_v=0;s_dash_v=0;s_hls_l=0;s_dash_l=0;s_hls_c=0;s_dash_c=0

file = sys.argv[1:]
for z in file:
    y = y+ sum(1 for file in open(os.getcwd()+'\/'+z,'r'))
    print('\r',end='')
    print('Total rows = ',y,end='')
    end_time = datetime.now()
    print('      Duration: {}'.format(end_time - start_time), end='')
def type_cache (i,j):
    """Function for count request percentage of VOD/Live/CU and HIT/MISS percentage of this types"""
    global v; global l; global t; global hv; global mv; global hl; global ml; global ht; global mt
    for i, j in zip(i, j):
         if j.find('servicetype=0') != -1 and i.endswith('HIT'):
                v += 1
                hv += 1
         elif j.find('servicetype=0') != -1 and i.endswith('MISS'):
                v += 1
                mv += 1
         elif j.find('servicetype=1') != -1 and i.endswith('HIT'):
                l += 1
                hl += 1
         elif j.find('servicetype=1') != -1 and i.endswith('MISS'):
                l += 1
                ml += 1
         elif j.find('servicetype=3') != -1 and i.endswith('HIT'):
                t += 1
                ht += 1
         elif j.find('servicetype=3') != -1 and i.endswith('MISS'):
                t += 1
                mt += 1
def hls_dash (j):
    """Function for count request percentage of HLS/DASH for VOD/Live/CU"""
    global hls_v; global dash_v; global hls_l; global dash_l; global hls_c; global dash_c
    for j in j:
        if j.find('servicetype=0') != -1 and j.find('PolicyMode') != -1:
            hls_v += 1
        elif j.find('servicetype=0') != -1 and j.find('PolicyMode') == -1:
            dash_v += 1
        elif j.find('servicetype=1') != -1 and j.find('PolicyMode') != -1:
            hls_l += 1
        elif j.find('servicetype=1') != -1 and j.find('PolicyMode') == -1:
            dash_l += 1
        elif j.find('servicetype=3') != -1 and j.find('PolicyMode') != -1:
            hls_c += 1
        elif j.find('servicetype=3') != -1 and j.find('PolicyMode') == -1:
            dash_c += 1

def hls_dash_chunk (j):
    """Function for count request percentage of HLS/DASH for VOD/Live/CU"""
    global s_hls_v; global s_dash_v; global s_hls_l; global s_dash_l; global s_hls_c; global s_dash_c
    for j in j:
        if (j.find('.m4v') != -1 or j.find('.m4a') != -1) and j.find('servicetype=0') != -1 and j.find('PolicyMode') != -1:
            s_hls_v += 3
        elif (j.find('.m4v') != -1 or j.find('.m4a') != -1) and j.find('servicetype=0') != -1 and j.find('PolicyMode') == -1:
            s_dash_v += 1
        elif (j.find('.m4v') != -1 or j.find('.m4a') != -1) and j.find('servicetype=1') != -1 and j.find('PolicyMode') != -1:
            s_hls_l += 3
        elif (j.find('.m4v') != -1 or j.find('.m4a') != -1) and j.find('servicetype=1') != -1 and j.find('PolicyMode') == -1:
            s_dash_l += 1
        elif (j.find('.m4v') != -1 or j.find('.m4a') != -1) and j.find('servicetype=3') != -1 and j.find('PolicyMode') != -1:
            s_hls_c += 3
        elif (j.find('.m4v') != -1 or j.find('.m4a') != -1) and j.find('servicetype=3') != -1 and j.find('PolicyMode') == -1:
            s_dash_c += 1


if __name__ == '__main__':
    for m in file:
        with open(os.getcwd()+'\/'+m, newline='') as hcs_1:
           hcs_2 = csv.reader(hcs_1, delimiter=' ')
           for hcs in hcs_2:
                x+=1

                type_cache(hcs[3:4],hcs[10:11]);
                hls_dash(hcs[10:11]);
                hls_dash_chunk(hcs[10:11]);

                #if x > x+100:
                    print('\r',end='')
                    print('Processed/Total ',x,'/',y,end='')
                    end_time=datetime.now()
                    print('      Duration: {}'.format(end_time - start_time),end='')

print()
print()
print('1.   % between VOD/LIVE/CU  (all requests)')
print()
print('%14s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('VOD =',(v/(l+v+t)*100),'%','Live =',(l/(l+v+t)*100),'%','CU =',(t/(l+v+t)*100),'%'))
print()
print('2.  % between HIT/MISS for VOD/LIVE/CU  (all requests)')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HIT','VOD =',(hv/(hv+mv)*100),'%','Live =',(hl/(hl+ml)*100),'%','CU =',(ht/(ht+mt)*100),'%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('MISS','VOD =',(mv/(hv+mv)*100),'%','Live =',(ml/(hl+ml)*100),'%','CU =',(mt/(ht+mt)*100),'%'))
print()
print('3.  % between HLS/Dash of VOD/LIVE/CU  (all requests)')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLS','VOD =',(hls_v/(hls_v+dash_v)*100),'%','Live =',(hls_l/(hls_l+dash_l)*100),'%','CU =',(hls_c/(hls_c+dash_c)*100),'%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('DASH','VOD =',(dash_v/(hls_v+dash_v)*100),'%','Live =',(dash_l/(hls_l+dash_l)*100),'%','CU =',(dash_c/(hls_c+dash_c)*100),'%'))
print()
print('4.  % of PlayBack Duration. (HLS chunk = 6sec, Dash chunk=2sec) between HLS/Dash of VOD/LIVE/CU  (only m4v|m4a requests)')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLS','VOD =',(s_hls_v/(s_hls_v+s_dash_v)*100),'%','Live =',(s_hls_l/(s_hls_l+s_dash_l)*100),'%','CU =',(s_hls_c/(s_hls_c+s_dash_c)*100),'%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('DASH','VOD =',(s_dash_v/(s_hls_v+s_dash_v)*100),'%','Live =',(s_dash_l/(s_hls_l+s_dash_l)*100),'%','CU =',(s_dash_c/(s_hls_c+s_dash_c)*100),'%'))
print()