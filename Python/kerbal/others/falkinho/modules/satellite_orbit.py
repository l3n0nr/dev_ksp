#!/usr/bin/env python

## import modules
from base import launch

turn_start_altitude     = 1000						# inclination begin
turn_end_altitude       = 45000						# inclination end
target_altitude         = 2863330					# target 
						# 2863330 - sincronized orbit	
maxq_begin              = 25000						# reduce aceleration stage - begin
maxq_end                = 70000						# reduce aceleration stage - end
correction_time         = 5							# time correction before shutdown final engine
taxa					= 0							# Landing first stage in %(Taxa/100). "0" if not necessary
orientation				= 90						# 90 - NORMAL | 180 - DOWN | 270 - ANTINORMAL | 360 - TOP

launch(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, taxa, orientation)