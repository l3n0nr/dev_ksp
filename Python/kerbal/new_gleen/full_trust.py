#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newgleen

def main():
	# #################################################################################
	# #		X					Value				Profile					Weight	#
	# #################################################################################
	# # PROFILE MISSIONS
	# taxa					= 	0.01				# Fulltrusth			56.000kg
	# #
	# #################################################################################

	newgleen(1000,45000,150000, 28000, 70000, 0.01, 90)
	
main()