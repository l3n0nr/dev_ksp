#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			33				# DEFAULT	
	engines_landing				=			4				# 4/8 engines in landing 		
	altitude_landing_burn		=			1500			# altitude for shutdown unnecessary engines
	deploy_legs					=			100				# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falkinho", True)

main()