#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import landing_zone

def main():	
	target_altitude         = 180000					# target 
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	turn_start_altitude     = 100						# inclination begin
	turn_end_altitude       = target_altitude			# inclination end
	
	taxa					= 0.15						# dragao NR

	orientation				= 90						# NORMAL

	landing_zone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()