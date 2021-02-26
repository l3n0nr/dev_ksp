#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	################################################################################################################
	#	X				Value			Profile						Weight				RECOVERY			   	   #
	################################################################################################################
	#
	value			=	-140			# Abastecimento		 		25.000 kg	 		FULL
	# value			=	-145			# Voyager IV 				14.400 kg			PARCIAL
	# value			=	-145			# Deep Relay I 				14.500 kg			FULL
	#
	################################################################################################################
	#
	boostback(value)

main()