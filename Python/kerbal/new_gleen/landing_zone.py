#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newgleen_landingzone

def main():	
	#################################################################################
	#
	target_altitude			= 150000
	turn_end_altitude       = (target_altitude/1.25)
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	# PROFILE MISSIONS
	# taxa					= 	0.14				# Demo Flight			29.000 kg
	### 	29000 / 0.14 = 207142.85
	### 	29000 * 0.14 = 4060

	taxa					= 	0.23				# Abast. LZ				29.000 kg
	### 	29000 / 0.23 = 126086.95
	### 	29000 * 0.23 = 667000

	# taxa					= 	0.17				# Nuclear Engines I 	20.000 kg
	###		20000 / 0.17 = 1176.47
	###		20000 * 0.17 = 3400
	
	# taxa					=	0.28				# Lander v2				15.000 kg
	###		15000 / 0.28 = 53571.42
	###		15000 * 0.28 = 4200
	
	# taxa					= 0.28					# Adapter + Resourc.	13.500 kg
	###		135000 / 0.28 = 482142.85
	###		135000 * 0.28 = 37800

	#################################################################################
	#
	newgleen_landingzone(1000,turn_end_altitude,target_altitude, 28000, 30000, taxa, 90, True)

main()