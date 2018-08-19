#!/usr/bin/env python

# Reference: https://krpc.github.io/krpc/tutorials/launch-into-orbit.html

import math
import time
import krpc

conn = krpc.connect(name='Launch into orbit')
vessel = conn.space_center.active_vessel
ksc = conn.space_center
nave = ksc.active_vessel
rf = nave.orbit.body.reference_frame

# Set up streams for telemetry
# general
ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')    

# landing
recursos_estagio_1 = nave.resources_in_decouple_stage(stage=2, cumulative=False)
combustivel1 = conn.add_stream(recursos_estagio_1.amount, 'LiquidFuel')
recursos_estagio_2 = nave.resources_in_decouple_stage(stage=0, cumulative=False)
combustivel2 = conn.add_stream(recursos_estagio_2.amount, 'LiquidFuel')

# profile launch - low orbit
def launch():   
    turn_start_altitude     = 1000
    turn_end_altitude       = 45000
    target_altitude         = 82000
    maxq_begin              = 12000
    maxq_end                = target_altitude
    correction_time         = 0.05

    print('Systems nominal for launch. T-3 seconds!')
    time.sleep(3)

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1.0

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, 90)  # NORMAL
    
    print('Ignition!')

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0
    while True:      
        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, 90)   # NORMAL

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                print('----Strongback separated')
                print('LIFTOOF!')                        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50
        else:
            vessel.control.throttle = 1.0

        if vessel.available_thrust == 0.0:                
            vessel.control.throttle = 0.30

            vessel.control.activate_next_stage()        
            print('MECO-1')        
            time.sleep(1)

            print('----Separation first stage')            

            vessel.control.activate_next_stage()        
            print('MES-1')      
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print('----Approaching target apoapsis')
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print('MECO-2')
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print('----Coasting out of atmosphere')
    while altitude() < 70500:
        pass

def landing():    
    print ('')    

## call functions
launch()
landing()