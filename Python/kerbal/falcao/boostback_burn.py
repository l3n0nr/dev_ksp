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
	# value			=	-10			# Falcao Crew					220.000 kg	 	 #
	value			=	-10			# Falcao Fuel					227.000 kg	 	 #
	#
	##################################################################################

	boostback(value)

main()