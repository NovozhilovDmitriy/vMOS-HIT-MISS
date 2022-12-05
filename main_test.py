#!/home/uniagent/agent_plugins/OMAgent/modules/python/bin/python

import sys
import csv
import os
import time
from datetime import datetime

start_time=datetime.now()

cur_row = 0; total_rows = 0
unfound_rows = 0
count_rows = 0; total_profiles = 0

file = sys.argv[1:]

for z in file: #Counting how many rows totaly we will have for this process#
    total_rows = total_rows + sum(1 for file in open(os.getcwd() + '\/' + z, 'r'))
    print('\r',end='')
    end_time = datetime.now()
    print(f'Total rows = {total_rows:,}      Duration: {end_time - start_time}', end='')

qa_lab = [
    {"quality": "LV_Dyn_HD_1080_4HP_8000", "qa": "HD", "score" : 5.0, "count": 0},
    {"quality": "LV_Dyn_HD_1080_4HP_5000", "qa": "HD", "score" : 4.9, "count": 0},
    {"quality": "LV_Dyn_HD_720_4HP_2500", "qa": "HD", "score" : 4.2, "count": 0},
    {"quality": "LV_Dyn_HD_576_4HP_1400", "qa": "HD", "score" : 3.5, "count": 0},
    {"quality": "LV_Dyn_HD_504_4HP_900", "qa": "HD", "score" : 2.3, "count": 0},
    {"quality": "LV_Dyn_HD_432_4HP_500", "qa": "HD", "score" : 1.0, "count": 0},
    {"quality": "LV_Int_HD_1080_4HP_4300", "qa": "HD", "score" : 4.5 , "count": 0},
    {"quality": "LV_Int_HD_1080_4HP_5000", "qa": "HD", "score" : 5.0, "count": 0},
    {"quality": "LV_Int_HD_432_4HP_500", "qa": "HD", "score" : 1.0, "count": 0},
    {"quality": "LV_Int_HD_504_4HP_800", "qa": "HD", "score" : 2.2, "count": 0},
    {"quality": "LV_Int_HD_576_4HP_1200", "qa": "HD", "score" : 3.2, "count": 0},
    {"quality": "LV_Int_HD_720_4HP_2000", "qa": "HD", "score" : 4.2, "count": 0},
    {"quality": "LV_Sta_HD_1080_4HP_4000", "qa": "HD", "score" : 5.0, "count": 0},
    {"quality": "LV_Sta_HD_432_4HP_500", "qa": "HD", "score" : 1.0, "count": 0},
    {"quality": "LV_Sta_HD_504_4HP_700", "qa": "HD", "score" : 2.1, "count": 0},
    {"quality": "LV_Sta_HD_576_4HP_1000", "qa": "HD", "score" : 3.0, "count": 0},
    {"quality": "LV_Sta_HD_720_4HP_1800", "qa": "HD", "score" : 4.2, "count": 0},
    {"quality": "LV_Dyn_SD_432_4HP_500", "qa": "SD", "score" : 1.0, "count": 0},
    {"quality": "LV_Dyn_SD_480_4HP_900", "qa": "SD", "score" : 2.3, "count": 0},
    {"quality": "LV_Dyn_SD_576_4HP_1400", "qa": "SD", "score" : 3.5, "count": 0},
    {"quality": "LV_Dyn_SD_576_4HP_3000", "qa": "SD", "score" : 4.2, "count": 0},
    {"quality": "LV_SD_240_4HP_512", "qa": "SD", "score" : 1.0, "count": 0},
    {"quality": "LV_SD_480_4HP_1600", "qa": "SD", "score" : 3.3, "count": 0},
    {"quality": "LV_SD_576_4HP_2100", "qa": "SD", "score" : 4.0, "count": 0},
    {"quality": "LV_Sta_SD_432_4HP_500", "qa": "SD", "score" : 1.0, "count": 0},
    {"quality": "LV_Sta_SD_480_4HP_700", "qa": "SD", "score" : 2.1, "count": 0},
    {"quality": "LV_Sta_SD_576_4HP_1000", "qa": "SD", "score" : 3.0, "count": 0},
    {"quality": "LV_Sta_SD_576_4HP_2100", "qa": "SD", "score" : 4.2, "count": 0},
{"quality": "HHQ", "qa": "HD", "score" : 5.0, "count": 0},
{"quality": "HQ", "qa": "SD", "score" : 4.4, "count": 0},
{"quality": "MQ", "qa": "SD", "score" : 4.0, "count": 0},
{"quality": "LQ", "qa": "SD", "score" : 1.0, "count": 0},
]

def search_qa(i):
    """Function for counting quality from logs"""
    global unfound_rows;
    for z in qa_lab:
        if i[0].find(z["quality"]) != -1:
            z["count"] += 1
            return
    else:
        unfound_rows += 1

if __name__ == '__main__': #Main processing#
    for m in file:
        with open(os.getcwd()+'\/'+m, encoding='utf-8', newline='') as hcs_1:
           hcs_2 = csv.reader(hcs_1, delimiter=' ')
           for hcs in hcs_2:
               cur_row+=1
               a = hcs[10]
               if hcs[10].find('.m4v') != -1:
                   search_qa(hcs[10:11]);
               end_time = datetime.now()
               if cur_row % 1 == 0: #print pregress bar#
                   end_time = datetime.now()
                   print('\r', end='')
                   print(f'Processed/Total = {cur_row:,} / {total_rows:,}      Duration: {end_time - start_time}', end='')

#Print result#
print()
print()
print('1.   Total score for POP (all requests)')
print()
for i in qa_lab:
    if i["count"] > 0:
       profile_site_score = i['score'] * i['count']
       count_rows = count_rows + i['count']
       #print(i['quality'], ' - Score  -  ', i['score'], ' - Count -  ', i['count'], '  TOTAL Profile Score = ', profile_site_score)
       total_profiles = total_profiles + profile_site_score
print()
print(f'Total POP score = {total_profiles / count_rows}')

print()
print('Total rows skipped = ', unfound_rows)
# print('2.  % between HIT/MISS for VOD/LIVE/CU  (all requests)')
# print()
# print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('HIT','VOD =', vod_hit_total, '%', 'Live =', live_hit_total, '%', 'CU =', cuts_hit_total, '%'))
# print('%5s %8s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('MISS','VOD =', vod_miss_total, '%', 'Live =', live_miss_total, '%', 'CU =', cuts_miss_total, '%'))
