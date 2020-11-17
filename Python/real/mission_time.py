#!/usr/bin env python
#
###############################################
# AUTHOR: lenonr
#
# VERSION: 0.28
#
# CREATION DATE: 09/09/18
# LAST MODIFICATION: 17/11/18
#
# DESCRIPTION: 
#   Show time profile by type rocket, one by one using local time.
#
# REFERENCE:
#   <https://www.tutorialspoint.com/python/python_date_time.htm>
#   <https://pymotw.com/2/datetime/>
#
# CHECK:
#   Development webcrawler for extracted info of the launches.
#
###############################################
# BODY
import os, sys, time, datetime
from datetime import datetime

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# VARIABLES
var_sleep=0     # 0 = instantaneous # 1 = real time

## functions
sequence_f9_land = [ "LIFTOFF", "Max-Q", "MECO", 
                    "Separation", "SES-1", "Fairing deploy", 
                    "Reentry burn", "SECO-1", "LANDING",
                    "SES-2", "SECO-2", "Deploy's payload's", 
                    "Final mission" ]

countdown_f9_land = [ "000000", "000107", "000233", 
                      "000237", "000245", "000329", 
                      "000617", "000814", "000832", 
                      "002617", "002700", "003201", 
                      "003206" ]

## profile mission
def f9_land(launch_time, hour_launch, minute_launch, second_launch):    
    print ("SEQUENCE STARTED!")
    print ('#' * 20)            

    last_value_list=(len(countdown_f9_land)-1)

    # walk the array
    for x in range(len(sequence_f9_land)):  
        if x==last_value_list:
            print "T+", countdown_f9_land[x][0:2], "h", countdown_f9_land[x][2:4], "m", countdown_f9_land[x][4:6], "s", " |", sequence_f9_land[x]

            break
        else:
            value = countdown_f9_land[x]
            value_x = countdown_f9_land[x+1]

            hours = value[0:2]
            minutes = value[2:4]
            seconds = value[4:6]            

            hours_now_conv = int(hours) * 3600
            minute_now_conv = int(minutes) * 60
            second_now_conv = (hours_now_conv + minute_now_conv + int(seconds))         

            hours_x = value_x[0:2]
            minutes_x = value_x[2:4]
            seconds_x = value_x[4:6]

            hours_now_conv_x = int(hours_x) * 3600
            minute_now_conv_x = int(minutes_x) * 60
            second_now_conv_x = (hours_now_conv_x + minute_now_conv_x + int(seconds_x))         

            next_action = second_now_conv_x - second_now_conv

            if x == 0:
                print "Clock time:",hour_launch,":",minute_launch,":",second_launch
            else:
                sum_hour    = int(hour_launch) + int(hours_x)
                sum_min     = int(minute_launch) + int(minutes_x)
                sum_second  = int(second_launch) + int(seconds_x)

                if sum_second > 59:
                    sum_second = sum_second - 60
                    sum_min = sum_min + 1

                if sum_min > 59:
                    sum_min = sum_min - 60
                    sum_hour = sum_hour + 1

                print "Clock time:",sum_hour,":",sum_min,":", sum_second

            print "T+", hours, "h", minutes, "m", seconds, "s", " |", sequence_f9_land[x]
            print "* Next action: " , hours_x, "h", minutes_x, "m", seconds_x, "s", "-", sequence_f9_land[x+1], "\n"

            if var_sleep==1:
                time.sleep(next_action)

def test_date():
    format="%H:%M:%S" 
    date_now = datetime.strftime(datetime.now(),format)    

    hour_now        = date_now[0:2]
    minute_now      = date_now[3:5]
    second_now      = date_now[6:8]

    print hour_now
    print minute_now
    print second_now

    # launch_time = raw_input("\nLaunch in:")

    launch_time='123003'

    hour_launch = launch_time[0:2]
    minute_launch = launch_time[2:4]
    second_launch = launch_time[4:6]

    print hour_launch
    print minute_launch
    print second_launch

    sum_hour    = int(hour_now) + int(hour_launch)
    sum_min     = int(minute_now) + int(minute_launch)
    sum_second  = int(second_now) + int(second_launch)

    print sum_hour
    print sum_min
    print sum_second

def main():
    # launch()
    # launch_time = raw_input("\nLaunch in:")

    launch_time = "123800"

    hour_launch = launch_time[0:2]
    minute_launch = launch_time[2:4]
    second_launch = launch_time[4:6]

    f9_land(launch_time, hour_launch, minute_launch, second_launch)

    # test_date()

main()

# FOOTER