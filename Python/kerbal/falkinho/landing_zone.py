#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import landing_zone

def main():	
	# target_altitude         = 180000					# target 
	target_altitude         = 150000						# target 

	maxq_begin              = 35000						# reduce aceleration stage - begin	
	maxq_end                = 36000						# reduce aceleration stage - end

	turn_start_altitude     = 100						# inclination begin

	if (target_altitude/2) > 45000:
		turn_end_altitude = 45000
	else:
		turn_end_altitude = (target_altitude/2)

	# turn_end_altitude       = (target_altitude/2)			# inclination end
	# turn_end_altitude       = 45000						# inclination end
	
	# taxa					= 0.15						# dragao  			- 		space station
	taxa					= 0.25						# dragao  			-		docking to manuveur for mun

	orientation				= 90						# NORMAL

	landing_zone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()