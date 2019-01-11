#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			50				# DEFAULT	
	engines_landing				=			1				# enginges in landing 		
	altitude_landing_burn		=			0				# altitude for shutdown unnecessary engines
	deploy_legs					=			3000			# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Lander", True)

main()