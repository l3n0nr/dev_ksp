# -*- coding: utf-8 -*-
#!/usr/bin/env python

value=4135       	# kg

def calc(value):	
	mass=14948      # 14.948 kg, final stage
	taxa=0.145      # 0.145% fuel, first stage
	min = 5000
	max = 16000

	heavy = False
	light = False

	x = (value * taxa / mass)

	print x

	if value > min:
		x = x + taxa
	elif value < max:
		x = taxa - x
	else:
		x = taxa

		# ((5135*0,145)/14948) + 0,145  = 0,194811012

		# if x <= 0.04:
		# 	x = 1 - (x + taxa)
		# elif x >= 0.20:
		# 	x = taxa - x
		# else:
		# 	x = x + taxa

	if heavy:
		print ('Heavy, heavy!!'), x
	elif light:
		print ('Light, light!!'), x
	else:
		print ('Fuel first stage:'),x

calc(value)
