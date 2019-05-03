#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falcao_landing_zone

def main():	
	#################################################################################
	#
	target_altitude         = 180000
	turn_end_altitude       = (target_altitude/1.5)		
	#
	##########################################################################################
	#		X					Value				Profile					Weight orbiter	 #
	##########################################################################################
	#	
	taxa					= 	0.21				# Flight Test Cargo			141.000 kg
	# Adicionar pernas / alterar altura 

	#
	##########################################################################################

	falcao_landing_zone(2000,turn_end_altitude,target_altitude, 28000, 30000, taxa, 90, True)

main()