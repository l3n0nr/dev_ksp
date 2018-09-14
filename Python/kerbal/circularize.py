#!/usr/bin/env python

## import modules
from base import circularize

target_altitude = 35794000
	# KERBIN = KM
		# GEO-EQUA 		= 2863000.33
			# Orbit period: 04 hours - 03 satellites
			
	# MUN = KM
		# GEO-EQUA  	= 2970000.608
		# SEMI-SINCRO	= 1797000.41

	# MINMUS = KM	
		# GEO 			= 35794000 

circularize(target_altitude)