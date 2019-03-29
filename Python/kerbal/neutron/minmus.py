#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
	#################################################################
	#
	target_altitude			= 150000
	orientation				= 90
	#
	#################################################################

	neutron(1000,45000,target_altitude, 30000, 36000, 1, orientation)

main()