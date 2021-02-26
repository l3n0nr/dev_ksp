#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newglenn

def main():	
	#################################################################################
	#
	orientation 			= 90
	target_altitude			= 150000
	turn_end_altitude       = (target_altitude/1.25)
	#
	#####################################################################################################################
	#		X					Value				Profile					Weight					RECOVERY  			#
	#####################################################################################################################
	#		
	taxa					= 	0.25				# Abastecimento			25.000 kg 				FULL
	# taxa					= 	0.29				# Voyager IV			14.400 kg				PARCIAL
	# taxa					= 	0.29				# Deep Relay I 			14.500 kg				FULL
	#
	### PARCIAL RECOVERY: 	ONLY FIRST STAGE
	### FULL RECOVERY: 		MAX(0.32) - MIN(0.20) [Boostback burn + Landing Zone]
	#
	#####################################################################################################################
	#
	newglenn(1000,turn_end_altitude,target_altitude, 28000, 30000, taxa, orientation, True)

main()