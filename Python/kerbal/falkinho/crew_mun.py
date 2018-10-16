#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import suborbital

def main():
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 150000					# orbit target 
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 70000						# reduce aceleration stage - end	

	# taxa					= 0.13						# Landing - docking port  - mun
	# taxa					= 0.16						# Landing - crew - mun
	# taxa					= 0.13						# Landing - solid booster - kerbol
	taxa					= 0.18						# Landing - laboratorio + turistas = mun
		
	orientation				= 90						# NORMAL

	suborbital(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()