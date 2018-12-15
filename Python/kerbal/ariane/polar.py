#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ariane

def main():
	#######################################################################################
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end

	target_altitude         = 150000					# target 
	#######################################################################################

	orientation				= 180						# DOWN
	# orientation				= 75						# DOWN	-	mission polar

	ariane(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, orientation)

main()