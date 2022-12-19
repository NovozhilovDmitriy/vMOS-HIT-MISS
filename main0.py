import os
import sys
from multiprocessing import Manager, Pool

if len(sys.argv) < 5:
    print("\033[1;31m!!!Error!!! \033[0m")
    print("Please set number of CPU what you will use for process script and logs file by example: /home/sshusr/main_mp_prod.py \033[1;31m--cpu 2 --file *.log\033[0m")
    print("Where --cpu or --c set number of CPU, --file or --f hcs log files for analyze")
    sys.exit (1)

if (sys.argv[1] == "--cpu" or sys.argv[1] == "--c"):
    if sys.argv[2] < '1':
        print("\033[1;31m!!!Error!!! \033[0m")
        print("CPU number can't be less then \033[1;31m1\033[0m. Please don't choose CPU more than HW server capacity. It could overload system.")
        sys.exit ()
    else:
        cpu = int(sys.argv[2])
else:
    print("\033[1;31m!!!Error!!! \033[0m")
    print("Please set number of CPU what you will use for process script by : /home/sshusr/main_mp_prod.py \033[1;31m--cpu 2\033[0m --file *.log")
    print("Where --cpu or --c set number of CPU, --file or --f hcs log files for analyze")
    sys.exit (1)

if (sys.argv[3] == "--file" or sys.argv[3] == "--f"):
    file = sys.argv[4]
    if file.endswith('log'):
        file = sys.argv[4:]

    else:
        print("\033[1;31m!!!Error!!! \033[0m")
        print("Log files incorrect extension. Should be \033[1;31m*.log\033[0m")
        sys.exit (1)
else:
    print("\033[1;31m!!!Error!!! \033[0m")
    print("Please set log file for analyze by this way: /home/sshusr/main_mp_prod.py --cpu 2 \033[1;31m--file XXX.log\033[0m")
    print("Where --cpu or --c set number of CPU, --file or --f hcs log files for analyze.")
    print("You can choose multiply file by this way: --file access*.log")
    sys.exit (1)

print(sys.argv[2])


# def ff(c):
#     global b
#     c = c + 1
#     b = c
#     print('def ff, p.id:', os.getpid(), ', b=', b ,',c=', c)

# def f(a):
#     global b
#     b = 0
#     for i in range(2):
#         ff(b)
#     a.value = a.value + b
#     print('def f, p.id:', os.getpid(), ', a=', a.value, ',b=', b)
#
# if __name__ == '__main__':
#     manager = Manager()
#     a = manager.Value('i', 0)
#     cpu = 2
#     with Pool(cpu) as pool:
#         tasks = []
#         for m in range(2):
#             task = pool.apply_async(f, args=(a,))
#             tasks.append(task)
#         for task in tasks:
#             task.get()
#     print('Main, p.id:', os.getpid(), ', a=', a.value)


