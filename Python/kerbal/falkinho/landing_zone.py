#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falkinho

def main():	
	#################################################################################
	#
	target_altitude         = 180000										
	turn_end_altitude       = (target_altitude/1.5)		
	#
	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#			
	# taxa					= 0.19				# engines II nuclear-	+/- 08.880 kg
	# taxa					= 0.20				# minerio			-	+/- 04.400 kg	
	# taxa					= 0.20				# 6kerbals + ISRU	-	+/- 09.600 kg	
	# taxa					= 0.21				# dragao capsula II	-	+/- 12.300 kg		
	taxa					= 0.23				# deorbit garra	IIII	+/- 07.125 kg			
	#
	###########################		LEGACY 			#########################
	#
	# taxa					= 0.20				# engines I			-	+/- 04.529 kg
	# taxa					= 0.20				# extrator conv I	-	+/- 05.700 kg
	# taxa					= 0.20				# deorbit garra II		+/- 06.000 kg	
	# taxa					= 0.20				# lab + science		-	+/- 06.360 kg	
	# taxa					= 0.20				# 5 turist + lab	-	+/- 09.500 kg
	# taxa					= 0.21				# dragao capsula	-	+/- 11.000 kg		
	# taxa					= 0.21				# abastecimento fuel-	+/- 11.203 kg
	# taxa					= 0.22				# butterfly II		-	+/- 02.920 kg	
	# taxa					= 0.22				# turistas station	-	+/- 05.650 kg		
	# taxa					= 0.22				# turistas deorbit	-	+/- 08.050 kg
	# taxa					= 0.22				# ns capsula 		-	+/- 10.105 kg				
	# taxa					= 0.23				# deorbit I-II adapter	+/- 03.000 kg		
	# taxa					= 0.23				# deorbit garra	III		+/- 06.300 kg
	# taxa					= 0.23				# abastecimento rcs	-	+/- 06.343 kg
	# taxa					= 0.23				# turistas 12 		-	+/- 08.700 kg	
	# taxa					= 0.24				# deorbit garra I/II	+/- 03.500 kg	
	# taxa					= 0.24				# sat-climate III		+/- 03.900 kg	
	# taxa					= 0.24				# deorbit 			-	+/- 04.345 kg
	# taxa					= 0.24				# 2 hub's station	-	+/- 04.550 kg
	# taxa					= 0.25				# sat-climate		-	+/- 02.500 kg	
	# taxa					= 0.26				# science I + HUB	-	+/- 01.820 kg
	#
	###########################		NOT USED 		#################################
	#
	# taxa					= 0.19				# engines II nuclear-	+/- 08.880 kg
	# taxa					= 0.19				# lander mun v1		-	+/- 19.000 kg
	# taxa					= 0.21				# dream cheaser		-	+/- 18.352 kg
	# taxa					= 0.22				# ns capsula NTR	-	+/- 10.105 kg 	## RETROGRADE(270)
	# taxa					= 0.22				# lander mun v2		-	+/- 15.000 kg
	#
	#################################################################################

	falkinho(1000,turn_end_altitude,target_altitude, 28000, 30000, taxa, 90, True)

main()