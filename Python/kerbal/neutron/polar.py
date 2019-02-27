#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
	## UP
	# target_altitude			= 130000					#
	# orientation				= 0 						#

	## DOWN
	target_altitude			= 130000					#
	orientation				= 180 						#

	neutron(1000,45000,target_altitude, 30000, 36000, 1, orientation)

main()