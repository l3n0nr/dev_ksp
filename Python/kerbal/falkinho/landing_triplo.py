#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			35				# DEFAULT
	engines_landing				=			24				# all engines: liquid _ solid
	altitude_landing_burn		=			1000			# altitude for shutdown unnecessary engines
	deploy_legs					=			100				# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falkinho Triplo", True)

main()