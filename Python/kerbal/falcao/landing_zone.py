#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falcao_landing_zone

def main():	
	#################################################################################
	#
	orientation 			= 90
	target_altitude         = 180000										
	turn_end_altitude       = (target_altitude/1.5)		
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#	
	taxa					= 0.20				# Flight Test		-		+/- ??? kg	
	#	
	#################################################################################

	falcao_landing_zone(2000,turn_end_altitude,target_altitude, 28000, 30000, taxa, orientation, True)

main()