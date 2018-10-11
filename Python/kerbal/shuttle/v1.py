#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import shuttle

def main():
	turn_start_altitude     = 250						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 90000						# target 
	maxq_begin              = 35000						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	correction_time			= 1							# default
	orientation				= 90						# NORMAL

	shuttle(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation)

main()