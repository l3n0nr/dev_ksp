#!/usr/bin env python
#
###############################################
# AUTHOR: lenonr
#
# VERSION: 0.10
#
# CREATION DATE: 09/09/18
# LAST MODIFICATION: 09/09/18
#
# DESCRIPTION: 
#   Show time profile by type rocket, one by one using local time.
#
###############################################
# BODY
import os, sys, time

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# VARIABLES
var_sleep=0     # 0 = disabled # 1 = enable
time_hours   = 0
time_minutes = 0
time_seconds = 0

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
def f9_land():
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

            print "T+", hours, "h", minutes, "m", seconds, "s", " |", sequence_f9_land[x]
            print "* Next action: " , hours_x, "h", minutes_x, "m", seconds_x, "s", "-", sequence_f9_land[x+1], "\n"

            if var_sleep==1:
                time.sleep(next_action)

def main():
    rocket_name = raw_input("\nThe time for launch: ")           

    time_hours   = rocket_name[0:2]
    time_minutes = rocket_name[2:4]
    time_seconds = rocket_name[4:6]    

    f9_land()

main()

# FOOTER