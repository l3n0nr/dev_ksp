#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	engines_landing				=			1				# 1/3 engines in landing
	altitude_landing_burn		=			500				# altitude for shutdown engines
	deploy_legs					=			50				# distancy for deploy landing legs
	profile						=			"New Shepard"	# profile landing

	landing_advanced(engines_landing, altitude_landing_burn, deploy_legs, profile)

main()