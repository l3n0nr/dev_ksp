#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import velorg

def main():
	########################################################################################

	target_altitude 		= 		130000
	# orientation 			=		315							# TOP-RETROGRADE
	orientation 			=		135							# DOWN-PROGRADE

	########################################################################################

	velorg(1000,45000,target_altitude, 34000, 36000, 2, orientation)

main()