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
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	# PROFILE MISSIONS
	# taxa					= 	0.14				# Demo Flight			29.000 kg				INCONSISTENT
	### 	29000 / 0.14 = 207142.85
	### 	29000 * 0.14 = 4060	

	# taxa					= 	0.17				# Nuclear Engines I 	20.000 kg 				INCONSISTENT
	###		20000 / 0.17 = 1176.47
	###		20000 * 0.17 = 3400

	taxa					= 	0.205				# Tur + Min				35.000 kg  				??

	# taxa					= 	0.25				# Nuclear Engines II 	20.000 kg

	# taxa					= 	0.25				# Extrator 				19.000 kg 	
	
	# taxa					= 	0.25				# Abast. LZ				25.000 kg
	### 	25000 / 0.25 = 100000
	### 	25000 * 0.25 = 6250

	# taxa					=	0.28				# Lander v2				15.000 kg
	###		15000 / 0.28 = 53571.42
	###		15000 * 0.28 = 4200
	
	# taxa					= 0.28					# Adapter + Resourc.	13.500 kg
	###		135000 / 0.28 = 482142.85
	###		135000 * 0.28 = 37800

	#################################################################################
	#
	newglenn_landingzone(1000,turn_end_altitude,target_altitude, 28000, 30000, taxa, 90, True)

main()