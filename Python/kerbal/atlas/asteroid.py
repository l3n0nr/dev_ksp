#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import atlas

def main():
	######################################################################################			
	## DEFAULT 				-			Atlas I 		- 		27.000 kg
	# target_altitude         = 150000					# altitude default			
	# orientation				= 90						# NORMAL
	#
	######################################################################################
	## ASTEROID 01
	#
	# target_altitude         = 150000					# altitude default			
	# orientation				= 315						# TOP-ANTINORMAL
	#
	######################################################################################
	## ASTEROID 02
	target_altitude         = 180000					# altitude default			
	orientation				= 45						# TOP-NORMAL 					??
	#
	######################################################################################

	atlas(2000,45000,target_altitude, 30000, 36000, 1, orientation)

main()