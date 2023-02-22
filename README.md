#  This is the test scripts for check HCS logs and show different statistics

## 1. Script #1
### main3.py
this script could count HIT/MISS and total chunks+manifest requests for different services.(DASH/HLSv7/HLSv3) 
### Enviroment
Please check Environment section of next script.


## 2. Script #2
### main-mp-prod.py 
this script for multiprocessing counting (suggest no more than 4 cpu). It could count vMOS and HIT-MISS statistics for chunks only and don't show independent HLSv3 (on some linux it could show OpenGL lib error, but counting is correct and error could be ignored)

### Description
Script for count vMOS on MTS Video project. Analyze HCS access.log for count requests with different Video profiles.
- For Dash used current request count (because one chunk duration 2 seconds)
- For HLSv7 use request*3 because one chunk duration 6 seconds

### Enviroment
Script use Python 3.0. 
The path to this version of Python need to configure here at the beginning of script like:
```
/home/uniagent/agent_plugins/OMAgent/modules/python/bin/python
```
- You need done 'dos2unix' for script before run. (some time it could show some hidden symbol error after copy file)
- For correct execute script in Lunix you need change this:
```
os.getcwd() + '\/' + z, 'r')
```
   to 
```  
os.getcwd() + '/' + z, 'r')
```
   in two places in each script before execute.
### Usage

- For executing script write script location from the log folder. Important - you need execute script
from the log folder (dont try to write path of logs files)
``` python
/home/sshusr/main_test.py --c 1 --f logfile.log
```
- For argument "logfile.log" could use wildcard like "logfile*.log" and all files will be processed one by one
Script use multiprocessing feature. 
- To start script on several CPU need to add argument like "--c X" where X - CPU number. Each log file will presess new CPU.
If you choose 1 log file, 2-4 CPU will not improve time at all.
``` python
/home/sshusr/main_test.py --c 4 --f logfile*.log
```
- Please focus on Server I/O performance. More CPU will occupation more I/O resources. Experience show that no need chose more
than 4 CPU, it will not improve time.
- Processing status you can control by progress bar. Progress bar will update by files (after one log file finished -> result updated)
``` python
Processed/Total = 352,202 / 352,202
```

### Unsolved issues
- Some Linux server could generate error of some lib. It will not influence of script result, and you can ignore it.
``` python
#  Example
ERROR:root:code for hash blake2b was not found.
Traceback (most recent call last):
  File "/home/uniagent/agent_plugins/OMAgent/modules/python/lib/python3.8/hashlib.py", line 251, in <module>
    globals()[__func_name] = __get_hash(__func_name)
  File "/home/uniagent/agent_plugins/OMAgent/modules/python/lib/python3.8/hashlib.py", line 120, in __get_builtin_constructor
    raise ValueError('unsupported hash type ' + name)
ValueError: unsupported hash type blake2b
```
### Contribution
- Script provided by Novozhilov Dmitriy (+7 923 733 0029)


