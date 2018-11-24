#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ariane

def main():
	#######################################################################################
	turn_start_altitude     = 2000						# inclination begin
	target_altitude         = 180000					# target 
	maxq_begin              = 25000						# reduce aceleration stage - begin
	#######################################################################################

	orientation				= 41.7						# TOP-NORMAL
	# orientation				= 139.2						# DOWN-NORMAL

	ariane(turn_start_altitude, 45000,target_altitude, maxq_begin, 36000, 1, orientation)

main()