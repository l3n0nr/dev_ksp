#!/usr/bin/env python

## import modules
from base import launch

turn_start_altitude 	= 1000
turn_end_altitude 		= 45000
target_altitude 		= 140000
maxq_begin 				= 20000
maxq_end   				= turn_end_altitude
correction_time 		= 0.01

# start script
launch(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time)