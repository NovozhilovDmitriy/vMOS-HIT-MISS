import csv
import sys
import os
import multiprocessing
from multiprocessing import Process, Queue, Value, Manager
from datetime import datetime

start_time=datetime.now()

#file = sys.argv[1:]
#file = {"test3.log", "test4.log"}
file = {"hcs.log", "hcs1.log", "hcs2.log", "hcs3.log"}
#file = {"test.log", "test2.log"}

# def test(j,vod,live):
#     """Function for count request percentage of VOD/Live/CU and HIT/MISS percentage of this types"""
#     for j in j:
#          if j.find('MISS') != -1:
#              vod.value+=1
#          elif j.find('HIT') != -1:
#              live.value += 1
#          # elif j.find('servicetype=3') != -1:
#          #      cuts += 1
#          # return(vod,live,cuts)
#          # print(j)


def argument(m, a, n):
     proc_num = os.getpid()
     a_temp_m = a["vod_miss"]
     a_temp_h = a["vod_hit"]
     print(f'Processor = {proc_num} , Log file = {n} , {m}  , INPUT_1  : a[vod_hit] = ', a["vod_hit"], ', a[vod_miss] = ', a["vod_miss"], ' a_temp_h  = ', a_temp_h, ', a_temp_m  = ', a_temp_m)
     with open(os.getcwd() + '\/' + m, newline='') as hcs_1:
         hcs_2 = csv.reader(hcs_1, delimiter=' ')
         # for hcs in hcs_2:
         for j in hcs_2:
             if j[3].find('MISS') != -1:
                 #a_temp_m = a["vod_miss"]
                 a_temp_m[n] = a_temp_m[n] + 1
                 #a["vod_miss"][n] += 1
                 #a["vod_miss"] = a_temp_m
                 end_time = datetime.now()
                 #print(f'Log file = {n} , ', m, ', Processor = ', proc_num, ', update - ', j[3][-4:], ' - ', a_temp_m,
                 #      '      Duration: {}'.format(end_time - start_time))
             elif j[3].find('HIT') != -1:
                 #a_temp_h = a["vod_hit"]
                 a_temp_h[n] = a_temp_h[n] + 1
                 #a["vod_hit"][n] += 1
                 #a["vod_hit"] = a_temp_h
                 end_time = datetime.now()
                 #print(f'Log file = {n} , ', m, ', Processor = ', proc_num, ', update - ', j[3][-4:], ' - ', a_temp_h,
                 #      '      Duration: {}'.format(end_time - start_time))
     print(f'Log file = {n} , ', m, f'a[vod_hit][{n}] = ', a["vod_hit"][n],f', a_temp_h[{n}]=', a_temp_h[n], f', a[vod_miss][{n}] =', a["vod_miss"][n], f', a_temp_m[{n}]=', a_temp_m[n])
     print(f'Log file = {n} , ', m, 'INPUT_2  : a[vod_hit] = ', a["vod_hit"], ', a[vod_miss] = ', a["vod_miss"])
     print(f'Log file = {n} , ', m, 'OUTPUT : a_temp_h  = ', a_temp_h, ', a_temp_m  = ', a_temp_m)
     a["vod_miss"][n] = a_temp_m[n]
     a["vod_hit"][n] = a_temp_h[n]
     end_time = datetime.now()
     #print(f'Log file = {n} , ', m, ', Processor = ', proc_num, ', vod_live_cuts =', a, '      Duration: {}'.format(end_time - start_time))
     print()


if __name__ == '__main__':
    procs = []
    manager = Manager()
    vod_live_cuts = manager.dict()
    i = "vod_hit"
    ii = "vod_miss"
    cpu = 1
    n = 1
    # vod_live_cuts[i] = [0] * cpu
    # vod_live_cuts[ii] = [0] * cpu
    vod_live_cuts[i] = manager.list([0] * cpu)
    vod_live_cuts[ii] = manager.list([0] * cpu)
    for m in file:
        proc = Process(target=argument, args=(m, vod_live_cuts, (n-1)))
        procs.append(proc)
        proc.start()
        if n >= cpu:
            n = 1
            proc.join()
        else:
            n += 1
        #proc.join()
    [proc.join() for proc in procs]
    end_time = datetime.now()
    print('                                                update - ', vod_live_cuts["vod_hit"], vod_live_cuts["vod_miss"], '       Duration: {}'.format(end_time - start_time))
    #print('Total      Duration: {}'.format(end_time - start_time))
    #print(vod_live_cuts)
    [proc.close() for proc in procs]