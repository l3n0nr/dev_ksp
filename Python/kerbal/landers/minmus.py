#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	###################################################################################################
	alturaPouso					=			50				# DEFAULT	
	deploy_legs					=			200				# deploy landing legs
	###################################################################################################

	landing_adv(alturaPouso, 1, 0, deploy_legs, "Lander", True)

main()