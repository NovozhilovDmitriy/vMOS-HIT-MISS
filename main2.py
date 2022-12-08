import csv
import sys
import os
import multiprocessing
from multiprocessing import Process, Queue, Value, Manager
from datetime import datetime

# vod = 0;live = 0;cuts = 0

start_time=datetime.now()

#file = sys.argv[1:]
file = {"test.log","test.log"}

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
     print(m, proc_num,end=' \n')
     with open(os.getcwd()+'\/'+m, newline='') as hcs_1:
         hcs_2 = csv.reader(hcs_1, delimiter=' ')
         # for hcs in hcs_2:
         for j in hcs_2:
             if j[3].find('MISS') != -1:
                 shared = a["vod"][n]
                 shared.append(1)
                 a["vod"][n] = shared
                 print(a)
             # elif j[3].find('HIT') != -1:
             #     a["vod"][n] += 10
#     print (a)
     end_time = datetime.now()
     print('      Duration: {}'.format(end_time - start_time))



if __name__ == '__main__':
    procs = []
    manager = Manager()
    vod_live_cuts = manager.dict()
    i = "vod"
    cpu = 1
    n = 0
    vod_live_cuts[i] = [0] * cpu
    #vod_live_cuts[i] = manager.list()
    for m in file:
        proc = Process(target=argument, args=(m,vod_live_cuts,n))
        n += 1
        procs.append(proc)
        proc.start()
        proc.join()

    end_time = datetime.now()
    print('      Duration: {}'.format(end_time - start_time))
    # print(vod.value,live.value)
    print(vod_live_cuts)
    # print()
    # print('1.   % between VOD/LIVE/CU  (all requests)')
    # print()
    # print('%14s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('VOD =',(vod/(live+vod+cuts)*100),'%','Live =',(live/(live+vod+cuts)*100),'%','CU =',(cuts/(live+vod+cuts)*100),'%'))
    # print()