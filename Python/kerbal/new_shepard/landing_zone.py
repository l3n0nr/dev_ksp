#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newshepard_landingzone

def main():	
	#################################################################################
	target_altitude         = 180000					
	turn_start_altitude     = 2000						
	turn_end_altitude       = (target_altitude/2)	

	maxq_begin				= 28000
	maxq_end				= 30000
	orientation				= 90	

	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#
	taxa					= 0.17					# only test landing zone!
	#
	#################################################################################


	newshepard_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()