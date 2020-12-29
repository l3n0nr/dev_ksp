#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falkinho

def main(): 
    #################################################################################
    #
    target_altitude         = 250000                                        
    turn_end_altitude       = (target_altitude/1.17)     
    #
    ###############################################################################
    #       X                   Value               Profile                 Weight 
    ###############################################################################
    #    
    taxa                    = 0.24                  # DeOrbit IIII      07.125 kg  
    #
    ###########################     LEGACY          ###############################
    #
    # taxa                  = 0.20                  # DEMO              23.000 kg
    #
    ###############################################################################
    #
    # MINIMIUM DELTA-V 
    #   SECOND STAGE - CIRCULARIZATION BURN: +/- 1500 m/s
    #   FIRST STAGE: 20% [ Boostback + Reentry Burn + Landind Burn ]
    #
    ###############################################################################
    #
    falkinho(1000,turn_end_altitude,target_altitude, 26000, 36000, taxa, 90, True)

main()