# -*- coding: utf-8 -*-
#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import new_shepard

def main():	
	turn_start_altitude     = 3000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 180000					# target 
	maxq_begin              = 35000						# reduce aceleration stage - begin
	maxq_end                = 70000						# reduce aceleration stage - end
	taxa					= 0.10						# landing new shepard

	orientation				= 3							# TOP

	new_shepard(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()