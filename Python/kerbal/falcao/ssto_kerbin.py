#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ssto

def main():	
	#################################################################################
	#
	target_altitude         = 100000
	turn_end_altitude       = (target_altitude/3)		
	#
	##########################################################################################

	ssto(500,turn_end_altitude,target_altitude, 25000, 36000, 0, 90, False)

main()