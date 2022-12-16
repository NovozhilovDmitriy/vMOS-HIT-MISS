#!/home/uniagent/agent_plugins/OMAgent/modules/python/bin/python

"""
#  Script for count vMOS on MTS Video project. Analyze HCS access.log for count requests with different Video profiles.
#  For Dash used current request count (because one chunk duration 2 seconds)
#  For HLSv7 use request*3 because one chunk duration 6 seconds
#  Script use Python 3.0. The path to this version of Python need to configure here at the beginning of script like:
#  /home/uniagent/agent_plugins/OMAgent/modules/python/bin/python
#  For executing script use command "/home/sshusr/main_test.py logfile.log"
#  For argument "logfile.log" could use wildcard like "logfile*.log" and all files will be processed one by one
#  Script use multiprocessing feature. To start script on several CPU need to add argument like "-c X"
#  where X - CPU number. Example: "/home/sshusr/main_test.py -c 4 logfile*.log"
#  Please focus on Server I/O performance. More CPU will occupation more I/O resourses.
#  Processing status you can control by progress bar "Processed/Total = 352,202 / 352,202"
#  Progress bug will update by files (after one log file finished -> result updated
#  Script provided by Novozhilov Dmitriy (+7 923 733 0029)
"""

import csv
import os
import sys
from multiprocessing import Manager, Pool
from datetime import datetime

start_time=datetime.now()

cur_row = 0
total_rows = 0
count_rows = 0
total_site_vmos = 0
count_vmos_live_rows = 0
count_vmos_live_hit_rows = 0
count_vmos_live_miss_rows = 0
total_vmos_live = 0
total_vmos_live_hit = 0
total_vmos_live_miss = 0
count_vmos_cuts_rows = 0
count_vmos_cuts_hit_rows = 0
count_vmos_cuts_miss_rows = 0
total_vmos_cuts = 0
total_vmos_cuts_hit = 0
total_vmos_cuts_miss = 0
count_vmos_vod_rows = 0
count_vmos_vod_hit_rows = 0
count_vmos_vod_miss_rows = 0
total_vmos_vod = 0
total_vmos_vod_hit = 0
total_vmos_vod_miss = 0

count_vmos_hlsv7_live_rows = 0
count_vmos_hlsv7_live_hit_rows = 0
count_vmos_hlsv7_live_miss_rows = 0
total_vmos_hlsv7_live = 0
total_vmos_hlsv7_live_hit = 0
total_vmos_hlsv7_live_miss = 0
count_vmos_hlsv7_cuts_rows = 0
count_vmos_hlsv7_cuts_hit_rows = 0
count_vmos_hlsv7_cuts_miss_rows = 0
total_vmos_hlsv7_cuts = 0
total_vmos_hlsv7_cuts_hit = 0
total_vmos_hlsv7_cuts_miss = 0
count_vmos_hlsv7_vod_rows = 0
count_vmos_hlsv7_vod_hit_rows = 0
count_vmos_hlsv7_vod_miss_rows = 0
total_vmos_hlsv7_vod = 0
total_vmos_hlsv7_vod_hit = 0
total_vmos_hlsv7_vod_miss = 0

#  Import arguments like files for next processing
file = sys.argv[1:]


def total_r():
    global total_rows
    for m in file:  # Counting how many rows totally we will have for this process#
       total_rows = total_rows + sum(1 for line in open(os.getcwd() + '\/' + m, 'r'))
       print('\r', end='')
       end_time = datetime.now()
       print(f'Total rows = {total_rows:,}      Duration of total rows counting: {end_time - start_time}', end='')
    print()


def search_qa(j,qa):
    """Function for counting Total POP vmos quality from logs,
    include only m4v and for HLSv7*3, because 1*hlsv7 chunk = 3* dash chunk"""
    for z in qa:
        if j[0].find(z["quality"]) != -1:
            if j[0].find('PolicyMode') != -1:
                z["count"] += 3
            else:
                z["count"] += 1
            return


def search_all(i, j, qa):
    """Function for counting quality (HIT/MISS) LIVE/CUTS/VOD from logs"""
    """ 'count' - total rows with profile 'quality' """
    """ 'count_hit_miss' - [dash_live_hit,dash_live_miss,dash_cuts_hit,dash_cuts_miss,dash_vod_hit,dash_vod_miss """
    """ hlsv7_live_hit,hlsv7_live_miss,hlsv7_cuts_hit,hlsv7_cuts_miss,hlsv7_vod_hit,hlsv7_vod_miss] """
    """ 'live_cuts_vod' - count of [dash_live, dash_cuts, dash_vod, hlsv7_live, hlsv7_cuts, hlsv7_vod] """
    for z in qa:
        if j[0].find(z["quality"]) != -1:
            if j[0].find('servicetype=0') != -1:
                if j[0].find('PolicyMode') != -1:
                    z["live_cuts_vod"][5] += 3
                    z["count"] += 3
                    if i[0].endswith('HIT'):
                        z["count_hit_miss"][10] += 1
                    else:
                        z["count_hit_miss"][11] += 1
                    return
                else:
                    z["live_cuts_vod"][2] += 1
                    z["count"] += 1
                    if i[0].endswith('HIT'):
                        z["count_hit_miss"][4] += 1
                    else:
                        z["count_hit_miss"][5] += 1
                    return
            elif j[0].find('servicetype=1') != -1:
                if j[0].find('PolicyMode') != -1:
                    z["live_cuts_vod"][3] += 3
                    z["count"] += 3
                    if i[0].endswith('HIT'):
                        z["count_hit_miss"][6] += 1
                    else:
                        z["count_hit_miss"][7] += 1
                    return
                else:
                    z["live_cuts_vod"][0] += 1
                    z["count"] += 1
                    if i[0].endswith('HIT'):
                        z["count_hit_miss"][0] += 1
                    else:
                        z["count_hit_miss"][1] += 1
                    return
            elif j[0].find('servicetype=3') != -1 or j[0].find('servicetype=2') != -1:
                if j[0].find('PolicyMode') != -1:
                    z["live_cuts_vod"][4] += 3
                    z["count"] += 3
                    if i[0].endswith('HIT'):
                        z["count_hit_miss"][8] += 1
                    else:
                        z["count_hit_miss"][9] += 1
                    return
                else:
                    z["live_cuts_vod"][1] += 1
                    z["count"] += 1
                    if i[0].endswith('HIT'):
                        z["count_hit_miss"][2] += 1
                    else:
                        z["count_hit_miss"][3] += 1
                    return


def zero_divizion(a, b):
    """Function for cheking statistics result on division 0. If True - print =0 in result"""
    return a / b if b else 0


def argument(m, a, c, t):
     qa_lab_proc = [
         dict(quality="LV_Dyn_HD_1080_4HP_8000", qa="HD", score=5.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Dyn_HD_1080_4HP_5000", qa="HD", score=4.9, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Dyn_HD_720_4HP_2500", qa="HD", score=4.2, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Dyn_HD_576_4HP_1400", qa="HD", score=3.5, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Dyn_HD_504_4HP_900", qa="HD", score=2.3, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Dyn_HD_432_4HP_500", qa="HD", score=1.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Int_HD_1080_4HP_4300", qa="HD", score=4.5, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Int_HD_1080_4HP_5000", qa="HD", score=5.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Int_HD_432_4HP_500", qa="HD", score=1.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Int_HD_504_4HP_800", qa="HD", score=2.2, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Int_HD_576_4HP_1200", qa="HD", score=3.2, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Int_HD_720_4HP_2000", qa="HD", score=4.2, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Sta_HD_1080_4HP_4000", qa="HD", score=5.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Sta_HD_432_4HP_500", qa="HD", score=1.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Sta_HD_504_4HP_700", qa="HD", score=2.1, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Sta_HD_576_4HP_1000", qa="HD", score=3.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Sta_HD_720_4HP_1800", qa="HD", score=4.2, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Dyn_SD_432_4HP_500", qa="SD", score=1.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Dyn_SD_480_4HP_900", qa="SD", score=2.3, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Dyn_SD_576_4HP_1400", qa="SD", score=3.5, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Dyn_SD_576_4HP_3000", qa="SD", score=4.2, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_SD_240_4HP_512", qa="SD", score=1.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_SD_480_4HP_1600", qa="SD", score=3.3, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_SD_576_4HP_2100", qa="SD", score=4.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Sta_SD_432_4HP_500", qa="SD", score=1.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Sta_SD_480_4HP_700", qa="SD", score=2.1, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Sta_SD_576_4HP_1000", qa="SD", score=3.0, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LV_Sta_SD_576_4HP_2100", qa="SD", score=4.2, count=0,
              count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="HHQ", qa="HD", score=5.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="HQ", qa="SD", score=4.4, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="MQ", qa="SD", score=4.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="LQ", qa="SD", score=1.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="video_HD_AB_4", qa="HD", score=5.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="video_HD_AB_3", qa="HD", score=4.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="video_HD_AB_2", qa="HD", score=3.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="video_HD_AB_1", qa="HD", score=1.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="video_SD_AB_3", qa="SD", score=4.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="video_SD_AB_2", qa="SD", score=2.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0]),
         dict(quality="video_SD_AB_1", qa="SD", score=1.0, count=0, count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              live_cuts_vod=[0, 0, 0, 0, 0, 0])
     ]
     cur_row_p = 0
     with open(os.getcwd() + '\/' + m, newline='') as hcs_1:
         hcs_2 = csv.reader(hcs_1, delimiter=' ')
         for hcs in hcs_2:
             cur_row_p += 1
             if hcs[10].find('.m4v') != -1:  # will analyze only m4v chunks by functions
                 search_all(hcs[3:4], hcs[10:11], qa_lab_proc)
     for i, j in zip(a, qa_lab_proc):
         i["count"].append(j["count"])
         i["count_hit_miss"].append(j["count_hit_miss"])
         i["live_cuts_vod"].append(j["live_cuts_vod"])
     c.append(cur_row_p)
     end_time = datetime.now()
     #print(f'Processor = {proc_num} , Final def, Log file = {m} ',', qa_lab[31]["count"] = ', a[31]["count"], ', qa_lab_proc[31]["count"] =', qa_lab_proc[31]["count"], '  Duration: {}'.format(end_time - start_time))
     print('\r', end='')
     print(f'Processed/Total = {sum(c):,} / {t:,}      Duration: {end_time - start_time}', end='')


if __name__ == '__main__':
    total_r()
    procs = []
    m = Manager()
    qa_lab = [
        m.dict(quality="LV_Dyn_HD_1080_4HP_8000", qa="HD", score=5.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Dyn_HD_1080_4HP_5000", qa="HD", score=4.9, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Dyn_HD_720_4HP_2500", qa="HD", score=4.2, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Dyn_HD_576_4HP_1400", qa="HD", score=3.5, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Dyn_HD_504_4HP_900", qa="HD", score=2.3, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Dyn_HD_432_4HP_500", qa="HD", score=1.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Int_HD_1080_4HP_4300", qa="HD", score=4.5, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Int_HD_1080_4HP_5000", qa="HD", score=5.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Int_HD_432_4HP_500", qa="HD", score=1.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Int_HD_504_4HP_800", qa="HD", score=2.2, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Int_HD_576_4HP_1200", qa="HD", score=3.2, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Int_HD_720_4HP_2000", qa="HD", score=4.2, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Sta_HD_1080_4HP_4000", qa="HD", score=5.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Sta_HD_432_4HP_500", qa="HD", score=1.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Sta_HD_504_4HP_700", qa="HD", score=2.1, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Sta_HD_576_4HP_1000", qa="HD", score=3.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Sta_HD_720_4HP_1800", qa="HD", score=4.2, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Dyn_SD_432_4HP_500", qa="SD", score=1.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Dyn_SD_480_4HP_900", qa="SD", score=2.3, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Dyn_SD_576_4HP_1400", qa="SD", score=3.5, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Dyn_SD_576_4HP_3000", qa="SD", score=4.2, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_SD_240_4HP_512", qa="SD", score=1.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_SD_480_4HP_1600", qa="SD", score=3.3, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_SD_576_4HP_2100", qa="SD", score=4.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Sta_SD_432_4HP_500", qa="SD", score=1.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Sta_SD_480_4HP_700", qa="SD", score=2.1, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Sta_SD_576_4HP_1000", qa="SD", score=3.0, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="LV_Sta_SD_576_4HP_2100", qa="SD", score=4.2, count=m.list(),
               count_hit_miss=m.list(), live_cuts_vod=m.list()),
        m.dict(quality="HHQ", qa="HD", score=5.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="HQ", qa="SD", score=4.4, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="MQ", qa="SD", score=4.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="LQ", qa="SD", score=1.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="video_HD_AB_4", qa="HD", score=5.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="video_HD_AB_3", qa="HD", score=4.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="video_HD_AB_2", qa="HD", score=3.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="video_HD_AB_1", qa="HD", score=1.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="video_SD_AB_3", qa="SD", score=4.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="video_SD_AB_2", qa="SD", score=2.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list()),
        m.dict(quality="video_SD_AB_1", qa="SD", score=1.0, count=m.list(), count_hit_miss=m.list(),
               live_cuts_vod=m.list())
    ]
    cpu = 1
    cur_row = m.list()
    with Pool(cpu) as pool:
        tasks = []
        for m in file:
            task = pool.apply_async(argument, args=(m, qa_lab, cur_row, total_rows))
            tasks.append(task)
        for task in tasks:
            task.get()
    end_time = datetime.now()
    print()
    final_qa = {}
    for i in qa_lab:
        final_qa[i] = i
        final_qa[i]["count"] = sum(i["count"])
        final_qa[i]["count_hit_miss"] = list(map(sum, zip(*i["count_hit_miss"])))
        final_qa[i]["live_cuts_vod"] = list(map(sum, zip(*i["live_cuts_vod"])))

    for i in final_qa:  # count total site vMOS
        if i["count"] > 0:
            profile_vmos_site_score = i['score'] * i['count']
            count_rows = count_rows + i['count']
            total_site_vmos = total_site_vmos + profile_vmos_site_score

    for i in final_qa:  # count HLSv7 CUTS vMOS with divide by HIT/MISS
        if i["live_cuts_vod"][4] > 0:
            profile_vmos_hlsv7_cuts_hit = i['score'] * i['count_hit_miss'][
                8]  # count vmos for one live profile and HIT requests
            profile_vmos_hlsv7_cuts_miss = i['score'] * i['count_hit_miss'][
                9]  # count vmos for one live profile and MISS requests
            profile_vmos_hlsv7_cuts = i['score'] * i['live_cuts_vod'][4]  # count vmos for live one profile

            count_vmos_hlsv7_cuts_rows = count_vmos_hlsv7_cuts_rows + i['live_cuts_vod'][
                4]  # count how many total requests with live services
            count_vmos_hlsv7_cuts_hit_rows = count_vmos_hlsv7_cuts_hit_rows + i['count_hit_miss'][
                8]  # count how many HIT requests with live services
            count_vmos_hlsv7_cuts_miss_rows = count_vmos_hlsv7_cuts_miss_rows + i['count_hit_miss'][
                9]  # count how many MISS requests with live services

            total_vmos_hlsv7_cuts = total_vmos_hlsv7_cuts + profile_vmos_hlsv7_cuts
            # count what is sum of vmos for full live
            total_vmos_hlsv7_cuts_hit = total_vmos_hlsv7_cuts_hit + profile_vmos_hlsv7_cuts_hit
            total_vmos_hlsv7_cuts_miss = total_vmos_hlsv7_cuts_miss + profile_vmos_hlsv7_cuts_miss

    for i in final_qa:
        if i["live_cuts_vod"][5] > 0:  # count HLSv7 VOD vMOS with divide by HIT/MISS
            profile_vmos_hlsv7_vod_hit = i['score'] * i['count_hit_miss'][
                10]  # count vmos for one live profile and HIT requests
            profile_vmos_hlsv7_vod_miss = i['score'] * i['count_hit_miss'][
                11]  # count vmos for one live profile and MISS requests
            profile_vmos_hlsv7_vod = i['score'] * i['live_cuts_vod'][5]  # count vmos for live one profile

            count_vmos_hlsv7_vod_rows = count_vmos_hlsv7_vod_rows + i['live_cuts_vod'][
                5]  # count how many total requests with live services
            count_vmos_hlsv7_vod_hit_rows = count_vmos_hlsv7_vod_hit_rows + i['count_hit_miss'][
                10]  # count how many HIT requests with live services
            count_vmos_hlsv7_vod_miss_rows = count_vmos_hlsv7_vod_miss_rows + i['count_hit_miss'][
                11]  # count how many MISS requests with live services

            total_vmos_hlsv7_vod = total_vmos_hlsv7_vod + profile_vmos_hlsv7_vod  # count what is sum of vmos for full live
            total_vmos_hlsv7_vod_hit = total_vmos_hlsv7_vod_hit + profile_vmos_hlsv7_vod_hit
            total_vmos_hlsv7_vod_miss = total_vmos_hlsv7_vod_miss + profile_vmos_hlsv7_vod_miss

    for i in final_qa:  # count HLSv7 LIVE vMOS with divide by HIT/MISS
        if i["live_cuts_vod"][3] > 0:
            profile_vmos_hlsv7_live_hit = i['score'] * i['count_hit_miss'][6]
            # count vmos for one live profile and HIT requests
            profile_vmos_hlsv7_live_miss = i['score'] * i['count_hit_miss'][
                7]  # count vmos for one live profile and MISS requests
            profile_vmos_hlsv7_live = i['score'] * i['live_cuts_vod'][3]  # count vmos for live one profile

            count_vmos_hlsv7_live_rows = count_vmos_hlsv7_live_rows + i['live_cuts_vod'][
                3]  # count how many total requests with live services
            count_vmos_hlsv7_live_hit_rows = count_vmos_hlsv7_live_hit_rows + i['count_hit_miss'][
                6]  # count how many HIT requests with live services
            count_vmos_hlsv7_live_miss_rows = count_vmos_hlsv7_live_miss_rows + i['count_hit_miss'][
                7]  # count how many MISS requests with live services

            total_vmos_hlsv7_live = total_vmos_hlsv7_live + profile_vmos_hlsv7_live
            # count what is sum of vmos for full live
            total_vmos_hlsv7_live_hit = total_vmos_hlsv7_live_hit + profile_vmos_hlsv7_live_hit
            total_vmos_hlsv7_live_miss = total_vmos_hlsv7_live_miss + profile_vmos_hlsv7_live_miss

    for i in final_qa:  # count DASH CUTS vMOS with divide by HIT/MISS
        if i["live_cuts_vod"][1] > 0:
            profile_vmos_cuts_hit = i['score'] * i['count_hit_miss'][
                2]  # count vmos for one live profile and HIT requests
            profile_vmos_cuts_miss = i['score'] * i['count_hit_miss'][
                3]  # count vmos for one live profile and MISS requests
            profile_vmos_cuts = i['score'] * i['live_cuts_vod'][1]  # count vmos for live one profile

            count_vmos_cuts_rows = count_vmos_cuts_rows + i['live_cuts_vod'][
                1]  # count how many total requests with live services
            count_vmos_cuts_hit_rows = count_vmos_cuts_hit_rows + i['count_hit_miss'][
                2]  # count how many HIT requests with live services
            count_vmos_cuts_miss_rows = count_vmos_cuts_miss_rows + i['count_hit_miss'][
                3]  # count how many MISS requests with live services

            total_vmos_cuts = total_vmos_cuts + profile_vmos_cuts  # count what is sum of vmos for full live
            total_vmos_cuts_hit = total_vmos_cuts_hit + profile_vmos_cuts_hit
            total_vmos_cuts_miss = total_vmos_cuts_miss + profile_vmos_cuts_miss

    for i in final_qa:
        if i["live_cuts_vod"][2] > 0:  # count DASH VOD vMOS with divide by HIT/MISS
            profile_vmos_vod_hit = i['score'] * i['count_hit_miss'][
                4]  # count vmos for one live profile and HIT requests
            profile_vmos_vod_miss = i['score'] * i['count_hit_miss'][
                5]  # count vmos for one live profile and MISS requests
            profile_vmos_vod = i['score'] * i['live_cuts_vod'][2]  # count vmos for live one profile

            count_vmos_vod_rows = count_vmos_vod_rows + i['live_cuts_vod'][
                2]  # count how many total requests with live services
            count_vmos_vod_hit_rows = count_vmos_vod_hit_rows + i['count_hit_miss'][
                4]  # count how many HIT requests with live services
            count_vmos_vod_miss_rows = count_vmos_vod_miss_rows + i['count_hit_miss'][
                5]  # count how many MISS requests with live services

            total_vmos_vod = total_vmos_vod + profile_vmos_vod  # count what is sum of vmos for full live
            total_vmos_vod_hit = total_vmos_vod_hit + profile_vmos_vod_hit
            total_vmos_vod_miss = total_vmos_vod_miss + profile_vmos_vod_miss

    for i in final_qa:  # count DASH LIVE vMOS with divide by HIT/MISS
        if i["live_cuts_vod"][0] > 0:
            profile_vmos_live_hit = i['score'] * i['count_hit_miss'][
                0]  # count vmos for one live profile and HIT requests
            profile_vmos_live_miss = i['score'] * i['count_hit_miss'][
                1]  # count vmos for one live profile and MISS requests
            profile_vmos_live = i['score'] * i['live_cuts_vod'][0]  # count vmos for live one profile

            count_vmos_live_rows = count_vmos_live_rows + i['live_cuts_vod'][
                0]  # count how many total requests with live services
            count_vmos_live_hit_rows = count_vmos_live_hit_rows + i['count_hit_miss'][
                0]  # count how many HIT requests with live services
            count_vmos_live_miss_rows = count_vmos_live_miss_rows + i['count_hit_miss'][
                1]  # count how many MISS requests with live services

            total_vmos_live = total_vmos_live + profile_vmos_live  # count what is sum of vmos for full live
            total_vmos_live_hit = total_vmos_live_hit + profile_vmos_live_hit
            total_vmos_live_miss = total_vmos_live_miss + profile_vmos_live_miss

    # Print result
    print()
    print()
    print('1.   Total vMOS for POP (m4v requests, exclude HLSv3, for HLSv7 multilply 3)')
    print()
    print(f'\033[1m Total vMOS = \033[1;31m {zero_divizion(total_site_vmos, count_rows):.3f} \033[0m')
    print()
    print('2.  vMOS DASH by HIT/MISS for VOD/LIVE/CU  (m4v requests)')
    print()
    print(
        f'\033[1m Dash  vMOS = \033[1;32m {zero_divizion((zero_divizion(total_vmos_vod, count_vmos_vod_rows) + zero_divizion(total_vmos_live, count_vmos_live_rows) + zero_divizion(total_vmos_cuts, count_vmos_cuts_rows)), 3):.3f} \033[0m')
    print()
    print('%5s %8s %5.3f %8s %5.3f %8s %5.3f' % (
        'DASH', 'VOD =', zero_divizion(total_vmos_vod, count_vmos_vod_rows), 'Live =',
        zero_divizion(total_vmos_live, count_vmos_live_rows), 'CU =',
        zero_divizion(total_vmos_cuts, count_vmos_cuts_rows)))
    print('%5s %8s %5.3f %8s %5.3f %8s %5.3f' % (
        'HIT', 'VOD =', zero_divizion(total_vmos_vod_hit, count_vmos_vod_hit_rows), 'Live =',
        zero_divizion(total_vmos_live_hit, count_vmos_live_hit_rows), 'CU =',
        zero_divizion(total_vmos_cuts_hit, count_vmos_cuts_hit_rows)))
    print('%5s %8s %5.3f %8s %5.3f %8s %5.3f' % (
        'MISS', 'VOD =', zero_divizion(total_vmos_vod_miss, count_vmos_vod_miss_rows), 'Live =',
        zero_divizion(total_vmos_live_miss, count_vmos_live_miss_rows), 'CU =',
        zero_divizion(total_vmos_cuts_miss, count_vmos_cuts_miss_rows)))
    print()
    print('3.  vMOS HLSv7 by HIT/MISS for VOD/LIVE/CU  (m4v requests)')
    print()
    print(
        f'\033[1m HLSv7 vMOS = \033[1;32m {zero_divizion((zero_divizion(total_vmos_hlsv7_vod, count_vmos_hlsv7_vod_rows) + zero_divizion(total_vmos_hlsv7_live, count_vmos_hlsv7_live_rows) + zero_divizion(total_vmos_hlsv7_cuts, count_vmos_hlsv7_cuts_rows)), 3):.3f} \033[0m')
    print()
    print('%5s %8s %5.3f %8s %5.3f %8s %5.3f' % (
        'HLSv7', 'VOD =', zero_divizion(total_vmos_hlsv7_vod, count_vmos_hlsv7_vod_rows), 'Live =',
        zero_divizion(total_vmos_hlsv7_live, count_vmos_hlsv7_live_rows), 'CU =',
        zero_divizion(total_vmos_hlsv7_cuts, count_vmos_hlsv7_cuts_rows)))
    print('%5s %8s %5.3f %8s %5.3f %8s %5.3f' % (
        'HIT', 'VOD =', zero_divizion(total_vmos_hlsv7_vod_hit, count_vmos_hlsv7_vod_hit_rows), 'Live =',
        zero_divizion(total_vmos_hlsv7_live_hit, count_vmos_hlsv7_live_hit_rows), 'CU =',
        zero_divizion(total_vmos_hlsv7_cuts_hit, count_vmos_hlsv7_cuts_hit_rows)))
    print('%5s %8s %5.3f %8s %5.3f %8s %5.3f' % (
        'MISS', 'VOD =', zero_divizion(total_vmos_hlsv7_vod_miss, count_vmos_hlsv7_vod_miss_rows), 'Live =',
        zero_divizion(total_vmos_hlsv7_live_miss, count_vmos_hlsv7_live_miss_rows), 'CU =',
        zero_divizion(total_vmos_hlsv7_cuts_miss, count_vmos_hlsv7_cuts_miss_rows)))
    print()
    end_time = datetime.now()
    print('Total script Duration: {}'.format(end_time - start_time))