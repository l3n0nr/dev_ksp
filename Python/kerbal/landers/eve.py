#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	# alturaPouso					=			40				# DEFAULT	
	alturaPouso					=			30				# FALCAO	
	engines_landing				=			50				# ALL engines - MAX	
	altitude_landing_burn		=			3000			# altitude for shutdown unnecessary engines
	deploy_legs					=			150				# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Lander", True)

main()