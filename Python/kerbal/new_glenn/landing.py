#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	#######################################################################################
	alturaPouso					=			40				# approach the ground
	engines_landing				=			4				# 4/7 engines in landing
	altitude_landing_burn		=			1000			# altitude for shutdown engines
	deploy_legs					=			70				# deploy landing legs
	#######################################################################################
	
	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "New Glenn", True)
	
main()