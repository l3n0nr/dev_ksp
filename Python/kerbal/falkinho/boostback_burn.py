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
	value			=	-90			# deorbit garra IIII	-	+/- 07.125 kg
	# value			=	-115		# dragao capsula II		-	+/- 12.300 kg
	#
	#########################################################################

	boostback(value)

main()