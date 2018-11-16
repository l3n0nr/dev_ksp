#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	maxq_begin              = 30000						# reduce aceleration stage - begin
	maxq_end                = turn_end_altitude			# reduce aceleration stage - end
	correction_time			= 1							# fine tuning - orbital manuever

	target_altitude         = 130000					# target
	
	orientation				= 135						# inclination 01
	# orientation				= 180						# inclination 02

	######## IDEAL ########
	## inclination 1	 
	## inclination 2
	## inclination 1	 
	## inclination 2
	## inclination 1	 
	## inclination 2
	######## 

	neutron(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation)

main()