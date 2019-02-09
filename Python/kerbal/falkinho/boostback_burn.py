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
	# value			=	-25			# lander mun v1			-	+/- 19.000 kg
	##		LANDING ZONE NOT POSSIBLE

	# value			= 	-30			# butterfly II			-	+/- 02.920 kg
	# value			=	-40			# lab + science			-	+/- 05.900 kg

	value			=	-50			# minerio 				-	+/- 04.400 kg
	# value			=	-60			# extrator conv 		-	+/- 05.700 kg			
	
	# value			=	-65			# science I + HUB		-	+/- 01.820 kg	

	# value			=	-70			# sat-climate I 		-	+/- 02.500 kg
	# value			=	-70			# engines I				-	+/- 04.529 kg
	
	# value			=	-80			# deorbit 				-	+/- 04.430 kg		
	# value			=	-80			# sat-climate II		- 	+/- 02.500 kg
	# value			=	-80			# lander mun v2			-	+/- 15.000 kg
	# value			=	-80			# dragao				-	+/- 24.000 kg
	##		LANDING ZONE NOT POSSIBLE
	
	# value			=	-85			# deorbit garra			-	+/- 03.500 kg

	# value			=	-85			# sat-climate III		-	+/- 03.800 kg

	# value			=	-90			# engines II(nucl.)		-	+/- 13.000 kg	
	# value			=	-90			# abastecimento rcs		-	+/- 06.343 kg
	# value			=	-90			# 2 hub's station 		-	+/- 04.550 kg	
	# value			=	-90			# turistas 12 			-	+/- 08.700 kg

	# value			=	-95			# turistas station 		-	+/- 05.650 kg				
	# value			=	-95			# ns capsula 			-	+/- 10.105 kg		
	# value			=	-95			# dream cheaser			-	+/- 18.352 kg
	##		LANDING ZONE NOT POSSIBLE

	# value			=	-95			# only test landing zone!	

	# value			=	-110		# deorbit I-II adapter	-	+/- 03.000 kg
	# value			=	-110		# abastecimento fuel	-	+/- 11.203 kg

	# value			=	-520		# ns capsula 			-	+/- 10.105 kg

	# value			=	80			# falkinho triplo		-	+/- 24.000 kg		
	# value			=	20			# falkinho triplo teste	-	+/- 36.000 kg
	#
	#########################################################################

	boostback(value)

main()