#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	# value			=	-80			# dragao
	value			=	-25			# lander mun

	# v2  = -80             # dragao
    # v2  = -25             # lander mun

	boostback(value)

main()