#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_adv

def main():
	#######################################################################################
	# alturaPouso					=			25				# New Shepard I
	alturaPouso					=			40					# New Shepard II
	#######################################################################################

	landing_adv(alturaPouso, 1, 1000, 250, "New Shepard", False)

main()