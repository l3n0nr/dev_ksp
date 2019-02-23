#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			50				# DEFAULT	
	engines_landing				=			8				# ??		
	altitude_landing_burn		=			3000			# altitude for shutdown unnecessary engines
	deploy_legs					=			300				# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falkinho", True)

main()