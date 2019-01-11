#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import velorg

def main():
	## VELORG I
	# ########################################################################################
	# turn_start_altitude     = 16000					# inclination begin
	# target_altitude         = 100000					# target 
	# maxq_begin              = 30000					# reduce aceleration stage - begin
	# ########################################################################################

	## VELORG II
	########################################################################################
	turn_start_altitude     = 1000						# inclination begin
	target_altitude         = 100000					# target 
	maxq_begin              = 34000						# reduce aceleration stage - begin
	########################################################################################

	velorg(turn_start_altitude,45000,target_altitude, maxq_begin, 36000, 1, 90)

main()