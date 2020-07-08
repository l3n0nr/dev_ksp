#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falkinho_landing_zone

def main(): 

    ###############################################################################
    #    
    # taxa                  = 0.20                # DEMO              23.000 kg
    taxa                  = 0.24                # DeOrbit IIII      07.125 kg  
    #
    ###############################################################################
    #
    # MINIMIUM DELTA-V 
    #   SECOND STAGE - CIRCULARIZATION BURN: +/- 1500 m/s
    #   FIRST STAGE: 20% [ Boostback + Reentry Burn + Landind Burn ]
    #
    ###############################################################################
    #
    falkinho_landing_zone(1000,213333,250000, 26000, 36000, taxa, 90, True)

main()