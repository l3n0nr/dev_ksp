#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
	######################################################################################
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	maxq_begin              = 30000						# reduce aceleration stage - begin
	maxq_end                = turn_end_altitude			# reduce aceleration stage - end
	######################################################################################

	## UP
	# target_altitude			= 100000					#
	# orientation				= 0 						#

	## DOWN
	target_altitude			= 120000					#
	orientation				= 180 						#

	neutron(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, orientation)

main()