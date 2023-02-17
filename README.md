# Please read this file carefull. It describe some main steps for correct script work.
# This is test script for check HCS logs and show statistics of the data

main3.py - this script could count HIT/MISS and total chunks+manifest requests for differnt services. 

main-mp-prod.py - this script for multiprocessing counting (suggest no more than 4 cpu). It could count vMOS and HIT-MISS statistics for chunks only and don't show independent HLSv3 (on some linux it could show OpenGL lib error, but counting is correct and error could be ignored)

  Script for count vMOS on MTS Video project. Analyze HCS access.log for count requests with different Video profiles.
  For Dash used current request count (because one chunk duration 2 seconds)
  For HLSv7 use request*3 because one chunk duration 6 seconds
  Script use Python 3.0. The path to this version of Python need to configure here at the beginning of script like:
  /home/uniagent/agent_plugins/OMAgent/modules/python/bin/python
  For executing script use command "/home/sshusr/main_test.py --c 1 --f logfile.log"
  For argument "logfile.log" could use wildcard like "logfile*.log" and all files will be processed one by one
  Script use multiprocessing feature. To start script on several CPU need to add argument like "--c X"
  where X - CPU number. Example: "/home/sshusr/main_test.py --c 4 --f logfile*.log"
  Please focus on Server I/O performance. More CPU will occupation more I/O resources.
  Processing status you can control by progress bar "Processed/Total = 352,202 / 352,202"
  Progress bar will update by files (after one log file finished -> result updated)
  Script provided by Novozhilov Dmitriy (+7 923 733 0029)


After copy files to Linux server, you need confirm that Python version higher 2.7
You can update location from script:

#!/home/uniagent/agent_plugins/OMAgent/modules/python/bin/python

Also you need change this:
# os.getcwd() + '\/' + z, 'r')
to 
# os.getcwd() + '\' + z, 'r')

in two places in each sript before execute.

Also you need done
dos2unix for script before run.
