#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	#######################################################################################
	alturaPouso					=			30				# default
	engines_landing				=			7				# 7 engines in landing
		## Config ship in KSP
	altitude_landing_burn		=			1500			# altitude for shutdown engines
	deploy_legs					=			100				# deploy landing legs
	#######################################################################################

	landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "New Gleen", False)

main()