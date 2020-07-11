#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	#########################################################################
	#
	value			=	-380			# NS Capsula 			+/- 10.105 kg
	#
	#########################################################################

	boostback(value)

main()