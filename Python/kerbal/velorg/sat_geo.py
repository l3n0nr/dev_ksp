#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import velorg

def main():
	########################################################################################
	turn_start_altitude     = 16000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 100000					# target 
	maxq_begin              = 30000						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	########################################################################################

	velorg(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, 90)

main()