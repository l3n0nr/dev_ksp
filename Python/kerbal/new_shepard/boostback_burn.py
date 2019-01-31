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
	## New Shepard I
	value			=	-355			# NS Capsula 			+/- 10.105 kg

	# ## New Shepard II
	# value			=	-355			# NS Capsula 			+/- 10.105 kg
	#
	#########################################################################

	boostback(value)

main()