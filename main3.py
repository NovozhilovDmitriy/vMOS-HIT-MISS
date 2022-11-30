#!/home/uniagent/agent_plugins/OMAgent/modules/python/bin/python

import sys
import csv
import os
import time
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, '')

start_time=datetime.now()

vod = 0; live = 0; cuts = 0; hit_vod = 0; miss_vod = 0; hit_live = 0; miss_live = 0; hit_cuts = 0; miss_cuts = 0
cur_row = 0; total_rows = 0
hlsv7_vod = 0; dash_vod = 0; hlsv7_live = 0; dash_live = 0; hlsv7_cuts = 0; dash_cuts = 0
sec_hlsv7_vod = 0; sec_dash_vod = 0; sec_hlsv7_live = 0; sec_dash_live = 0; sec_hlsv7_cuts = 0; sec_dash_cuts = 0
hlsv3_cuts = 0; hlsv3_vod = 0; sec_hlsv3_cuts = 0; sec_hlsv3_vod = 0;

file = sys.argv[1:] #Import arguments like files for next processing#

for z in file: #Counting how many rows totaly we will have for this process#
    total_rows = total_rows + sum(1 for file in open(os.getcwd() + '\/' + z, 'r'))
    print('\r',end='')
    end_time = datetime.now()
    print('Total rows = ',f'{total_rows:n}', '      Duration: {}'.format(end_time - start_time), end='')
def type_cache (i,j):
    """Function for count request percentage of VOD/Live/CU and HIT/MISS percentage of this types"""
    global vod; global live; global cuts; global hit_vod; global miss_vod; global hit_live; global miss_live; global hit_cuts; global miss_cuts
    for i, j in zip(i, j):
        if j.find('servicetype=0') != -1 or (j.find('.hls.ts') != -1 and j.find('TVOD') == -1):
            if i.endswith('HIT'):
                vod += 1
                hit_vod += 1
            else:
                vod += 1
                miss_vod += 1
        elif j.find('servicetype=1') != -1:
            if i.endswith('HIT'):
                live += 1
                hit_live += 1
            else:
                live += 1
                miss_live += 1
        elif (j.find('servicetype=3') != -1 or j.find('servicetype=2') != -1) or (j.find('.hls.ts') != -1 and j.find('TVOD') != -1):
            if i.endswith('HIT'):
                cuts += 1
                hit_cuts += 1
            else:
                cuts += 1
                miss_cuts += 1
def hlsv7_dash (j):
    """Function for count request percentage of HLS/DASH for VOD/Live/CU"""
    global hlsv7_vod; global dash_vod; global hlsv7_live; global dash_live; global hlsv7_cuts; global dash_cuts
    global sec_hlsv7_vod; global sec_dash_vod; global sec_hlsv7_live; global sec_dash_live; global sec_hlsv7_cuts; global sec_dash_cuts
    for j in j:
        if j.find('servicetype=0') != -1:
            if j.find('PolicyMode') != -1:
                hlsv7_vod += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_hlsv7_vod += 3
            else:
                dash_vod += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_dash_vod += 1
        elif j.find('servicetype=1') != -1:
            if j.find('PolicyMode') != -1:
                hlsv7_live += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_hlsv7_live += 3
            else:
                dash_live += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_dash_live += 1
        elif j.find('servicetype=3') != -1 or j.find('servicetype=2'):
            if j.find('PolicyMode') != -1:
                hlsv7_cuts += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_hlsv7_cuts += 3
            else:
                dash_cuts += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_dash_cuts += 1
def hlsv3 (j):
    """Function for count request percentage of VOD/Live/CU for HLSv3"""
    global hlsv3_cuts; global hlsv3_vod;global sec_hlsv3_cuts; global sec_hlsv3_vod;
    for j in j:
        if j.find('.hls.ts') != -1:
            if j.find('TVOD') != -1:
                hlsv3_cuts += 1
                sec_hlsv3_cuts += 3
            else:
                hlsv3_vod += 1
                sec_hlsv3_vod += 3

if __name__ == '__main__': #Main processing#
    for m in file:
        with open(os.getcwd()+'\/'+m, newline='') as hcs_1:
           hcs_2 = csv.reader(hcs_1, delimiter=' ')
           for hcs in hcs_2:
               cur_row+=1
               type_cache(hcs[3:4],hcs[10:11]);
               hlsv7_dash(hcs[10:11]);
               hlsv3(hcs[10:11]);
               end_time = datetime.now()
               if cur_row % 12345 == 0: #print pregress bar#
                   end_time = datetime.now()
                   print('\r', end='')
                   print('Processed/Total ', f'{cur_row:n}', '/', f'{total_rows:n}', '      Duration: {}'.format(end_time - start_time), end='')

print()
print()
print('1.   % between VOD/LIVE/CU  (all requests)')
print()
print('%14s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('VOD =', (vod / (live + vod + cuts) * 100), '%', 'Live =', (live / (live + vod + cuts) * 100), '%', 'CU =', (cuts / (live + vod + cuts) * 100), '%'))
print()
print('2.  % between HIT/MISS for VOD/LIVE/CU  (all requests)')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HIT','VOD =', (hit_vod / (hit_vod + miss_vod) * 100), '%', 'Live =', (hit_live / (hit_live + miss_live) * 100), '%', 'CU =', (hit_cuts / (hit_cuts + miss_cuts) * 100), '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('MISS','VOD =', (miss_vod / (hit_vod + miss_vod) * 100), '%', 'Live =', (miss_live / (hit_live + miss_live) * 100), '%', 'CU =', (miss_cuts / (hit_cuts + miss_cuts) * 100), '%'))
print()
#print('3.  % between HLSv7/HLSv3/Dash of VOD/LIVE/CU  (all requests)')
#print()
#print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLSv3','VOD =', (hlsv3_vod / (hlsv3_vod+hlsv7_vod + dash_vod) * 100), '%', 'Live =', 0, '%', 'CU =', (hlsv3_cuts / (hlsv3_cuts+hlsv7_cuts + dash_cuts) * 100), '%'))
#print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLSv7','VOD =', (hlsv7_vod / (hlsv3_vod+hlsv7_vod + dash_vod) * 100), '%', 'Live =', (hlsv7_live / (hlsv7_live + dash_live) * 100), '%', 'CU =', (hlsv7_cuts / (hlsv3_cuts+hlsv7_cuts + dash_cuts) * 100), '%'))
#print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('DASH','VOD =', (dash_vod / (hlsv3_vod+hlsv7_vod + dash_vod) * 100), '%', 'Live =', (dash_live / (hlsv7_live + dash_live) * 100), '%', 'CU =', (dash_cuts / (hlsv3_cuts+hlsv7_cuts + dash_cuts) * 100), '%'))
#print()
print('3.  % of PlayBack Duration. (HLS chunk = 6sec, Dash chunk=2sec) between HLSv7/HLSv3/Dash of VOD/LIVE/CU  (only ts|m4v|m4a requests)')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLSv3','VOD =', (sec_hlsv3_vod / (sec_hlsv3_vod+sec_hlsv7_vod + sec_dash_vod) * 100), '%', 'Live =', 0, '%', 'CU =', (sec_hlsv3_cuts / (sec_hlsv3_cuts+sec_hlsv7_cuts + sec_dash_cuts) * 100), '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLSv7','VOD =', (sec_hlsv7_vod / (sec_hlsv3_vod+sec_hlsv7_vod + sec_dash_vod) * 100), '%', 'Live =', (sec_hlsv7_live / (sec_hlsv7_live + sec_dash_live) * 100), '%', 'CU =', (sec_hlsv7_cuts / (sec_hlsv3_cuts+sec_hlsv7_cuts + sec_dash_cuts) * 100), '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('DASH','VOD =', (sec_dash_vod / (sec_hlsv3_vod+sec_hlsv7_vod + sec_dash_vod) * 100), '%', 'Live =', (sec_dash_live / (sec_hlsv7_live + sec_dash_live) * 100), '%', 'CU =', (sec_dash_cuts / (sec_hlsv3_cuts+sec_hlsv7_cuts + sec_dash_cuts) * 100), '%'))
print()