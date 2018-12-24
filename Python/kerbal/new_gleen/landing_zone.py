#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newgleen_landingzone

def main():	
	#################################################################################
	# NOT CHANGE
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
	### 	27000 / 0.13 = 192857,14
	### 	27000 * 0.13 = 3780

	taxa					= 	0.17				# Nuclear Engines I 	20.000 kg
	#
	#################################################################################
	#
	newgleen_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, 90, True)

main()