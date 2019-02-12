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
	# value			=	-155			# Demo. Flight				29.000 kg

	# value			=	-140			# Abast.			 		25.000 kg

	# value			=	-145			# Nuclear Engines I 		20.000 kg

	# value			=	-155			# Nuclear Engines II 		20.000 kg

	value			=	-170			# Tur + Min 				26.000 kg 				???

	# value			=	-160			# Extrator			 		19.000 kg

	# value 		=	-125			# Lander v2					15.000 kg
	
	# value			=	-115			# Adapter + Resourc.		13.500 kg 
	#
	#########################################################################
	#
	boostback(value)

main()