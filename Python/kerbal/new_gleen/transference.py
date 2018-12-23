#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newgleen

def main():
	######################################################################################
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 180000					# target orbit
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 70000						# reduce aceleration stage - end
	######################################################################################
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	# PROFILE MISSIONS
	taxa					= 	0.03				# Transference			31.500 kg
	#
	#################################################################################

	newgleen(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, 90)
	
main()