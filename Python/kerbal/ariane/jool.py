#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ariane

def main():
	#######################################################################################
	turn_start_altitude     = 3000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	maxq_begin              = 35999						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	#######################################################################################

	# target_altitude         = 105000					# pioner jool
	# target_altitude         = 80000					# relay'sat jool
	target_altitude         = 80000						# relay'sat laythe

	ariane(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, 90)

main()