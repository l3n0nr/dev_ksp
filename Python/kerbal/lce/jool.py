#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import lce

def main():	
	########################################################################################
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end	
	maxq_begin              = 35999						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	########################################################################################

	target_altitude         = 120000					# JUNO I / POL I / VOYAGER III
	# target_altitude         = 80000						# LAYTHE CLIP I

	lce(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, 90)

main()