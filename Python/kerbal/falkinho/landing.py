#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	alturaPouso					=			35				# DEFAULT
	engines_landing				=			3				# 3/8 engines in landing 		
	altitude_landing_burn		=			1500			# altitude for shutdown unnecessary engines
	deploy_legs					=			45				# deploy landing legs

	# profile						=			"Falkinho"		# profile landing
	
	sound 						= 			True 			# sound script landing

	# landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, profile, sound)
	landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falkinho", sound)

main()