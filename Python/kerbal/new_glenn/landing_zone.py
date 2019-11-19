#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import newglenn_landingzone

def main():	
	#################################################################################
	#
	orientation 			= 90
	target_altitude			= 150000
	turn_end_altitude       = (target_altitude/1.25)
	#
	#####################################################################################################################
	#		X					Value				Profile					Weight					Observations  		#
	#####################################################################################################################
	#		
	# taxa					= 	0.20				# Dream Cheaser I 		15.000 kg 				FULL RECOVERY

	# taxa					= 	0.25				# Nuclear II 			20.000 kg 				FULL RECOVERY

	# taxa					= 	0.25				# Extrator 				19.000 kg 				FULL RECOVERY
	
	taxa					= 	0.25				# Abastecimento			25.000 kg 				FULL RECOVERY

	# taxa					= 	0.26				# CaronaCraft I p2	 	17.600 kg 				(OP) PARCIAL RECOVERY	

	# taxa					= 	0.26				# CaronaCraft I p1	 	15.500 kg 				FULL RECOVERY	

	# taxa					=	0.28				# Lander v2	/ v3		15.000 kg 				FULL RECOVERY

	# taxa					= 	0.28				# Adapter + Resourc.	13.500 kg 				FULL RECOVERY

	# taxa					= 	0.29				# Voyager IV - Eevee	14.400 kg				(OP) PARCIAL RECOVERY
	#
	### FULL RECOVERY: MAX(0.32) - MIN(0.20) [Boostback burn + Landing Zone]
	#
	############################################### 	NOT USED 		#################################################
	#
	# taxa					= 	0.14				# Demo Flight			29.000 kg				INCONSISTENT

	# taxa					= 	0.17				# Nuclear I 			20.000 kg 				INCONSISTENT

	# taxa					= 	0.205				# Tur + Min				35.000 kg  				EXCEED MAX WEIGHT	

	# taxa					= 	0.29				# DeOrbitGarra II		05.200 kg 				NOT IDEAL - GTO	
	#
	#####################################################################################################################
	#
	newglenn_landingzone(1000,turn_end_altitude,target_altitude, 28000, 30000, taxa, orientation, True)

main()