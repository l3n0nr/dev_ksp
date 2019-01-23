#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	#######################################################################################
	# alturaPouso					=			25				# New Shepard I
	alturaPouso					=			32				# New Shepard II

	# deploy_legs					=			180				# New Shepard I
	deploy_legs					=			250				# New Shepard II

	engines_landing				=			1				# 1/3 engines in landing
	altitude_landing_burn		=			1000			# altitude for shutdown engines	
	#######################################################################################

	landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "New Shepard", False)

main()