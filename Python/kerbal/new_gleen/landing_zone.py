#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newgleen_landingzone

def main():	
	#################################################################################
	#
	turn_start_altitude     = 1000	
	maxq_begin				= 28000
	maxq_end				= 30000
	target_altitude			= 150000
	turn_end_altitude       = (target_altitude/1.25)
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	# PROFILE MISSIONS
	# taxa					= 	0.14				# Demo Flight			27.000 kg
	### 	27000 / 0.13 = 192857.14
	### 	27000 * 0.13 = 3780

	# taxa					= 	0.17				# Nuclear Engines I 	20.000 kg
	###		20000 / 0.17 = 1176.47
	###		20000 * 0.17 = 3400
	
	# taxa					=	0.28				# Lander v2				15.000 kg
	###		15000 / 0.28 = 53571.42
	###		15000 * 0.28 = 4200
	
	taxa					= 0.28					# adaptar + resourc.	13.500 kg
	###		135000 / 0.28 = 482142.85
	###		135000 * 0.28 = 37800

	#################################################################################
	#
	newgleen_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, 90, True)

main()