#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newglenn_landingzone

def main():	
	#################################################################################
	turn_start_altitude     = 1000						
	maxq_begin				= 32000
	maxq_end				= 36000
	sound					= False
	#################################################################################
	
	target_altitude         = 150000				
	turn_end_altitude       = (target_altitude/1.5)

	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#
	taxa					= 0.15					# Demo Flight			36.000 kg
	#
	#################################################################################


	newglenn_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, 90, sound)

main()