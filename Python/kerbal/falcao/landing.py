#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			40				# landing way 		- 		GENERIC
	engines_landing				=			1				# engines on
	altitude_landing_burn		=			1800			# altitude for shutdown unnecessary engines
	deploy_legs					=			200				# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falkinho", True)

main()