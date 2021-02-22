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
	# value			=	-45			# 6 kerbals + ISRU		-	+/- 09.600 kg	
	# value			=	-50			# minerio 				-	+/- 04.400 kg	
	# value			=	-60			# engines II nuclear	-	+/- 08.880 kg			
	value			=	-90			# deorbit garra IIII	-	+/- 07.125 kg					
	# value			=	-115		# dragao capsula II		-	+/- 12.300 kg
	# value			=	-115		# sat climate IIII		-	+/- 03.050 kg	
	#
	#########################################################################

	boostback(value)

main()