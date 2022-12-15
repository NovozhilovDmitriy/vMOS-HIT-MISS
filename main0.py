import os
from multiprocessing import Manager, Pool

def ff(c):
    global b
    c = c + 1
    b = c
    print('def ff, p.id:', os.getpid(), ', b=', b ,',c=', c)

def f(a):
    global b
    b = 0
    for i in range(2):
        ff(b)
    a.value = a.value + b
    print('def f, p.id:', os.getpid(), ', a=', a.value, ',b=', b)

if __name__ == '__main__':
    manager = Manager()
    a = manager.Value('i', 0)
    cpu = 2
    with Pool(cpu) as pool:
        tasks = []
        for m in range(2):
            task = pool.apply_async(f, args=(a,))
            tasks.append(task)
        for task in tasks:
            task.get()
    print('Main, p.id:', os.getpid(), ', a=', a.value)


