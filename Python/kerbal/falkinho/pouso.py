# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Reference: https://krpc.github.io/krpc/tutorials/launch-into-orbit.html

import math
import time
import krpc

from numpy.linalg import *
from numpy import array
from time import sleep
from math import exp,sqrt,cos,pi,acos

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

## copia e cola
ut = conn.add_stream(getattr, ksc, 'ut')
altitude = conn.add_stream(getattr, nave.flight(rf), 'mean_altitude')
apoastro = conn.add_stream(getattr, nave.orbit, 'apoapsis_altitude')
recursos_estagio_1 = nave.resources_in_decouple_stage(stage=2, cumulative=False)
combustivel1 = conn.add_stream(recursos_estagio_1.amount, 'LiquidFuel')
recursos_estagio_2 = nave.resources_in_decouple_stage(stage=0, cumulative=False)
combustivel2 = conn.add_stream(recursos_estagio_2.amount, 'LiquidFuel')
altitude_nivel_mar = conn.add_stream(getattr, nave.flight(rf), 'mean_altitude')
velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')
velocidade_horizontal = conn.add_stream(getattr, nave.flight(rf), 'horizontal_speed')
velocidade_vertical = conn.add_stream(getattr, nave.flight(rf), 'vertical_speed')
impulso = conn.add_stream(getattr, nave, 'max_thrust')
massatotal = conn.add_stream(getattr, nave, 'mass')
massaseca = conn.add_stream(getattr, nave, 'dry_mass')

# profile launch - low orbit
def launch():   
    turn_start_altitude     = 1000
    turn_end_altitude       = 45000
    target_altitude         = 78000
    maxq_begin              = 12000
    maxq_end                = 70000
    correction_time         = 0.05

    print('Systems nominal for launch. T-3 seconds!')
    time.sleep(1)
    print('3...')
    time.sleep(1)
    print('2...')
    time.sleep(1)
    print('1...')
    time.sleep(1)

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

def curse_centered_addstr(l,pos,scr):
    my,mx=scr.getmaxyx()
    try:
        scr.addstr(pos,mx/2-len(l)/2,l)
    except ERR:
        scr.addstr(my-1,0,"ERROR IN PRINTING")
        pass


def stage(vess):
    vess.control.activate_next_stage()

class runmode:
    def __init__(self,mode=0):
        self.mode = mode
    def __add__(self,n):
        self.mode = self.mode+n
    def __sub__(self,n):
        self.mode = self.mode-n
    def reset(self):
        self.mode = 0
    def finish(self):
        self.mode = -1
    def __nonzero__(self):
        return not self.mode == -1
    def __call__(self,n):
        return self.mode == n
    def __str__(self):
        return "Run Mode: "+str(self.mode)

def check_engines(vessel):
    for eng in vessel.parts.engines:
        if not eng.has_fuel:
            stage(vessel)
            break

def tnorm(tu):
    return float(linalg.norm(array(tu)))

def executemaneuver(conn):
    vessel = conn.space_center.active_vessel
    control = vessel.control
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.orbit.body.reference_frame
    ap.set_pid_parameters(30,0,6)
    ap.engage()

    if len(control.nodes)<1:
        raise NameError('NoNode')


    rm = runmode()

    mynode = control.nodes[0]


    while rm:
        if rm(0):
            dv =  mynode.delta_v
            ########################
            #Only for 1-engine vessels
            for eng in vessel.parts.engines:
                if eng.active:
                    Isp=eng.specific_impulse
                    break
            ########################
            mdot = vessel.max_thrust/9.82/Isp #mass flowrate
            mfoverm0 = exp(-dv/Isp/9.82)
            dt = vessel.mass*(1-mfoverm0)/mdot
            rm+1
        if rm(1):
            ap.target_direction=mynode.burn_vector(vessel.orbit.body.reference_frame)
            print "ETA: {0:0.2f}".format(mynode.time_to-dt/2)
            if mynode.time_to<dt/2:
                rm+1
        if rm(2):
            dvvec=mynode.remaining_burn_vector(vessel.orbit.body.reference_frame)
            ap.target_direction=dvvec
            tcommand = 0.07*mynode.remaining_delta_v
            control.throttle = min(max(tcommand,0),1)
            if tnorm(dvvec)<0.2:
                rm.finish()


    control.throttle = 0

def landing():      
    print ('Reentry core')      

    # if altitude() <= airbrakes:
    #    nave.control.brakes = True

    # if altitude() <= legs:
    #     nave.control.gear = True

    conn = krpc.connect(name='Land Program')
    vessel = conn = krpc.connect(name='Land Program')
    vessel = conn.space_center.active_vessel
    control = vessel.control
    ap = vessel.auto_pilot
    ap.reference_frame = vessel.surface_velocity_reference_frame
    # ap.set_pid_parameters(20,0,4)
    ap.engage()

    ksc = conn.space_center
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame
    altitude = conn.add_stream(getattr, nave.flight(rf), 'mean_altitude')
    taxa = 450
    legs = 250
    airbrakes = 45000

    rm = runmode()

    nengines = 1 # ONLY FOR IDENTICAL ENGINES   
    nave.control.brakes = True

    while True:     
        if altitude() >= taxa:
            if rm(0):
                dv = vessel.flight(vessel.orbit.body.reference_frame).speed
                ########################
                #Only for 1-engine vessels
                for eng in vessel.parts.engines:
                    if eng.active:
                        Isp=eng.specific_impulse
                        break
                ########################
                mdot = vessel.max_thrust/9.82/Isp #mass flowrate
                mfoverm0 = exp(-dv/Isp/9.82)
                dt = vessel.mass*(1-mfoverm0)/mdot
                ap.target_direction=(0,-1,0)
                rm+1
            if rm(1):
                dir=vessel.direction(vessel.surface_velocity_reference_frame)
                angle = acos(abs(dir[1]/tnorm(dir)))*(360./(2.*pi))
                if angle < 1:
                    rm+1
            if rm(2):
                dvvec=vessel.flight(vessel.orbit.body.reference_frame).velocity
                tcommand = 0.1*tnorm(dvvec)
                control.throttle = min(max(tcommand,0),1)
                if tnorm(dvvec)<5:
                    control.throttle=0
                    rm+2
                    continue
                dir=vessel.direction(vessel.surface_velocity_reference_frame)
                angle = acos(abs(dir[1]/tnorm(dir)))*(360./(2.*pi))
                if angle > 5:
                    control.throttle=0
                    rm+1
            if rm(3):
                dir=vessel.direction(vessel.surface_velocity_reference_frame)
                angle = acos(abs(dir[1]/tnorm(dir)))*(360./(2.*pi))
                if angle <2:
                    rm-1
            if rm(4):
                v=vessel.flight(vessel.orbit.body.reference_frame).speed
                T=0
                for eng in vessel.parts.engines:
                    if eng.active:
                        T=T+eng.available_thrust
        #                break        
                g = vessel.orbit.body.surface_gravity
                m = vessel.mass
                hburn = v*v/(T/m-g)/2
                print "{:2.2f} {:2.2f}".format(hburn,vessel.flight(ap.reference_frame).surface_altitude)
                if vessel.flight(ap.reference_frame).surface_altitude < hburn + 50:
                    rm+1
                    control.throttle = 1
            if rm(5):
                if vessel.flight(vessel.orbit.body.reference_frame).speed < 7:
                    rm+1
            if rm(6):
                print vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
                m = vessel.mass
                v=vessel.flight(vessel.orbit.body.reference_frame).speed
                tcommand = v-5
        #        print min(max(0.05*tcommand + m*g/T,0),1)
                control.throttle = min(max(0.1*tcommand + m*g/T,0),1)
                if vessel.flight(vessel.orbit.body.reference_frame).surface_altitude < 10:
                    rm+1
            if rm(7):                
                print vessel.flight(vessel.orbit.body.reference_frame).surface_altitude
                ap.reference_frame = vessel.surface_reference_frame
                ap.target_direction = (1,0,0)
                m = vessel.mass
                v=vessel.flight(vessel.orbit.body.reference_frame).speed
                tcommand = v-0.5
                control.throttle = min(max(0.1*tcommand + m*g/T,0),1)
                if vessel.flight(vessel.orbit.body.reference_frame).surface_altitude < 5:
                    rm.finish()
                    control.throttle=0
                    print ('Landing!')

    control.throttle = 0
    sleep(10)

    # nave.control.brakes = True
    # nave.control.rcs = True
 #    nave.control.sas = True

## call functions
launch()
# landing()

## nao esta chamando as funcoes corretamente, mais perto do que nunca para o suicide burn