#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falcao_landing_zone

def main():	
	#################################################################################
	#
	taxa					= 0.20
	target_altitude         = 150000
	turn_end_altitude       = (target_altitude/1.5)		
	#
	#################################################################################
	#
	#	INCLINATION ORBITS:
	#		UP: 	Inclination - Relative inclination to target
	#		DOWN: 	Inclination + Relative inclination to target
	#
	#################################################################################

	falcao_landing_zone(1000,turn_end_altitude,target_altitude, 20000, 36000, taxa, 90, False)

main()