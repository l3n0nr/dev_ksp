#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			30				# DEFAULT	
	engines_landing				=			10				# all engines ON
	altitude_landing_burn		=			3000			# altitude for shutdown unnecessary engines
	deploy_legs					=			200				# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Hooper", True)

main()