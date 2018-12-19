#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newglenn_landingzone

def main():	
	#################################################################################
	#
	turn_start_altitude     = 1000
	target_altitude         = 180000											
	turn_end_altitude       = (target_altitude/1.5)		
	maxq_begin				= 28000
	maxq_end				= 30000
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#
	taxa					= 	0.12				# Demo Flight			36.000 kg
	#
	#################################################################################
	#
	newglenn_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, 90, True)

main()