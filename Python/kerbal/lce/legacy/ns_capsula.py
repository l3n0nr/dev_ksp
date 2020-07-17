#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import lce

def main():	
	######################################################################################
	## RETROGRADE
	# orientation				= 270						# 
	# maxq_begin 				= 30000						# throtle down
	# target_altitude         = 150000					# target 	

	## NORMAL
	orientation				= 90						
	maxq_begin 				= 28000						# throtle down
	target_altitude         = 180000					# target 	
	######################################################################################

	lce(2000,45000,target_altitude, maxq_begin, 36000, 1, orientation)

main()