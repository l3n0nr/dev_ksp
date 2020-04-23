#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import velorg

def main():
	########################################################################################

	## PROGRADE
	### normal
		# target_altitude       =       130000
		# orientation           =       90

	### down + 45(right) 
		# target_altitude       =       130000
		# orientation           =       135

	## RETROGRADE
	### top
		# target_altitude       =       130000
		# orientation           =       315

	### down + 45(left)
	target_altitude         =       100000
	orientation             =       225

	########################################################################################

	velorg(1000,45000,target_altitude,34000,36000,3,orientation)

main()