#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			38				# landing way
	engines_landing				=			30				# engines on in landing 
	altitude_landing_burn		=			4000			# altitude for shutdown unnecessary engines
	deploy_legs					=			200				# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falcao", True)

main()