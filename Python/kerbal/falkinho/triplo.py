#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import suborbital_triplo

def main():
    turn_start_altitude     = 1000                      # inclination begin
    turn_end_altitude       = 45000                     # inclination end
    # target_altitude         = 300000                    # target 

    target_altitude         = 75000                    	# target 

    maxq_begin              = 25000                     # reduce aceleration stage - begin
    maxq_end                = 70000                     # reduce aceleration stage - end    
    orientation             = 90                        # NORMAL

    # taxa_beco               = 0.18                      # Landing side boosters
    # taxa_meco               = taxa_beco*3               # Landing central core

    taxa_beco               = 0.0                      # Landing side boosters
    taxa_meco               = taxa_beco*3               # Landing central core

    suborbital_triplo(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa_beco, taxa_meco, orientation)

main()