#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
# from base import landing_advanced
from base import landing_adv

def main():
	#######################################################################################
	alturaPouso					=			25				# default
	engines_landing				=			1				# 1/3 engines in landing
	altitude_landing_burn		=			1000			# altitude for shutdown engines
	deploy_legs					=			180				# deploy landing legs
	#######################################################################################

	# landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, profile, sound)
	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "New Shepard", True)

main()