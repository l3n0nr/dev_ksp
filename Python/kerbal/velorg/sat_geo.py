#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import velorg

def main():
	########################################################################################
	turn_start_altitude     = 1000						# inclination begin
	########################################################################################

	velorg(turn_start_altitude,45000,100000, 30000, 36000, 2, 90)

main()