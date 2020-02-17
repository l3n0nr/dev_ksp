#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
	#################################################################
	## UP
	orientation				= 0 			

	# DOWN
	# orientation				= 180

	#################################################################

	neutron(1000,45000,130000, 30000, 36000, 2, orientation)

main()