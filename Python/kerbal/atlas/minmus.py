#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import atlas

def main():
	### Rover I
	######################################################################################			
	maxq_begin              = 30000						# reduce aceleration stage - begin
	target_altitude         = 150000					# altitude default			
	######################################################################################

	atlas(2000,45000,target_altitude, maxq_begin, 36000, 1, 90)

main()