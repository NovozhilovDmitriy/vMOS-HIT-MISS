import csv
import sys
import os
from multiprocessing import Process, Queue
from datetime import datetime

vod = 0;live = 0;cuts = 0

start_time=datetime.now()

file = sys.argv[1:]

def test(j):
    """Function for count request percentage of VOD/Live/CU and HIT/MISS percentage of this types"""
    global vod; global live; global cuts
    for j in j:
         # if j.find('MISS') != -1:
         #     vod+=1
         # elif j.find('HIT') != -1:
         #     live += 1
         # elif j.find('servicetype=3') != -1:
         #      cuts += 1
         print(j)

def argument(m):
     proc_num = os.getpid()
     print(m, proc_num,end=' \n')
     with open(os.getcwd()+'\/'+m, newline='') as hcs_1:
         hcs_2 = csv.reader(hcs_1, delimiter=' ')
         for hcs in hcs_2:
             test(hcs[3:4])
     end_time = datetime.now()
     print('      Duration: {}'.format(end_time - start_time))

if __name__ == '__main__':
    procs = []
    for m in file:
        proc = Process(target=argument, args=(m,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    end_time = datetime.now()
    print('      Duration: {}'.format(end_time - start_time))
    # print()
    # print('1.   % between VOD/LIVE/CU  (all requests)')
    # print()
    # print('%14s %5.1f %-3s %8s %5.1f %0s %8s %5.1f %0s' % ('VOD =',(vod/(live+vod+cuts)*100),'%','Live =',(live/(live+vod+cuts)*100),'%','CU =',(cuts/(live+vod+cuts)*100),'%'))
    # print()