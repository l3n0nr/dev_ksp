# -*- coding: utf-8 -*-
#!/usr/bin/env python

value=12810       	# kg

def calc(value):	
	mass=16948      # 14.948 kg, final stage
	taxa=0.145      # 0.145% fuel, first stage

	plus_less=0.66
	mass_plus=mass+(mass*plus_less)
	mass_less=mass-(mass*plus_less)

	heavy = False
	light = False

	x = (value * taxa / mass)

	# print 'Valor de x antes:',x
	# print mass_plus
	# print mass_less

	if value > mass_plus or value < mass_less:
		print ('Very heavy or very light')			
	else:
		if value > mass:
			x = x - taxa
		elif value < mass:
			x = taxa + x 
		else:
			x = taxa

	# print 'Valor de x depois:',x
	print x

calc(value)
