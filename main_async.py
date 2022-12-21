import csv
import sys
import os
import multiprocessing
from multiprocessing import Process, Queue, Value, Manager
from datetime import datetime
import asyncio

start_time=datetime.now()

#file = sys.argv[1:]
#file = {"test3.log", "test4.log"}
file = {"hcs.log", "hcs1.log", "hcs2.log", "hcs3.log"}
#file = {"hcs.log"}
#file = {"hcs.log", "hcs1.log"}

vod_live_cuts = {}
i = "vod_hit"
ii = "vod_miss"
cpu = 1
vod_live_cuts[i] = [0] * cpu
vod_live_cuts[ii] = [0] * cpu
n = 0


async def argument(m, a):
     print(f'Log file = {m} , INPUT_1  : a[vod_hit] = ', a["vod_hit"], ', a[vod_miss] = ', a["vod_miss"])
     with open(os.getcwd() + '\/' + m, newline='') as hcs_1:
         hcs_2 = csv.reader(hcs_1, delimiter=' ')
         for j in hcs_2:
             if j[3].find('MISS') != -1:
                 a["vod_miss"][n] += 1
             elif j[3].find('HIT') != -1:
                 a["vod_hit"][n] += 1
     print(f'Log file = {m}', 'INPUT_2  : a[vod_hit] = ', a["vod_hit"], ', a[vod_miss] = ', a["vod_miss"])
     print()


async def main():
    tasks = [asyncio.create_task(argument(m, vod_live_cuts)) for m in file]
    await asyncio.gather(*tasks)

if __name__=="__main__":
    asyncio.run(main())


end_time = datetime.now()
print('                                                update - ', vod_live_cuts["vod_hit"], vod_live_cuts["vod_miss"], '       Duration: {}'.format(end_time - start_time))
