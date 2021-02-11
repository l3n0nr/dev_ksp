#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ssto

def main():	
	#################################################################################
	#
	target_altitude         = 107000
	turn_end_altitude       = (target_altitude/3)		
	#
	##########################################################################################

	ssto(1000,turn_end_altitude,target_altitude, 5000, 15000, 0, 90, False)

main()