#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import titan_x

def main():
    ######################################################################################
    ## ASTEROID 01
    target_altitude         = 150000                    # altitude default          
    sepatron 				= 32 						# ???
    #
    ######################################################################################

    titan_x(1000,45000,target_altitude, 30000, 36000, 1, 90, sepatron)

main()