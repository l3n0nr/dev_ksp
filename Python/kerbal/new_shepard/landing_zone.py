#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newshepard_landingzone

def main():	
	#################################################################################
	#
	target_altitude         = 180000					
	turn_start_altitude     = 2000						
	turn_end_altitude       = (target_altitude/2)	
	maxq_begin				= 28000
	maxq_end				= 30000
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#
	## New Shepard I
	# taxa					= 0.17					# NS Capsula  		+/- 10.105 kg			

	## New Shepard II
	taxa					= 0.19					# NS Capsula 		+/- 10.105 kg
	## 				Separation first stage: 55km

	#
	#################################################################################


	newshepard_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, 90, True)

main()