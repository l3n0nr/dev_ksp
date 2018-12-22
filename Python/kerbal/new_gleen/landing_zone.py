#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newglenn_landingzone

def main():	
	#################################################################################
	# NOT CHANGE
	turn_start_altitude     = 1000	
	maxq_begin				= 28000
	maxq_end				= 30000
	turn_end_altitude		= 120000
	#
	#################################################################################
	# CHANGE
	target_altitude         = 150000	
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	# PROFILE MISSIONS
	# taxa					= 	0.14				# Demo Flight			36.000 kg
	taxa					= 	0.13				# Demo Flight			36.000 kg			# CHECK THIS
	#
	#################################################################################
	#
	newglenn_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, 90, True)

main()