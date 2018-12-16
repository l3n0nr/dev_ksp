#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ariane

def main():
	#######################################################################################
	turn_start_altitude     = 2000						# inclination begin
	turn_end_altitude       = 45000						# inclination end	
	maxq_begin              = 34000						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	#######################################################################################	

	# Explorer I - Asteroid I
	orientation 			= 180
	target_altitude         = 100000

	ariane(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, orientation)

main()