#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	#########################################################################
	#	X				Value			Profile						Weight	#
	#########################################################################
	#			
	value			=	30			# deorbit garra IIII	-	+/- 07.125 kg
	#
	###########################		LEGACY 			#########################
	#
	# value			=	25			# DEMO					-	+/- 23.000 kg
	#
	#########################################################################

	boostback(value)

main()