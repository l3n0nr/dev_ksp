#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	##################################################################################
	#	X				Value			Profile						Weight orbiter	 #
	##################################################################################
	#	
	value			=	-150			# Flight Test Cargo					141.000 kg
	#
	##################################################################################

	boostback(value)

main()