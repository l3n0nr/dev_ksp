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
	value			=	-365			# NS Capsula 			+/- 10.105 kg
	#
	#########################################################################

	boostback(value)

main()