#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
	#################################################################
	# ## INCLIN TOP
	# target_altitude			= 110000
	# orientation				= 41.7

	# ## INCLIN DOWN
	# target_altitude			= 100000
	# orientation				= 139.2

	# target_altitude 		=		100000
	# orientation 			=		315

	target_altitude 		=		105000
	orientation 			=		160

	#################################################################

	neutron(1000,45000,target_altitude, 30000, 36000, 1, orientation)

main()