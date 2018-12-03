#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falkinho_triplo_landingzone

def main(): 
    #####################################################################
    turn_start_altitude     = 2000                               
    maxq_begin              = 28000
    maxq_end                = 32000
    # taxa_meco               = 0
    #####################################################################

    target_altitude         = 300000    
    turn_end_altitude       = (target_altitude/1.5)

    taxa_meco               = 0.18

    # falkinho_triplo_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa_beco, taxa_meco, 90)
    falkinho_triplo_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa_meco, 90)

main()