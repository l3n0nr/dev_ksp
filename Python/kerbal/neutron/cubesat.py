#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 130000					# target 
	maxq_begin              = 30000						# reduce aceleration stage - begin
	maxq_end                = turn_end_altitude			# reduce aceleration stage - end
	correction_time			= 1							# fine tuning - orbital manuever
	
	orientation				= 41.7						# TOP-NORMAL
	# orientation				= 135						# DOWN-NORMAL

	neutron(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation)

main()