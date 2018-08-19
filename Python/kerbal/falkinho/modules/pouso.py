#!/usr/bin/env python

## import modules
from base import launch
from base import landing

# variables default
turn_start_altitude     = 1000
turn_end_altitude       = 45000
target_altitude         = 80000
maxq_begin              = 8000
maxq_end                = 60000
correction_time         = 0.05

# start script
launch(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time)
landing()