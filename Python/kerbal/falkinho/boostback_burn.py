#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	# value			=	-80			# dragao
	# value			=	-25			# lander mun v1	
	# value			=	-70			# sat-climate I
	# value			=	-95			# turistas station
	# value			=	-80			# sat-climate II
	value			=	-80			# lander mun v2

	boostback(value)

main()