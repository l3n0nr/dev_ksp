#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import triplo_landingzone

def main(): 
    # target_altitude         = 180000                    # target 
    target_altitude         = 500000                    # target 
    maxq_begin              = 25000                     # reduce aceleration stage - begin
    maxq_end                = 36000                     # reduce aceleration stage - end
    turn_start_altitude     = 100                       # inclination begin
    turn_end_altitude       = target_altitude           # inclination end
    
    # taxa                  = 0.15                      # dragao NR

    taxa_beco               = 0.18                      # Landing side boosters
    taxa_meco               = (taxa_beco*3)               # Landing central core

    orientation             = 90                        # NORMAL

    triplo_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa_beco, taxa_meco, orientation)

main()