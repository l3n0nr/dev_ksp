#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../../')
from base import falkinho_triplo

def main(): 
    #####################################################################
    #                             
    target_altitude         = 150000    
    taxa                    = 0.15                   # 36.000 kg payload    
    #
    #####################################################################

    falkinho_triplo(1000,45000,target_altitude, 25000, 70000, taxa, 90, "True")

main()