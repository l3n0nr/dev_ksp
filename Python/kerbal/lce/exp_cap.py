#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import lce

def main():	
	######################################################################################
	## NORMAL
	orientation				= 90						
	maxq_begin 				= 25000						# throtle down
	target_altitude         = 150000					# target 	
	######################################################################################

	lce(2000,45000,target_altitude, maxq_begin, 36000, 1, orientation)

main()