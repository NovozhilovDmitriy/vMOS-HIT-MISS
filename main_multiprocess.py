import csv
import os
from multiprocessing import Process, Queue, Value, Manager, Pool
from datetime import datetime

start_time=datetime.now()

#file = sys.argv[1:]
#file = {"test3.log", "test4.log"}
file = {"hcs.log", "hcs1.log", "hcs2.log", "hcs3.log"}
#file = {"hcs.log"}

def argument(m, a):
     proc_num = os.getpid()
     a_temp_m = 0
     a_temp_h = 0
     print(f'Processor = {proc_num} , Log file = {m}  , INPUT_1  : a[vod_hit] = ', a["vod_hit"], ', a[vod_miss] = ', a["vod_miss"], ' a_temp_h  = ', a_temp_h, ', a_temp_m  = ', a_temp_m)
     with open(os.getcwd() + '\/' + m, newline='') as hcs_1:
         hcs_2 = csv.reader(hcs_1, delimiter=' ')
         for j in hcs_2:
             if j[3].find('MISS') != -1:
                 a_temp_m = a_temp_m + 1
             elif j[3].find('HIT') != -1:
                 a_temp_h = a_temp_h + 1
     print(f'Log file = {m}', f'a[vod_hit] = ', a["vod_hit"],f', a_temp_h=', a_temp_h, f', a[vod_miss] =', a["vod_miss"], f', a_temp_m=', a_temp_m)
     print(f'Log file = {m}', 'INPUT_2  : a[vod_hit] = ', a["vod_hit"], ', a[vod_miss] = ', a["vod_miss"])
     print(f'Log file = {m}', 'OUTPUT : a_temp_h  = ', a_temp_h, ', a_temp_m  = ', a_temp_m)
     a["vod_miss"].append(a_temp_m)
     a["vod_hit"].append(a_temp_h)
     end_time = datetime.now()
     print(f'Log file = {m} ', ' Processor = ', proc_num, ', vod_live_cuts =', a["vod_hit"], a["vod_miss"], '      Duration: {}'.format(end_time - start_time))
     print()


if __name__ == '__main__':
    procs = []
    manager = Manager()
    vod_live_cuts = manager.dict()
    i = "vod_hit"
    ii = "vod_miss"
    cpu = 1
    vod_live_cuts[i] = manager.list()
    vod_live_cuts[ii] = manager.list()
    with Pool(cpu) as pool:
        tasks = []
        for m in file:
            task = pool.apply_async(argument, args=(m, vod_live_cuts))
            tasks.append(task)
        for task in tasks:
            task.get()
    end_time = datetime.now()
    print('                                                update - ', vod_live_cuts["vod_hit"], vod_live_cuts["vod_miss"], '       Duration: {}'.format(end_time - start_time))