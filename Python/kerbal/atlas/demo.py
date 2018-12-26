#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import atlas

def main():
	######################################################################################
	turn_start_altitude     = 2000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 135000					# target 
	maxq_begin              = 30000						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	orientation				= 90						# NORMAL
	######################################################################################

	atlas(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, orientation)

main()