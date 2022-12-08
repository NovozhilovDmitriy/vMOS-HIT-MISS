import csv
import sys
import os
import multiprocessing
from multiprocessing import Process, Queue, Value, Manager
from datetime import datetime

start_time=datetime.now()

#file = sys.argv[1:]
file = {"test.log","test2.log"}
#file = {"hcs.log","hcs1.log"}

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

def argument(m,a,n):
     proc_num = os.getpid()
     with open(os.getcwd()+'\/'+m, newline='') as hcs_1:
         hcs_2 = csv.reader(hcs_1, delimiter=' ')
         # for hcs in hcs_2:
         for j in hcs_2:
             if j[3].find('MISS') != -1:
                 a_temp_m = a["vod_miss"]
                 a_temp_m[n] += 1
                 a["vod_miss"] = a_temp_m
                 #print(a)
             elif j[3].find('HIT') != -1:
                 a_temp_h = a["vod_hit"]
                 a_temp_h[n] += 1
                 a["vod_hit"] = a_temp_h
                 #print(a)
     print(f'Log file = {n}',m, 'Processor = ',proc_num, end=' \n')
     print (a)
     end_time = datetime.now()
     print('      Duration: {}'.format(end_time - start_time))
     print()

if __name__ == '__main__':
    procs = []
    manager = Manager()
    vod_live_cuts = manager.dict()
    i = "vod_hit"
    ii = "vod_miss"
    cpu = 2
    n = 0
    vod_live_cuts[i] = [0] * cpu
    vod_live_cuts[ii] = [0] * cpu
    for m in file:
        proc = Process(target=argument, args=(m,vod_live_cuts,n))
        n += 1
        procs.append(proc)
        proc.start()
        #proc.join()
    [proc.join() for proc in procs]
    end_time = datetime.now()
    print('Total      Duration: {}'.format(end_time - start_time))
    print(vod_live_cuts)
    [proc.close() for proc in procs]