#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	#######################################################################################
	#
	alturaPouso					=			27					# New Shepard IV
	#
	#######################################################################################

	landing_adv(alturaPouso, 3, 1000, 300, "New Shepard", False)

main()