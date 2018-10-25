# -*- coding: utf-8 -*-
#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import new_shepard

def main():	
	turn_start_altitude     = 3000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 150000					# target 
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 70000						# reduce aceleration stage - end
	
	# taxa					= 0.05						# landing new shepard 	-	down
	taxa					= 0.068						# landing new shepard 	-	top
	
	# orientation				= 41.7						# TOP-NORMAL		- OK

	orientation				= 42.2						# TOP-NORMAL		- inclination + 0.5
	# orientation				= 41.2						# TOP-NORMAL		- inclination - 0.5

	# orientation				= 135						# DOWN-NORMAL		- OK	

	new_shepard(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()