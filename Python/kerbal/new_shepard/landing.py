#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	#######################################################################################
	#
	alturaPouso					=			30					# New Shepard III
	#
	#######################################################################################

	landing_adv(alturaPouso, 3, 1000, 300, "New Shepard", False)

main()