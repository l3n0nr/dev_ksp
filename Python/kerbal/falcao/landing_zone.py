#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falcao_landing_zone

def main():	
	#################################################################################
	#
	target_altitude         = 150000
	turn_end_altitude       = (target_altitude/1.5)		
	#
	##########################################################################################
	#		X					Value				Profile					Weight orbiter	 #
	##########################################################################################
	#	
	taxa					= 	0.18				# Flight Test Cargo			?? kg		 #
	#
	##########################################################################################

	falcao_landing_zone(2000,turn_end_altitude,target_altitude, 28000, 30000, taxa, 90, True)

main()