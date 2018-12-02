#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	alturaPouso					=			35				# DEFAULT	
	engines_landing				=			4				# 4/8 engines in landing 		
	altitude_landing_burn		=			2000			# altitude for shutdown unnecessary engines
	deploy_legs					=			100				# deploy landing legs

	landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falkinho", True)

main()