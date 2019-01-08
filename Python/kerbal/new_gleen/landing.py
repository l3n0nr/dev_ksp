#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	#######################################################################################
	# alturaPouso					=			34				# approach the ground
	alturaPouso					=			40				# approach the ground
	engines_landing				=			4				# 4/7 engines in landing
	altitude_landing_burn		=			1000			# altitude for shutdown engines
	deploy_legs					=			70				# deploy landing legs
	#######################################################################################
	#
	landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "New Gleen", False)
	#
main()