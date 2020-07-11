#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newshepard

def main():	
	
	#################################################################################
	#
	taxa					= 0.20
	target_altitude 		= 160000	
	turn_end_altitude       = (target_altitude/1.7)	
	#
	#################################################################################

	newshepard(1000,turn_end_altitude,target_altitude, 28000, 30000, taxa, 90, False)

main()