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
	value			=	-155			# Demo Flight - Land. Zone	27.000 kg
	# value			=	-145			# Nuclear Engines I 		20.000 kg
	# value 			=	-125			# Lander v2					15.000 kg
	#
	#########################################################################
	#
	boostback(value)

main()