#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	alturaPouso					=			31.5			# DEFAULT
	engines_landing				=			3				# 3/8 engines in landing 		
	altitude_landing_burn		=			1200			# altitude for shutdown engines
	deploy_legs					=			45				# distancy for deploy landing legs
	profile						=			"Falkinho"		# profile landing
	sound 						= 			True 			# sound script landing

	# fuel: 251

	landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, profile, sound)

main()