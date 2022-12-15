import csv
import os
import sys
from multiprocessing import Manager, Pool
from datetime import datetime

start_time=datetime.now()

cur_row = 0; total_rows = 0

file = sys.argv[1:]

#  Import arguments like files for next processing
file = sys.argv[1:]


def total_r():
    global total_rows
    for m in file:  # Counting how many rows totally we will have for this process#
       total_rows = total_rows + sum(1 for line in open(os.getcwd() + '\/' + m, 'r'))
       print('\r', end='')
       end_time = datetime.now()
       print(f'Total rows = {total_rows:,}      Duration: {end_time - start_time}', end='')
    print()


def search_qa(j,qa):
    """Function for counting Total POP vmos quality from logs,
    include only m4v and for HLSv7*3, because 1*hlsv7 chunk = 3* dash chunk"""
    for z in qa:
        if j[0].find(z["quality"]) != -1:
            if j[0].find('PolicyMode') != -1:
                z["count"].append(3)
            else:
                z["count"].append(1)
            return


def test(j,a_m, a_h, c_r):
    """Function for count request percentage of VOD/Live/CU and HIT/MISS percentage of this types"""
    global a_temp_m; global a_temp_h; global cur_row_p
    for j in j:
         if j.endswith('MISS'):
             a_m = a_m + 1
             c_r = c_r + 1
         elif j.endswith('HIT'):
             a_h = a_h + 1
             c_r = c_r + 1
    a_temp_m = a_m
    a_temp_h = a_h
    cur_row_p = c_r

def argument(m, a, c, t):
     proc_num = os.getpid()
     global a_temp_m; global a_temp_h; global cur_row_p
     a_temp_m = 0
     a_temp_h = 0
     cur_row_p = 0
     # end_time = datetime.now()
     # print(f'Processor = {proc_num} , Log file = {m}  , INPUT_1  : a[vod_hit] = ', a["vod_hit"], ', a[vod_miss] = ', a["vod_miss"], ' a_temp_h  = ', a_temp_h, ', a_temp_m  = ', a_temp_m, '      Duration: {}'.format(end_time - start_time))
     with open(os.getcwd() + '\/' + m, newline='') as hcs_1:
         hcs_2 = csv.reader(hcs_1, delimiter=' ')
         for hcs in hcs_2:
             #test(hcs[3:4], a_temp_m, a_temp_h, cur_row_p)
            search_qa(hcs[10:11], a)
     # end_time = datetime.now()
     # print(f'Processor = {proc_num} , Log file = {m}', f'After loop a_temp_h=', a_temp_h, f', a_temp_m=', a_temp_m, '      Duration: {}'.format(end_time - start_time))
     # print(f'Processor = {proc_num} , Log file = {m}', 'INPUT_2  : a[vod_hit] = ', a["vod_hit"], ', a[vod_miss] = ', a["vod_miss"], '      Duration: {}'.format(end_time - start_time))
     # print(f'Processor = {proc_num} , Log file = {m}', 'OUTPUT : a_temp_h  = ', a_temp_h, ', a_temp_m  = ', a_temp_m, '      Duration: {}'.format(end_time - start_time))
     # a["vod_miss"].append(a_temp_m)
     # a["vod_hit"].append(a_temp_h)
     # c.append(cur_row_p)
     end_time = datetime.now()
     #print(f'Processor = {proc_num} , Final def, Log file = {m} ', ' Processor = ', proc_num, sum(c), ', vod_live_cuts =', a["vod_hit"], a["vod_miss"], '      Duration: {}'.format(end_time - start_time))
     print('\r', end='')
     print(f'Processed/Total = {sum(c):,} / {t:,}      Duration: {end_time - start_time}', end='')


if __name__ == '__main__':
    total_r()
    procs = []
    m = Manager()
    qa_lab = [
        m.dict(quality="LV_Dyn_HD_1080_4HP_8000", qa="HD", score=5.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Dyn_HD_1080_4HP_5000", qa="HD", score=4.9, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Dyn_HD_720_4HP_2500", qa="HD", score=4.2, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Dyn_HD_576_4HP_1400", qa="HD", score=3.5, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Dyn_HD_504_4HP_900", qa="HD", score=2.3, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Dyn_HD_432_4HP_500", qa="HD", score=1.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Int_HD_1080_4HP_4300", qa="HD", score=4.5, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Int_HD_1080_4HP_5000", qa="HD", score=5.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Int_HD_432_4HP_500", qa="HD", score=1.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Int_HD_504_4HP_800", qa="HD", score=2.2, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Int_HD_576_4HP_1200", qa="HD", score=3.2, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Int_HD_720_4HP_2000", qa="HD", score=4.2, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Sta_HD_1080_4HP_4000", qa="HD", score=5.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Sta_HD_432_4HP_500", qa="HD", score=1.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Sta_HD_504_4HP_700", qa="HD", score=2.1, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Sta_HD_576_4HP_1000", qa="HD", score=3.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Sta_HD_720_4HP_1800", qa="HD", score=4.2, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Dyn_SD_432_4HP_500", qa="SD", score=1.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Dyn_SD_480_4HP_900", qa="SD", score=2.3, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Dyn_SD_576_4HP_1400", qa="SD", score=3.5, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Dyn_SD_576_4HP_3000", qa="SD", score=4.2, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_SD_240_4HP_512", qa="SD", score=1.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_SD_480_4HP_1600", qa="SD", score=3.3, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_SD_576_4HP_2100", qa="SD", score=4.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Sta_SD_432_4HP_500", qa="SD", score=1.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Sta_SD_480_4HP_700", qa="SD", score=2.1, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Sta_SD_576_4HP_1000", qa="SD", score=3.0, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LV_Sta_SD_576_4HP_2100", qa="SD", score=4.2, count=m.list(),
               count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="HHQ", qa="HD", score=5.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="HQ", qa="SD", score=4.4, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="MQ", qa="SD", score=4.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="LQ", qa="SD", score=1.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="video_HD_AB_4", qa="HD", score=5.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="video_HD_AB_3", qa="HD", score=4.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="video_HD_AB_2", qa="HD", score=3.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="video_HD_AB_1", qa="HD", score=1.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="video_SD_AB_3", qa="SD", score=4.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="video_SD_AB_2", qa="SD", score=2.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0]),
        m.dict(quality="video_SD_AB_1", qa="SD", score=1.0, count=m.list(), count_hit_miss=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               live_cuts_vod=[0, 0, 0, 0, 0, 0])
    ]
    vod_live_cuts = m.dict()
    i = "vod_hit"
    ii = "vod_miss"
    cpu = 1
    vod_live_cuts[i] = m.list()
    vod_live_cuts[ii] = m.list()
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
    print(qa_lab[0]["count"], '       Duration: {}'.format(end_time - start_time))