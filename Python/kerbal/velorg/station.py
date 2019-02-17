#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import velorg

def main():
	########################################################################################
	turn_start_altitude     = 1000						# inclination begin
	target_altitude 		= 130000

	orientation				= 41.7						# TOP-NORMAL
	# orientation				= 139.2						# DOWN-NORMAL

	########################################################################################

	velorg(turn_start_altitude,45000,target_altitude, 34000, 36000, 1, orientation)

main()