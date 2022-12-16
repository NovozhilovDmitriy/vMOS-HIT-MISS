import csv
import os
import sys
from multiprocessing import Manager, Pool
from datetime import datetime
import time

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
     proc_num = os.getpid()
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
     with open(os.getcwd() + '\/' + m, newline='') as hcs_1:
         hcs_2 = csv.reader(hcs_1, delimiter=' ')
         for hcs in hcs_2:
             if hcs[10].find('.m4v') != -1:  # will analyze only m4v chunks by functions
                 search_all(hcs[3:4], hcs[10:11], qa_lab_proc)
     for i, j in zip(a, qa_lab_proc):
         i["count"].append(j["count"])
         i["count_hit_miss"].append(j["count_hit_miss"])
         i["live_cuts_vod"].append(j["live_cuts_vod"])
     #c.append(cur_row_p)
     end_time = datetime.now()
     print(f'Processor = {proc_num} , Final def, Log file = {m} ',', qa_lab[31]["count"] = ', a[31]["count"], ', qa_lab_proc[31]["count"] =', qa_lab_proc[31]["count"], '  Duration: {}'.format(end_time - start_time))
     #print('\r', end='')
     #print(f'Processed/Total = {sum(c):,} / {t:,}      Duration: {end_time - start_time}', end='')


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
    cpu = 4
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
    # for i in qa_lab:
    #     print('qa_lab[0]["count"] = ', i["count"], 'qa_lab[0]["count_hit_miss"] = ', i["count_hit_miss"], '       Duration: {}'.format(end_time - start_time))
    print('qa_lab[31]["count"] = ', qa_lab[31]["count"])
    print('qa_lab[31]["count"] = ', sum(qa_lab[31]["count"]))
    print('qa_lab[31]["count_hit_miss"] = ', qa_lab[31]["count_hit_miss"])
    print('qa_lab[31]["count_hit_miss"] = ', list(map(sum, zip(*qa_lab[31]["count_hit_miss"]))))
    print('qa_lab[31]["live_cuts_vod"] = ', qa_lab[31]["live_cuts_vod"])
    print('qa_lab[31]["live_cuts_vod"] = ', list(map(sum, zip(*qa_lab[31]["live_cuts_vod"]))))
    print('       Duration: {}'.format(end_time - start_time))