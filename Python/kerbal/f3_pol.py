#!/usr/bin/env python

## import modules
from base import suborbital

turn_start_altitude     = 1000						# inclination begin
turn_end_altitude       = 45000						# inclination end
target_altitude         = 2929677					# target 
maxq_begin              = 25000						# reduce aceleration stage - begin
maxq_end                = 70000						# reduce aceleration stage - end
correction_time			= 0							# fine tuning orbit - NOT USED HERE
taxa					= 0.15						# Landing first stage in %(Taxa/100)
		# 0 			 : Full Thrust - Not Recovery
		# ( 0.15 |  0.17): Landing insland
		# (-0.17 | +0.20): Landing ocean
		# (-0.15 | +0.21): Surprise me.

orientation				= 360						# TOP POLAR
		# 45  : TOP-NORMAL							# 1.5 hours in the clock.
		# 90  : NORMAL 								# 3 hours in the clock.
		# 135 : NORMAL-DOWN							# 4.5 hours in the clock.
		# 180 : DOWN 								# 6 hours in the clock.
		# 225 : DOWN-ANTINORMAL						# 7.5 hours in the clock.
		# 270 : ANTINORMAL 							# 9 hours in the clock.
		# 315 : ANTINORMAL-TOP						# 10.5 in the clock.
		# 360 : TOP									# 12 hours in the clock.

suborbital(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, taxa, orientation)