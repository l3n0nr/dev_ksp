#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import titan_x

def main():
	######################################################################################
	## ASTEROID 01
	target_altitude         = 150000					# altitude default			
	orientation				= 45						# TOP-NORMAL 
	sepatron 				= 51.2 						# 32(4s x 8 boost) x 1.6(unid)
	#
	######################################################################################

	titan_x(2000,45000,target_altitude, 30000, 36000, 1, orientation, sepatron)

main()