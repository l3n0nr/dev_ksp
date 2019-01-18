#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import atlas

def main():
	######################################################################################			
	## DEFAULT 				-			Atlas I 		- 		27.000 kg
	# maxq_begin              = 34000						# reduce aceleration stage - begin
	# target_altitude         = 150000					# altitude default			
	# orientation				= 90						# NORMAL
	#
	######################################################################################
	## ASTEROID 01
	#
	# maxq_begin              = 30000						# reduce aceleration stage - begin
	target_altitude         = 150000					# altitude default			
	orientation				= 315						# TOP-ANTINORMAL
	#
	######################################################################################

	atlas(2000,45000,target_altitude, 30000, 36000, 1, orientation)

main()