#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import landing_zone

def main():	
	target_altitude         = 180000					
	turn_start_altitude     = 2000						
	turn_end_altitude       = (target_altitude/1.5)		
	maxq_begin				= 28000
	maxq_end				= 30000
	
	# taxa					= 0.19				# dragao - lander mun			-	24.000 kg
	# taxa					= 0.25				# sat-climate					-	2.500  kg
	taxa					= 0.22				# turistas station				-	5.650  kg

	orientation				= 90

	landing_zone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()