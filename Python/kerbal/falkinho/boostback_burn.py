#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	value			=	-80			# dragao				-	+/- 24.000 kg
	# value			=	-25			# lander mun v1			-	+/- 19.000 kg
	# value			=	-70			# sat-climate I 		-	+/- 02.500 kg
	# value			=	-95			# turistas station 		-	+/- 05.650 kg
	# value			=	-80			# sat-climate II		- 	+/- 02.500 kg
	# value			=	-80			# lander mun v2			-	+/- 15.000 kg
	# value			=	-78			# deorbit I 			-	+/- 04.430 kg		

	boostback(value)

main()