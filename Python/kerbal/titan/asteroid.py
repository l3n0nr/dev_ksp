#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import titan

def main():
    ######################################################################################
    ## ASTEROID 01
    target_altitude         = 150000                    # altitude default          
    orientation             = 45                       	# TOP
    #
    ######################################################################################

    titan(1000,45000,target_altitude, 32000, 36000, orientation, "Titan", True, 1)

main()