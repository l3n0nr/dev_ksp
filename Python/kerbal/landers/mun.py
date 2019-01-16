#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			25				# DEFAULT	
	deploy_legs					=			4000			# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, 1, 100, deploy_legs, "Lander", True)

main()