#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falkinho_landing_zone

def main(): 

    ###############################################################################
    #
    # DEMO              21.000 kg
    # target_altitude       = 280000               
    # taxa                  = 0.20              

    # DeOrbit IIII      07.125 kg
    target_altitude       = 200000                
    taxa                  = 0.24              

    #
    # MINIMIUM FUEL: 0.20 [ Boostback + Reentry Burn + Landind Burn ]
    #
    ###############################################################################
    #
    falkinho_landing_zone(1000,213333,280000, 26000, 36000, taxa, 90, True)

main()