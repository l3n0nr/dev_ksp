#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import lce

def main():	
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 120000					# target 
	maxq_begin              = 35500						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	correction_time			= 1							# fine tuning - orbital manuever
	orientation				= 90						# normal inclination	

	lce(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation)

main()