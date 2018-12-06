#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newglenn_landingzone

def main():	
	#################################################################################
	target_altitude         = 150000					
	turn_start_altitude     = 2000						
	turn_end_altitude       = (target_altitude/2)	

	maxq_begin				= 28000
	maxq_end				= 30000
	orientation				= 90	
	sound					= False

	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#
	taxa					= 0.20					# Demo Flight			36.000 kg
	#
	#################################################################################


	newglenn_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound)

main()