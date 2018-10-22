#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import boostback

def main():
	# value			=	-80			# dragao
	# value			=	-25			# lander mun
	value			=	-70			# sat-climate

	boostback(value)

main()