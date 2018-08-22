#!/usr/bin/env python

## import modules
from base import launch

# variables default
turn_start_altitude     = 1000
turn_end_altitude       = 45000
target_altitude         = 140000
maxq_begin              = 30000
maxq_end                = 70000
correction_time         = 1

# start script
launch(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time)