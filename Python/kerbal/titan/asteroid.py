#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import titan

def main():
    ######################################################################################
    ## ASTEROID 01
    target_altitude         = 150000                    # altitude default          
    orientation             = 0                       # TOP-NORMAL 
    #
    ######################################################################################

    titan(1000,45000,target_altitude, 30000, 36000, orientation, "Titan")

main()