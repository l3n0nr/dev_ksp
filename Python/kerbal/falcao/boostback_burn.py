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
	value			=	-225			# Flight test		-	+/- 170.000 kg
	#
	#########################################################################

	boostback(value)

main()