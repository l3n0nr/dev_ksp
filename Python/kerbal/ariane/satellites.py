#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ariane

def main():
    #######################################################################################
    turn_start_altitude     = 2000                      # inclination begin
    turn_end_altitude       = 45000                     # inclination end   
    maxq_begin              = 34000                     # reduce aceleration stage - begin
    maxq_end                = 36000                     # reduce aceleration stage - end    
    #######################################################################################
    #
    # 1 satellite mission + 1 satellite geo     -       NORMAL
    # orientation               = 90                
    # target_altitude           = 120000

    # Sat Tundra I                              -       DOWN(180-25) 
    # orientation               = 155
    # target_altitude           = 100000
    
    # Surveilance Camera II                     -       DOWN
    # orientation               =   180
    # target_altitude           =   120000

    # ## Ariane IV        -           3 GEO + 1 MINMUS
    # orientation             = 90              #       NORMAL
    # target_altitude         = 120000

    ## Ariane IV        -           3 GEO(MINMUS)
    # orientation             = 90                #       NORMAL
    # target_altitude         = 400000

    ## Ariane IV        -           3 GEO(Eevee)
    orientation             = 90                #       NORMAL
    target_altitude         = 360000
    #
    ariane(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, orientation)

main()