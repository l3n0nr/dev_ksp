#!/usr/bin/env python

## import modules
import sys
sys.path.insert(0, '../')
from base import saturninho

turn_start_altitude     = 1000						# inclination begin
turn_end_altitude       = 45000						# inclination end
target_altitude         = 150000					# target 
maxq_begin              = 30000						# reduce aceleration stage - begin
maxq_end                = turn_end_altitude			# reduce aceleration stage - end
correction_time         = 1							# time correction before shutdown engine
taxa					= 0							# Landing first stage in %(Taxa/100)
orientation				= 90						# 90 - NORMAL | 180 - DOWN | 270 - ANTINORMAL | 360 - TOP

saturninho(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, taxa, orientation)