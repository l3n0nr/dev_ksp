#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falkinho

def main():
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	# target_altitude         = 150000					# target 
	target_altitude         = 2862000					# GEO - Kerbin
		# Orbit period: 04 hours - 03 satellites
		
	#						  2.970,608					# MUN 	 - GEO NOT POSSIBLE
	#						  1.797,41					# MUN 	 - Semi-synchronous orbit - many satellites
	#						  357.94					# MINMUS - Synchronous orbit

	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 70000						# reduce aceleration stage - end
	correction_time         = 1							# time correction before shutdown engine					
	taxa					= 0.115						# Landing first stage
	orientation				= 90						# NORMAL
			# 45  : TOP-NORMAL							# 1.5 hours in the clock.
			# 90  : NORMAL 								# 3 hours in the clock.
			# 135 : NORMAL-DOWN							# 4.5 hours in the clock.
			# 180 : DOWN 								# 6 hours in the clock.
			# 225 : DOWN-ANTINORMAL						# 7.5 hours in the clock.
			# 270 : ANTINORMAL 							# 9 hours in the clock.
			# 315 : ANTINORMAL-TOP						# 10.5 in the clock.
			# 360 : TOP									# 12 hours in the clock.

	falkinho(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, taxa, orientation)

main()