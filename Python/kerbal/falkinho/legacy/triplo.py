#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../../')
from base import falkinho_triplo

def main(): 
    ##############################################################################
    #                             
    target_altitude         = 520000                           # NOT CHANGE
    
    # core + boosters
    Deorbit garra IIII    = 07.125 kg         
    taxa_central            = 0.30            
    taxa_side               = 0.35

    # DEMO MAX              = 15.000 kg
    # taxa_central            = 0.29            
    # taxa_side               = 0.30

    #
    # MINIMIUM FUEL: CORE 0.29 | BOOSTER 0.30 [ Boostback | Reentry | Landing ]
    #
    ###############################################################################

    falkinho_triplo(1000, target_altitude, 20000, 30000, taxa_central, taxa_side, 90, False)    

main()