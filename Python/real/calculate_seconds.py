#!/usr/bin/env python
import os

# input time
hours = raw_input("Time: ")	

# convert numbers
hours_conv = hours[0:2]
minute = hours[2:4]
second = hours[4:6]

# if hours_conv > 0 and hours_conv < 60:
if hours_conv > 0:
	if minute < 60:
		if second < 60:
			print ("Passou")
		else:
			print ("Digite segundo menor que 60")
	else:
		print ("Digite minuto menor que 60")
else:
	print ("Digite hora menor que 60")

    # 2 hours is 2 hours * (3600 seconds / 1 hour) = 2 * 3600 seconds = 7200 seconds
    # 45 minutes is 45 minutes * (60 seconds / 1 minute) = 45 * 60 seconds = 2700 seconds
    # 45 seconds is 45 seconds * (1 second / 1 second) = 45 * 1 seconds = 45 seconds
    # Adding them all together we have 7200 seconds + 2700 seconds + 45 seconds = 9945 seconds
