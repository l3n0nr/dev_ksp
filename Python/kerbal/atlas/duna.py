#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import atlas_x

def main():
	######################################################################################
	## RELAYSAT II
	maxq_begin              = 28000						# reduce aceleration stage - begin
	target_altitude         = 150000					# altitude default			
	orientation				= 90						# NORMAL	

	atlas_x(2000,45000,target_altitude, maxq_begin, 36000, 1, orientation)

main()