#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	#########################################################################
	# value			=	-80			# dragao				-	+/- 24.000 kg
	# value			=	-25			# lander mun v1			-	+/- 19.000 kg
	# value			=	-70			# sat-climate I 		-	+/- 02.500 kg
	# value			=	-95			# turistas station 		-	+/- 05.650 kg
	# value			=	-80			# sat-climate II		- 	+/- 02.500 kg
	# value			=	-80			# lander mun v2			-	+/- 15.000 kg
	# value			=	-78			# deorbit I 			-	+/- 04.430 kg
	# value			=	-65			# science I + HUB		-	+/- 01.820 kg
	# value			=	-90			# 2 hub's station 		-	+/- 04.550 kg
	#########################################################################

	value			=	-85			# ns capsula 			-	+/- 04.550 kg			????

	boostback(value)

main()