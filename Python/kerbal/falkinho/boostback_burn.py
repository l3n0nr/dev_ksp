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
	# value			= 	-30			# butterfly II			-	+/- 02.920 kg
		
	# value			=	-50			# 5 turist + lab		-	+/- 09.500 kg
	# value			=	-50			# lab + science			-	+/- 05.900 kg
	# value			=	-50			# minerio 				-	+/- 04.400 kg

	# value			=	-60			# engines II nuclear	-	+/- 08.880 kg	
	# value			=	-60			# extrator conv I 		-	+/- 05.700 kg
	# value			=	-60			# deorbit garra	II		-	+/- 06.000 kg				
	
	# value			=	-65			# science I + HUB		-	+/- 01.820 kg	

	# value			=	-70			# sat-climate I 		-	+/- 02.500 kg
	# value			=	-70			# engines I				-	+/- 04.529 kg
	
	# value			=	-80			# deorbit 				-	+/- 04.430 kg		
	# value			=	-80			# sat-climate II		- 	+/- 02.500 kg	
	
	# value			=	-85			# deorbit garra I/II	-	+/- 03.500 kg
	# value			=	-85			# sat-climate III		-	+/- 03.800 kg	
	
	# value			=	-90			# deorbit garra III		-	+/- 06.300 kg
	# value			=	-90			# abastecimento rcs		-	+/- 06.343 kg
	# value			=	-90			# 2 hub's station 		-	+/- 04.550 kg	
	# value			=	-90			# turistas 12 			-	+/- 08.700 kg	

	# value			=	-95			# turistas station 		-	+/- 05.650 kg				
	# value			=	-95			# turistas deorbit 		-	+/- 08.000 kg				
	# value			=	-95			# ns capsula 			-	+/- 10.105 kg				

	# value			=	-110		# deorbit I-II adapter	-	+/- 03.000 kg
	value			=	-110		# abastecimento fuel	-	+/- 11.203 kg
	# value			=	-110		# dragao capsula 		-	+/- 11.000 kg
	#
	###########################		NOT USED 		#########################
	#
	# value			=	-25			# lander mun v1			-	+/- 19.000 kg
	##		LANDING ZONE NOT POSSIBLE
	#
	# value			=	-80			# lander mun v2			-	+/- 15.000 kg
	#
	# value			=	-90			# engines II nuclear	-	+/- 08.880 kg
	#
	# value			=	-95			# dream cheaser			-	+/- 18.352 kg
	##		LANDING ZONE NOT POSSIBLE
	#
	# value			=	-520		# ns capsula 			-	+/- 10.105 kg
	#
	#########################################################################

	boostback(value)

main()