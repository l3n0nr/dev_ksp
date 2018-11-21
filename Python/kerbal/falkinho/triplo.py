#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import suborbital_triplo

def main():
    ######################################################################################
    turn_start_altitude     = 3000                      # begin inclination
    target_altitude         = 400000                    # target 
    turn_end_altitude       = target_altitude/4         # end inclination 
    maxq_begin              = 34000                     # begin reduce aceleration stages
    maxq_end                = 36000                     # end reduce aceleration stage
    ######################################################################################

    taxa_beco               = 0.16                      # Landing fuel side boosters
    taxa_meco               = taxa_beco*3               # Landing fuel central core

    suborbital_triplo(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa_beco, taxa_meco, 90)

main()
