#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import shuttle

def main():
	#######################################################################################
	turn_start_altitude     = 100						# inclination begin - meters
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 90000						# target - min. altitude
	maxq_begin              = 35000						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	orientation				= 1
	#######################################################################################

	shuttle(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, orientation, 90)

main()