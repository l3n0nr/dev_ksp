#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_advanced

def main():
	alturaPouso					=			30				# DEFAULT
	engines_landing				=			24				# 8/8 engines in landing * 3
	altitude_landing_burn		=			300				# altitude for shutdown unnecessary engines
	deploy_legs					=			100				# deploy landing legs

	landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, "Falkinho Triplo", True)

main()

# import sys
# sys.path.insert(0, '../')
# from base import landing

# landing()