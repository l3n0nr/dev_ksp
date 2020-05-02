#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
	#################################################################
	# PROGRADE
	target_altitude			= 120000
	orientation				= 90
		
	# RETROGRADE
	# target_altitude			= 90000
	# orientation				= 270
	#################################################################

	neutron(1000,45000,target_altitude, 30000, 36000, 1, orientation)

main()