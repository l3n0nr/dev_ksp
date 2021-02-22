#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falkinho

def main():	
	#################################################################################
	#
	target_altitude         = 180000										
	turn_end_altitude       = (target_altitude/1.5)		
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#			
	# taxa					= 0.19				# engines II nuclear-	+/- 08.880 kg
	# taxa					= 0.20				# minerio			-	+/- 04.400 kg	
	# taxa					= 0.20				# 6kerbals + ISRU	-	+/- 09.600 kg	
	# taxa					= 0.21				# dragao capsula II	-	+/- 12.300 kg		
	taxa					= 0.23				# deorbit garra	IIII-	+/- 07.125 kg
	# taxa					= 0.24				# sat-climate IIII	-	+/- 03.050 kg	
	#
	#################################################################################
	#
	#	INCLINATION ORBITS:
	#		UP: 	Inclination - Relative inclination to target (200km)
	#		DOWN: 	Inclination + Relative inclination to target (200km)
	#
	#################################################################################

	falkinho(1000,turn_end_altitude,target_altitude, 28000, 30000, taxa, 90, True)

main()