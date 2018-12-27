#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import atlas

def main():
	######################################################################################			
	maxq_begin              = 34000						# reduce aceleration stage - begin
	target_altitude         = 150000					# altitude default			
	orientation				= 90						# NORMAL
	######################################################################################
	#	
	# 		Atlas I 		- 		27.000 kg
	#
	######################################################################################

	atlas(2000,45000,target_altitude, maxq_begin, 36000, 1, orientation)

main()