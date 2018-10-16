#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import suborbital

def main():
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 150000					# target 				# ICESAT
	# target_altitude         = 2862000					# GEO - Kerbin - BUT ONLY EQUATORIAL, MEN!
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 70000						# reduce aceleration stage - end
	taxa					= 0.115						# Landing first stage	# GEOSAT
	# taxa					= 0.15						# Landing first stage	# ICESAT
	orientation				= 360						# POLAR TOP

	suborbital(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()