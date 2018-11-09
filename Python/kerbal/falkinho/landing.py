#!/usr/bin/env python

import sys
sys.path.insert(0, '../')
from base import landing_simple

def main():
	altura_pouso				=			35
	engines_landing				=			4				# engines in landing
	altitude_landing_burn		=			1200			# deploy legs

	landing_simple(altura_pouso, engines_landing, altitude_landing_burn)

main()