#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
	#
	#################################################################
	# PROGRADE
	target_altitude			= 150000
	orientation				= 90
		
	# RETROGRADE
	# target_altitude			= 90000
	# orientation				= 270

	## CUBESATS
	# target_altitude         	= 125000
	# orientation				= 10	
	#################################################################
	#
	#	INCLINATION ORBITS:
	#		UP: 	Inclination - Relative inclination to target
	#		DOWN: 	Inclination + Relative inclination to target
	#
	#################################################################
	#
	neutron(1000,45000,target_altitude, 30000, 36000, 1, orientation, True)

main()