#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	alturaPouso					=			35				# DEFAULT
	engines_landing				=			3				# 3/8 engines in landing 		
	altitude_landing_burn		=			300				# altitude for shutdown unnecessary engines
	deploy_legs					=			40				# deploy landing legs

	landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falkinho Triplo", True)

main()