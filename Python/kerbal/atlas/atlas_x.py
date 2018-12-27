#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import atlas_x

def main():
	######################################################################################			
	maxq_begin              = 34000						# reduce aceleration stage - begin
	target_altitude         = 150000					# altitude default			
	orientation				= 90						# NORMAL
	######################################################################################
	#	
	# 		Atlas IA 		- 		36.000 kg
	# 		Atlas IB 		- 		38.250 kg
	# 		Atlas IC 		- 		39.500 kg
	# 		Atlas ID 		- 		54.000 kg
	#
	######################################################################################

	atlas_x(2000,45000,target_altitude, maxq_begin, 36000, 1, orientation)

main()