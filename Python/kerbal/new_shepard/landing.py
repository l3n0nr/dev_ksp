#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	alturaPouso					=			35				# default
	engines_landing				=			1				# 1/3 engines in landing
	altitude_landing_burn		=			150				# altitude for shutdown engines
	deploy_legs					=			12				# deploy landing legs
	profile						=			"New Shepard"	# profile landing
	sound 						= 			False 			# sound script landing	

	landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, profile, sound)

main()