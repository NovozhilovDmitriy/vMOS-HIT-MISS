#!/home/uniagent/agent_plugins/OMAgent/modules/python/bin/python

import sys
import csv
import os
import time
from datetime import datetime

start_time=datetime.now()

vod = live = cuts = hit_vod = miss_vod = hit_live = miss_live = hit_cuts = miss_cuts = 0
cur_row = total_rows = 0
hlsv7_vod = dash_vod = hlsv7_live = dash_live = hlsv7_cuts = dash_cuts = 0
sec_hlsv7_vod = sec_dash_vod = sec_hlsv7_live = 0
sec_dash_live = sec_hlsv7_cuts = sec_dash_cuts = 0
hlsv3_cuts = hlsv3_vod = sec_hlsv3_cuts = sec_hlsv3_vod = 0
sec_hlsv3_cuts_hit = sec_hlsv3_cuts_miss = sec_hlsv3_vod_hit = sec_hlsv3_vod_miss = 0
sec_hlsv7_vod_hit = sec_dash_vod_hit = sec_hlsv7_live_hit = 0
sec_hlsv7_vod_miss = sec_dash_vod_miss = sec_hlsv7_live_miss = 0
sec_dash_live_hit = sec_hlsv7_cuts_hit = sec_dash_cuts_hit = 0
sec_dash_live_miss = sec_hlsv7_cuts_miss = sec_dash_cuts_miss = 0

#  Import arguments like files for next processing
file = sys.argv[1:]

for z in file: #  Counting how many rows totaly we will have for this process#
    total_rows = total_rows + sum(1 for line in open(os.getcwd() + '\/' + z, 'r'))
    #  For LINUX execute, please commit previous row and uncommit this
    #  total_rows = total_rows + sum(1 for line in open(os.getcwd() + '/' + z, 'r'))
    print('\r', end='')
    end_time = datetime.now()
    print(f'Total rows = {total_rows:,}      Duration: {end_time - start_time}', end='')
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
def hlsv7_dash (i,j):
    """Function for count request percentage of HLS/DASH for VOD/Live/CU"""
    global hlsv7_vod; global dash_vod; global hlsv7_live; global dash_live; global hlsv7_cuts; global dash_cuts
    global sec_hlsv7_vod; global sec_dash_vod; global sec_hlsv7_live; global sec_dash_live; global sec_hlsv7_cuts; global sec_dash_cuts
    global sec_hlsv7_vod_hit; global sec_dash_vod_hit; global sec_hlsv7_live_hit; global sec_hlsv7_vod_miss; global sec_dash_vod_miss
    global sec_hlsv7_live_miss; global sec_dash_live_hit; global sec_hlsv7_cuts_hit; global sec_dash_cuts_hit; global sec_dash_live_miss
    global sec_hlsv7_cuts_miss; global sec_dash_cuts_miss
    for i, j in zip(i, j):
        if j.find('servicetype=0') != -1:
            if j.find('PolicyMode') != -1:
                hlsv7_vod += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_hlsv7_vod += 3
                    if i.endswith('HIT'):
                        sec_hlsv7_vod_hit += 1
                    else:
                        sec_hlsv7_vod_miss += 1
            else:
                dash_vod += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_dash_vod += 1
                    if i.endswith('HIT'):
                        sec_dash_vod_hit += 1
                    else:
                        sec_dash_vod_miss += 1
        elif j.find('servicetype=1') != -1:
            if j.find('PolicyMode') != -1:
                hlsv7_live += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_hlsv7_live += 3
                    if i.endswith('HIT'):
                        sec_hlsv7_live_hit += 1
                    else:
                        sec_hlsv7_live_miss += 1
            else:
                dash_live += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_dash_live += 1
                    if i.endswith('HIT'):
                        sec_dash_live_hit += 1
                    else:
                        sec_dash_live_miss += 1
        elif j.find('servicetype=3') != -1 or j.find('servicetype=2'):
            if j.find('PolicyMode') != -1:
                hlsv7_cuts += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_hlsv7_cuts += 3
                    if i.endswith('HIT'):
                        sec_hlsv7_cuts_hit += 1
                    else:
                        sec_hlsv7_cuts_miss += 1
            else:
                dash_cuts += 1
                if (j.find('.m4v') != -1 or j.find('.m4a') != -1):
                    sec_dash_cuts += 1
                    if i.endswith('HIT'):
                        sec_dash_cuts_hit += 1
                    else:
                        sec_dash_cuts_miss += 1
def hlsv3 (i,j):
    """Function for count request percentage of VOD/Live/CU for HLSv3"""
    global hlsv3_cuts; global hlsv3_vod;global sec_hlsv3_cuts; global sec_hlsv3_vod
    global sec_hlsv3_cuts_hit; global sec_hlsv3_cuts_miss; global sec_hlsv3_vod_hit; global sec_hlsv3_vod_miss
    for i, j in zip(i, j):
        if j.find('.hls.ts') != -1:
            if j.find('TVOD') != -1:
                hlsv3_cuts += 1
                sec_hlsv3_cuts += 3
                if i.endswith('HIT'):
                    sec_hlsv3_cuts_hit += 1
                else:
                    sec_hlsv3_cuts_miss += 1
            else:
                hlsv3_vod += 1
                sec_hlsv3_vod += 3
                if i.endswith('HIT'):
                    sec_hlsv3_vod_hit += 1
                else:
                    sec_hlsv3_vod_miss += 1


def zero_divizion(a, b):
    """Function for cheking statistics result on division 0. If True - print =0 in result"""
    return a / b * 100 if b else 0


if __name__ == '__main__':  # Main processing
    for m in file:
        with open(os.getcwd() + '\/' + m, encoding='utf-8', newline='') as hcs_1:
        #  For LINUX execute, please commit previous row and uncommit this
        #  with open(os.getcwd()+'/'+m, encoding='utf-8', newline='') as hcs_1:
           hcs_2 = csv.reader(hcs_1, delimiter=' ')
           for hcs in hcs_2:
               cur_row+=1
               type_cache(hcs[3:4], hcs[10:11])
               hlsv7_dash(hcs[3:4], hcs[10:11])
               hlsv3(hcs[3:4], hcs[10:11])
               end_time = datetime.now()
               if cur_row % 12345 == 0:  # print progress bar
                   end_time = datetime.now()
                   print('\r', end='')
                   print(f'Processed/Total = {cur_row:,} / {total_rows:,}      Duration: {end_time - start_time}', end='')

#  Prepare final statistics for print
vod_total = zero_divizion(vod, live + vod + cuts)
live_total = zero_divizion(live, live + vod + cuts)
cuts_total = zero_divizion(cuts, live + vod + cuts)
vod_hit_total = zero_divizion(hit_vod, hit_vod + miss_vod)
vod_miss_total = zero_divizion(miss_vod, hit_vod + miss_vod)
live_hit_total = zero_divizion(hit_live, hit_live + miss_live)
live_miss_total = zero_divizion(miss_live, hit_live + miss_live)
cuts_hit_total = zero_divizion(hit_cuts, hit_cuts + miss_cuts)
cuts_miss_total = zero_divizion(miss_cuts, hit_cuts + miss_cuts)
sec_hlsv3_vod_total = zero_divizion(sec_hlsv3_vod, sec_hlsv3_vod + sec_hlsv7_vod + sec_dash_vod)
sec_hlsv3_cuts_total = zero_divizion(sec_hlsv3_cuts, sec_hlsv3_cuts + sec_hlsv7_cuts + sec_dash_cuts)
sec_hlsv7_vod_total = zero_divizion(sec_hlsv7_vod, sec_hlsv3_vod + sec_hlsv7_vod + sec_dash_vod)
sec_hlsv7_live_total = zero_divizion(sec_hlsv7_live, sec_hlsv7_live + sec_dash_live)
sec_hlsv7_cuts_total = zero_divizion(sec_hlsv7_cuts, sec_hlsv3_cuts + sec_hlsv7_cuts + sec_dash_cuts)
sec_dash_vod_total = zero_divizion(sec_dash_vod, sec_hlsv3_vod + sec_hlsv7_vod + sec_dash_vod)
sec_dash_live_total = zero_divizion(sec_dash_live, sec_hlsv7_live + sec_dash_live)
sec_dash_cuts_total = zero_divizion(sec_dash_cuts, sec_hlsv3_cuts + sec_hlsv7_cuts + sec_dash_cuts)
sec_hlsv3_vod_hit_total = zero_divizion(sec_hlsv3_vod_hit, sec_hlsv3_vod_hit + sec_hlsv3_vod_miss)
sec_hlsv3_vod_miss_total = zero_divizion(sec_hlsv3_vod_miss, sec_hlsv3_vod_hit + sec_hlsv3_vod_miss)
sec_hlsv3_cuts_hit_total = zero_divizion(sec_hlsv3_cuts_hit, sec_hlsv3_cuts_hit + sec_hlsv3_cuts_miss)
sec_hlsv3_cuts_miss_total = zero_divizion(sec_hlsv3_cuts_miss, sec_hlsv3_cuts_hit + sec_hlsv3_cuts_miss)
sec_hlsv7_vod_hit_total = zero_divizion(sec_hlsv7_vod_hit, sec_hlsv7_vod_hit + sec_hlsv7_vod_miss)
sec_hlsv7_vod_miss_total = zero_divizion(sec_hlsv7_vod_miss, sec_hlsv7_vod_hit + sec_hlsv7_vod_miss)
sec_hlsv7_live_hit_total = zero_divizion(sec_hlsv7_live_hit, sec_hlsv7_live_hit + sec_hlsv7_live_miss)
sec_hlsv7_live_miss_total = zero_divizion(sec_hlsv7_live_miss, sec_hlsv7_live_hit + sec_hlsv7_live_miss)
sec_hlsv7_cuts_hit_total = zero_divizion(sec_hlsv7_cuts_hit, sec_hlsv7_cuts_hit + sec_hlsv7_cuts_miss)
sec_hlsv7_cuts_miss_total = zero_divizion(sec_hlsv7_cuts_miss, sec_hlsv7_cuts_hit + sec_hlsv7_cuts_miss)
sec_dash_vod_hit_total = zero_divizion(sec_dash_vod_hit, sec_dash_vod_hit + sec_dash_vod_miss)
sec_dash_vod_miss_total = zero_divizion(sec_dash_vod_miss, sec_dash_vod_hit + sec_dash_vod_miss)
sec_dash_live_hit_total = zero_divizion(sec_dash_live_hit, sec_dash_live_hit + sec_dash_live_miss)
sec_dash_live_miss_total = zero_divizion(sec_dash_live_miss, sec_dash_live_hit + sec_dash_live_miss)
sec_dash_cuts_hit_total = zero_divizion(sec_dash_cuts_hit, sec_dash_cuts_hit + sec_dash_cuts_miss)
sec_dash_cuts_miss_total = zero_divizion(sec_dash_cuts_miss, sec_dash_cuts_hit + sec_dash_cuts_miss)


#Print result#
print()
print()
print('1.  % between VOD/LIVE/CU  (all requests)')
print()
print('%14s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('VOD =', vod_total, '%', 'Live =', live_total, '%', 'CU =', cuts_total, '%'))
print()
print('2.  % between HIT/MISS for VOD/LIVE/CU  (all requests)')
print()
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HIT','VOD =', vod_hit_total, '%', 'Live =', live_hit_total, '%', 'CU =', cuts_hit_total, '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('MISS','VOD =', vod_miss_total, '%', 'Live =', live_miss_total, '%', 'CU =', cuts_miss_total, '%'))
print()
#print('3.  % between HLSv7/HLSv3/Dash of VOD/LIVE/CU  (all requests)')
#print()
#print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLSv3','VOD =', (hlsv3_vod / (hlsv3_vod+hlsv7_vod + dash_vod) * 100), '%', 'Live =', 0, '%', 'CU =', (hlsv3_cuts / (hlsv3_cuts+hlsv7_cuts + dash_cuts) * 100), '%'))
#print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLSv7','VOD =', (hlsv7_vod / (hlsv3_vod+hlsv7_vod + dash_vod) * 100), '%', 'Live =', (hlsv7_live / (hlsv7_live + dash_live) * 100), '%', 'CU =', (hlsv7_cuts / (hlsv3_cuts+hlsv7_cuts + dash_cuts) * 100), '%'))
#print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('DASH','VOD =', (dash_vod / (hlsv3_vod+hlsv7_vod + dash_vod) * 100), '%', 'Live =', (dash_live / (hlsv7_live + dash_live) * 100), '%', 'CU =', (dash_cuts / (hlsv3_cuts+hlsv7_cuts + dash_cuts) * 100), '%'))
#print()
print('3.  % of PlayBack Duration. (HLS chunk = 6sec, Dash chunk=2sec) between HLSv7/HLSv3/Dash of VOD/LIVE/CU  (only ts|m4v|m4a requests)')
print()
print('%5s %8s %5.1f %-3s %8s %5s %0s %8s %5.1f %0s' % ('HLSv3', 'VOD =', sec_hlsv3_vod_total, '%', 'Live =', 'NULL', '%', 'CU =', sec_hlsv3_cuts_total, '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HLSv7', 'VOD =', sec_hlsv7_vod_total, '%', 'Live =', sec_hlsv7_live_total, '%', 'CU =', sec_hlsv7_cuts_total, '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('DASH', 'VOD =', sec_dash_vod_total, '%', 'Live =', sec_dash_live_total, '%', 'CU =', sec_dash_cuts_total, '%'))
print()
print('4.  % of HIT/MISS for HLSv7/HLSv3/Dash of VOD/LIVE/CU  (only ts|m4v|m4a requests)')
print()
print('%5s' % ('HLSv3'))
print('%5s %8s %5.1f %-3s %8s %5s %0s %8s %5.1f %0s' % ('HIT', 'VOD =', sec_hlsv3_vod_hit_total, '%', 'Live =', 'NULL', '%', 'CU =', sec_hlsv3_cuts_hit_total, '%'))
print('%5s %8s %5.1f %-3s %8s %5s %0s %8s %5.1f %0s' % ('MISS', 'VOD =', sec_hlsv3_vod_miss_total, '%', 'Live =', 'NULL', '%', 'CU =', sec_hlsv3_cuts_miss_total, '%'))
print()
print('%5s' % ('HLSv7'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HIT', 'VOD =', sec_hlsv7_vod_hit_total, '%', 'Live =', sec_hlsv7_live_hit_total, '%', 'CU =', sec_hlsv7_cuts_hit_total, '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('MISS', 'VOD =', sec_hlsv7_vod_miss_total, '%', 'Live =', sec_hlsv7_live_miss_total, '%', 'CU =', sec_hlsv7_cuts_miss_total, '%'))
print()
print('%5s' % ('DASH'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HIT', 'VOD =', sec_dash_vod_hit_total, '%', 'Live =', sec_dash_live_hit_total, '%', 'CU =', sec_dash_cuts_hit_total, '%'))
print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('MISS', 'VOD =', sec_dash_vod_miss_total, '%', 'Live =', sec_dash_live_miss_total, '%', 'CU =', sec_dash_cuts_miss_total, '%'))
print()