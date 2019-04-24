#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	################################################################################################################
	#	X				Value			Profile						Weight				Observations		   	   #
	################################################################################################################
	#	
	# value 		=	-125			# Lander v2					15.000 kg

	# value 		=	-125			# Lander v3					15.000 kg
	
	# value			=	-135			# Adapter + Resourc.		13.500 kg 

	# value			=	-140			# Abast.			 		25.000 kg

	value			=	-145			# Voyager IV - Eevee 		14.400 kg	

	# value			=	-150			# CaronaCraft I p1	 		15.500 kg 
	
	# value			=	-155			# Nuclear II  				20.000 kg

	# value			=	-160			# Extrator			 		19.000 kg	

	# value			=	-160			# CaronaCraft I p2	 		17.600 kg	
	#
	###########################################		NOT USED 		################################################
	#
	# value			=	-135			# DeOrbitGarra II			05.200 kg 			NOT IDEAL - GTO

	# value			=	-145			# Nuclear I 				20.000 kg 			INCONSISTENT

	# value			=	-155			# Demo. Flight				29.000 kg 			INCONSISTENT		

	# value			=	-170			# Tur + Min 				26.000 kg 			EXCEED MAX WEIGHT	
	#
	################################################################################################################
	#
	boostback(value)

main()