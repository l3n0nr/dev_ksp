#!/usr/bin/env python

# import module
# import sys
# sys.path.insert(0, '../')
# from base import landing 

# landing()

import sys
sys.path.insert(0, '../')
from base import landing_simple

def main():
	altura_pouso				=			35
	engines_landing				=			4				# ON
	altitude_landing_burn		=			500

	landing_simple(altura_pouso, engines_landing, altitude_landing_burn)

main()