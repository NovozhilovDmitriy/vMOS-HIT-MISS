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
             test(hcs[3:4], a_temp_m, a_temp_h, cur_row_p)
     # end_time = datetime.now()
     # print(f'Processor = {proc_num} , Log file = {m}', f'After loop a_temp_h=', a_temp_h, f', a_temp_m=', a_temp_m, '      Duration: {}'.format(end_time - start_time))
     # print(f'Processor = {proc_num} , Log file = {m}', 'INPUT_2  : a[vod_hit] = ', a["vod_hit"], ', a[vod_miss] = ', a["vod_miss"], '      Duration: {}'.format(end_time - start_time))
     # print(f'Processor = {proc_num} , Log file = {m}', 'OUTPUT : a_temp_h  = ', a_temp_h, ', a_temp_m  = ', a_temp_m, '      Duration: {}'.format(end_time - start_time))
     a["vod_miss"].append(a_temp_m)
     a["vod_hit"].append(a_temp_h)
     c.append(cur_row_p)
     end_time = datetime.now()
     #print(f'Processor = {proc_num} , Final def, Log file = {m} ', ' Processor = ', proc_num, sum(c), ', vod_live_cuts =', a["vod_hit"], a["vod_miss"], '      Duration: {}'.format(end_time - start_time))
     print('\r', end='')
     print(f'Processed/Total = {sum(c):,} / {t:,}      Duration: {end_time - start_time}', end='')


if __name__ == '__main__':
    total_r()
    procs = []
    manager = Manager()
    vod_live_cuts = manager.dict()
    i = "vod_hit"
    ii = "vod_miss"
    cpu = 1
    vod_live_cuts[i] = manager.list()
    vod_live_cuts[ii] = manager.list()
    cur_row = manager.list()
    with Pool(cpu) as pool:
        tasks = []
        for m in file:
            task = pool.apply_async(argument, args=(m, vod_live_cuts, cur_row, total_rows))
            tasks.append(task)
        for task in tasks:
            task.get()
    end_time = datetime.now()
    print()
    print('                                                update - ', sum(vod_live_cuts["vod_hit"]), sum(vod_live_cuts["vod_miss"]), '       Duration: {}'.format(end_time - start_time))