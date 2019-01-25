#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import lce

def main():	
	######################################################################################
	orientation				= 270						# RETROGRADE	
	maxq_begin 				= 30000						# throtle down
	target_altitude         = 150000					# target 	
	######################################################################################

	lce(2500,45000,target_altitude, maxq_begin, 36000, 1, orientation)

main()