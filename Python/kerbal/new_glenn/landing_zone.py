#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newglenn_landingzone

def main():	
	#################################################################################
	#
	target_altitude			= 150000
	turn_end_altitude       = (target_altitude/1.25)
	#
	#####################################################################################################################
	#		X					Value				Profile					Weight					Observations  		#
	#####################################################################################################################
		
	# taxa					= 	0.14				# Demo Flight			29.000 kg				INCONSISTENT

	# taxa					= 	0.17				# Nuclear Engines I 	20.000 kg 				INCONSISTENT

	# taxa					= 	0.205				# Tur + Min				35.000 kg  				EXCEED MAX WEIGHT

	# taxa					= 	0.25				# Nuclear Engines II 	20.000 kg

	# taxa					= 	0.25				# Extrator 				19.000 kg 	
	
	# taxa					= 	0.25				# Abast. LZ				25.000 kg	

	# taxa					=	0.28				# Lander v2				15.000 kg
	
	# taxa					= 	0.28				# Adapter + Resourc.	13.500 kg

	taxa					= 	0.29				# DeOrbitGarra II		05.200 kg 				GEO	

	####################
	# FULL RECOVERY(MAX)		0.22 				Landing Zone 			32.000kg 
	####################

	#################################################################################
	#
	newglenn_landingzone(1000,turn_end_altitude,target_altitude, 28000, 30000, taxa, 90, True)

main()