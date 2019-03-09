#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import falkinho_triplo

def main(): 
    #####################################################################
    profile                 = "Falkinho Triplo"
    turn_start_altitude     = 1000                               
    maxq_begin              = 28000
    maxq_end                = 70000
    turn_end_altitude       = 45000
    #####################################################################

    target_altitude         = 120000    

    taxa                    = 0.15                   # 36.000 kg payload    

    falkinho_triplo(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, 90, profile)

main()