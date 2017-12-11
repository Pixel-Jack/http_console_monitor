# Requirements : 
- python 3

# Launch :
`./http_monitor file_path="${PATH}" delay_refresh_general=${DELAY_GEN} threshold=${THRESHOLD} delay_refresh_statistics=${DELAY_STATS} `
Parameters : 
- file_path : path to the log file (string), 
    Default : the last file create in the log directory (created by the launched create_log.py)  
- delay_refresh_general : the delay in second (integer) to refresh the screen
    Default : 2 secs
- threshold: the threshold that will target the alerts about the amount of request during the last 2 min
    Default: 400
- delay_refresh_statistics : the delay in second (integer) to refresh the stats
    Default: 10
  

# Tests :
`./http_monitoring_test`
We launch the monitoring with a threshold of 200.
And we create a file "log_test.log" filled every second with 50 requests for 20 seconds and then 0 for 60 seconds.
So the monitor will be on alert between 10 secs to 130 seconds.   
  
## Launch with random test :
`python3 create_log.py 
python3 http_monitor.py`
The create_log file will create logs with random attacks.

# Improvements :
- allow move with the cursor and scroll in the sections information window
- provide a way to sort the sections information, users information, ip information window
- allow to go up in the Http historic window and that could rewind the graphic in the bottom left
- allow to change refresh freqency inside the monitor
- there a difference between the refreshing of the statistics window and the graphic window. (Even with delay_refresh_general equals delay_refresh_statistics)
- save all info in a log file