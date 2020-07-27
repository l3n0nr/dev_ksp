#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			32				# landing way
	engines_landing				=			10				# shutdown engines on landing 
	altitude_landing_burn		=			2000			# altitude for shutdown unnecessary engines
	deploy_legs					=			100				# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falcao", True)

main()