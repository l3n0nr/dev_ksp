#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	#######################################################################################
	alturaPouso					=			20				# default
	engines_landing				=			12				# engines in landing
	altitude_landing_burn		=			1500			# altitude for shutdown engines
	deploy_legs					=			200				# deploy landing legs
	profile						=			"New Glenn"		# profile landing
	sound 						= 			False 			# sound script landing	
	#######################################################################################

	landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, profile, sound)

main()