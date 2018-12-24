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
	value			=	-165			# Demo Flight - Land. Zone	27.000 kg
	#
	#########################################################################
	#
	boostback(value)

main()