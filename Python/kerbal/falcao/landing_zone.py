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
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#	
	# taxa					= 0.17				# Cargo			-		+/- 170.000 kg	
	taxa					= 0.18				# Tripulation	-		+/- ??? 	kg	
	#
	####################
	# FULL RECOVERY(MAX)		0.165 Cargo
	# FULL RECOVERY(MAX)		0.175 Tripulation
	####################
	#	
	#################################################################################

	falcao_landing_zone(2000,turn_end_altitude,target_altitude, 28000, 30000, taxa, 90, True)

main()