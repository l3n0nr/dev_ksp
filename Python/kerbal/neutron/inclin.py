#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import neutron

def main():
    #################################################################
    # target_altitude       =       110000
    # orientation           =       41.7

    # target_altitude       =       100000
    # orientation           =       139.2

    # target_altitude       =       100000
    # orientation           =       315

    # target_altitude       =       105000
    # orientation           =       160

    target_altitude         =       120000
    orientation             =       100

    #################################################################

    neutron(1000,45000,target_altitude, 30000, 36000, 1, orientation)

main()