#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falkinho_landing_zone

def main():	
	#################################################################################
	target_altitude         = 180000					
	turn_start_altitude     = 2000						
	turn_end_altitude       = (target_altitude/1.5)		
	maxq_begin				= 28000
	maxq_end				= 30000
	orientation				= 90	

	#################################################################################
	#		X					Value				Profile					Weight	#
	#################################################################################
	#
	# taxa					= 0.19				# dragao			-	+/- 24.000 kg
	# taxa					= 0.19				# lander mun v1		-	+/- 19.000 kg
	# taxa					= 0.25				# sat-climate		-	+/- 02.500 kg
	# taxa					= 0.22				# turistas station	-	+/- 05.650 kg
	# taxa					= 0.22				# lander mun v2		-	+/- 15.000 kg
	# taxa					= 0.24				# deorbit 			-	+/- 04.345 kg
	# taxa					= 0.26				# science I + HUB	-	+/- 01.820 kg
	# taxa					= 0.24				# 2 hub's station	-	+/- 04.550 kg
	# taxa					= 0.22				# ns capsula 		-	+/- 10.105 kg
	# taxa					= 0.20				# engines I			-	+/- 04.529 kg
	# taxa					= 0.21				# dream cheaser		-	+/- 18.352 kg
	taxa					= 0.22				# butterfly II		-	+/- 02.920 kg	
	#
	#################################################################################

	falkinho_landing_zone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()