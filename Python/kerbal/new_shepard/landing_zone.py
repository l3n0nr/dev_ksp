#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newshepard_landingzone

def main():	
	#################################################################################
	#
	turn_end_altitude       = (target_altitude/2)	
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#
	## New Shepard I
	# taxa					= 0.17					# NS Capsula  		+/- 10.105 kg			
	#
	## New Shepard II
	taxa					= 0.19					# NS Capsula 		+/- 10.105 kg
	## 				Separation first stage: 55km
	#
	#################################################################################


	newshepard_landingzone(2000,turn_end_altitude,180000, 28000, 30000, taxa, 90, True)

main()