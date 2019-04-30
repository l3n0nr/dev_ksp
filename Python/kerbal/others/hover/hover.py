# Reference: github.com/ndeutschmann-fun/ksp-ap/blob/master/hover.py

import krpc, curses, time, sys
import os
import numpy as np
import numpy.linalg as la

os.system('clear')

conn = krpc.connect(name='Docking Guidance')
vessel = conn.space_center.active_vessel
control = vessel.control

kp = 10000
altitude_target = 500
ksc = conn.space_center
rocket = ksc.active_vessel
refer = rocket.orbit.body.reference_frame

def tdef(vessel):
    g = vessel.orbit.body.surface_gravity
    return g*vessel.mass/vessel.available_thrust

## pre-check
vessel.control.throttle = 1
time.sleep(3)
vessel.control.sas = True

## ignition
vessel.control.activate_next_stage()

tmem = conn.space_center.ut
altmem = vessel.flight().surface_altitude
speed = float(rocket.flight(refer).speed)

tmemprint = conn.space_center.ut - 0.1

while True:  
    alt=vessel.flight().surface_altitude
    dt = conn.space_center.ut-tmem

    if dt>0:    
        vessel.control.throttle = tdef(vessel)+kp*(altitude_target-alt)+kp*(altmem-alt)/dt
        if (conn.space_center.ut-tmemprint>0.1):            
            tmemprint = conn.space_center.ut
        tmem = conn.space_center.ut