#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../../')
from base import suborbital

def main():
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 150000					# target 
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 70000						# reduce aceleration stage - end
	taxa					= 0.125						# Landing first stage in %(Taxa/100)
		# 0.10% = fuel min		

	orientation				= 90						# NORMAL
	# orientation				= 96.7						# NORMAL - 6.7
	# orientation				= 128.3						# DOWN - 6.7


			# 45  : TOP-NORMAL							# 1.5 hours in the clock.
			# 90  : NORMAL 								# 3 hours in the clock.
			# 135 : NORMAL-DOWN							# 4.5 hours in the clock.
			# 180 : DOWN 								# 6 hours in the clock.
			# 225 : DOWN-ANTINORMAL						# 7.5 hours in the clock.
			# 270 : ANTINORMAL 							# 9 hours in the clock.
			# 315 : ANTINORMAL-TOP						# 10.5 in the clock.
			# 360 : TOP									# 12 hours in the clock.

	suborbital(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()