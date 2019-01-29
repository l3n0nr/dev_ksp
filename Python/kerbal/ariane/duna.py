#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ariane

def main():
	######################################################################################	
	#
	# target_altitude         = 130000					# duna I
	# target_altitude         = 160000					# duna polar orbiter I
	target_altitude         = 200000					# icesat
	#
	######################################################################################
	#
	ariane(1000,45000,target_altitude, 32000, 36000, 1, 90)

main()