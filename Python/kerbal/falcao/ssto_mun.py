#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ssto

def main():	
	#################################################################################
	#
	target_altitude         = 20000
	turn_end_altitude       = (target_altitude/3)		
	#
	##########################################################################################

	ssto(1000,turn_end_altitude,target_altitude, 2500, 3600, 0, 90, False)

main()