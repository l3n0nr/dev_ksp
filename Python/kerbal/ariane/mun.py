#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ariane

def main():
	#######################################################################################
	turn_start_altitude     = 2000						# inclination begin
	turn_end_altitude       = 45000						# inclination end	
	maxq_begin              = 34000						# reduce aceleration stage - begin
	maxq_end                = 36000						# reduce aceleration stage - end
	#######################################################################################	

	# Ariane II
	# target_altitude         = 120000					# 5 turistas + satelite
	target_altitude         = 120000					# Explorer I 

	ariane(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, 90)

main()