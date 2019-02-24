#!/usr/bin/env python
# -*- coding: utf-8 -*-

## import library's
import os, sys, math, time, krpc, pygame

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

################################# BEGIN GENERIC FUNCTIONS #################################
## Generic countdown - T-10s
def countdown():
    sequence = [ "|---      ALL SYSTEMS NOMINAL FOR LAUNCH      ---|",
                "Director flight: GO...",
                "Internal power...",
                "Computer Flight: GO...",
                "Temperatures: OK...",                                                             
                "Gimbal rocket: OK...",                 
                "Navigation system: OK...",
                "Ground control: GO...",                  
                "Ready for launch...",      
                "GO GO GO!"]

    x = 1    
    for x in range(len(sequence)):           
        if x == 0:            
            print sequence[x]
        else:
            print "...", sequence[x]
        time.sleep(1)

    time.sleep(1)

### Generic message - Orbital
def orbit():
    print "|---       ORBITAL INSERTION COMPLETE         ---|"    

### Generic message - SubOrbital
def suborbital():
    print "|---      SUB-ORBITAL INSERTION COMPLETE      ---|"    

### Gereric check - fuel
def check_fuel(conn, vessel, srb_fuel, srb_fuel_1, srb_fuel_2, solid_boosters, srb_tx):
    # conn = krpc.connect(name='Launch into orbit')
    # vessel = conn.space_center.active_vessel

    # ## STAGE
    # stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    # srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    # ## first stage 
    # stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    # srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    # ## second stage
    # stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=False)
    # srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')       

    # # solid boosters
    # stage_solid = vessel.resources_in_decouple_stage(stage=2, cumulative=True)
    # solid_boosters = conn.add_stream(stage_solid.amount, 'SolidFuel')  

    if srb_fuel == 0 or srb_fuel_1() == 0 or srb_fuel_2() == 0 or solid_boosters() == 0:        
        print "###################################################"
        print "[ERROR] CHECK YOUR VESSEL, NOT POSSIBLE READ FUEL!"
        print "###################################################"
        print "Stage:", srb_fuel()
        print "First Stage:", srb_fuel_1()
        print "Second Stage:", srb_fuel_2()
        print "SRB:", solid_boosters()
        print "############################"
        time.sleep(60)

################################# END GENERIC FUNCTIONS #################################
#
#
################################# BEGIN ESPECIFIC FUNCTIONS #################################
# Profile launch: Not recovery first stage
def saturninho(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, taxa, orientation):            
    pitch_row = False

    maq1 = False
    maq1_v = 410

    maxq = False

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')
    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # play sound t-10
    if sound:
        pygame.init()
        pygame.mixer.music.load("../audio/liftoof_apollo.wav")
        pygame.mixer.music.play()

    # call function for countdown
    countdown()

    print "... T-01s: IGNITION!"        
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1.0            

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
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                print "LIFTOOF!"                        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row" 
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if srb_fuel_2() <= srb_tx or vessel.available_thrust == 0.0:                         
            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            print "... Separation first stage" 
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(5)                    

            print "SES-1"     
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO-1"
    vessel.control.throttle = 0.0

    # if vessel.available_thrust == 0.0:
    #     print "MECO"
    #     vessel.control.throttle = 0.0
    #     time.sleep(1)

    #     print "... Separation first stage" 
    #     vessel.control.throttle = 0.30            
    #     vessel.control.activate_next_stage()            
    #     time.sleep(5)                    

    #     print "SES-1"     
    #     vessel.control.activate_next_stage()                    
    #     time.sleep(1)   
    #     break        

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.control.light = True
    vessel.control.rcs = True
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2"  
    # vessel.control.throttle = 1.0            
    vessel.control.throttle = 0.5

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.10
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()

    # Resources
    vessel.control.sas = True
    vessel.control.rcs = False

    ## call function for show message
    orbit()

# Profile launch: Launch - Suborbital insertion - Landing first stage..
def falkinho(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation):        
    pitch_row = False
    maxq = False
    maq1 = False
    maq1_v = 410
    solar_panels = False

    sound = True

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    # stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    # srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    # stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=False)
    # srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    # solid_boosters = 0.0

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # check_fuel(conn, vessel, srb_fuel, srb_fuel_1, srb_fuel_2, solid_boosters)

    if srb_tx == 0:
        print "HOLD HOLD HOLD"
        print "[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!"
        time.sleep(60)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_falcon9.wav")
        pygame.mixer.music.play()

    # call function for countdown
    countdown()

    print "... IGNITION!"    
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 0.75
    
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
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                vessel.control.throttle = 1.0
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_falcon9.wav")
                pygame.mixer.music.play()                        

            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_2() <= srb_tx or vessel.available_thrust == 0.0:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_falcon9.wav")
                pygame.mixer.music.play()

            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            print "... Separation first stage"
            print "... Fairing separation"            
            time.sleep(3)                 

            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(1)                    
    
            print "SES"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO"
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    suborbital()

# Profile launch: Suborbital insertion and landing attemp in the KSC or VAB.... \o
def falkinho_landing_zone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_row = False
    maxq = False
    maq1 = False
    maq1_v = 410
    meco = False
    solar_panels = False

    # sound = True

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # print srb_tx()

    # time.sleep(3)

    if srb_tx == 0:
        print "HOLD HOLD HOLD"
        print "[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!"
        time.sleep(60)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_falcon9.wav")
        pygame.mixer.music.play()
        countdown()

    print "... IGNITION!"
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 0.75
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:          
        # Gravity turn
        if altitude() >= turn_start_altitude and altitude() <= turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))       

            if not meco:
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.5:
                    turn_angle = new_turn_angle
                    vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                vessel.control.throttle = 1.0
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_falcon9.wav")
                pygame.mixer.music.play()                        

            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_2() <= srb_tx:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_falcon9.wav")
                pygame.mixer.music.play()
                meco = True

            if meco:
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.01:                
                    turn_angle = new_turn_angle
                    vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

            print "MECO"
            vessel.control.throttle = 0.0

            print "... Separation first stage"
            print "... Fairing separation"
            time.sleep(3)                    

            vessel.control.activate_next_stage()    
            vessel.control.throttle = 0.50            
            time.sleep(1)                    
    
            print "SES"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO"
    vessel.control.throttle = 0.0

    # Plan circularization burn (using vis-viva equation)
    # time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    time.sleep(1)

    vessel.control.sas = False
    vessel.control.rcs = False

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    suborbital()

def landing():        
    conn = krpc.connect(name='Suicide Burn')
    vessel = conn.space_center.active_vessel
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    situacao = conn.add_stream(getattr, vessel, 'situation')
    pousado_agua = conn.space_center.VesselSituation.splashed
    pousado = conn.space_center.VesselSituation.landed
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

    ksc = conn.space_center
    naveAtual = ksc.active_vessel

    secure_burn = False

    def landing_main():                
        print "Reentry Atmosphere..."    

        global pouso
        pouso = False    
        reentry_burn = False
        landing_burn = False
        landing = False        

        sound = True        

        ksc = conn.space_center
        foguete = ksc.active_vessel

        foguete.control.throttle = 0
        foguete.control.activate_next_stage()  # inicia zerando throttle e ligando motores   

        while pouso == False:
            # Variaveis
            # ksc = conn.space_center
            # foguete = ksc.active_vessel
            refer = foguete.orbit.body.reference_frame
            centroEspacial = conn.space_center
            # naveAtual = ksc.active_vessel
            vooNave = foguete.flight(refer)
            pontoRef = foguete.orbit.body.reference_frame
            UT = conn.space_center.ut
            TWRMax = float()
            distanciaDaQueima = float()
            tempoDaQueima = float()
            acelMax = float()

            #####################
            # alturaPouso = 20.0
            # alturaPouso = 35.0    # funciona mas com touchdown rapido
            # alturaPouso = 40.0
            alturaPouso = 50.0  # funcionando
            #####################

            speed = float(foguete.flight(refer).speed)
            altitudeNave = foguete.flight(refer).bedrock_altitude
            elevacaoTerreno = foguete.flight(refer).elevation
            massaTotalNave = foguete.mass
            velVertNave = foguete.flight(refer).vertical_speed
            piloto = foguete.auto_pilot
            refer = foguete.orbit.body.reference_frame
            vooNave = foguete.flight(refer)
            surAlt = foguete.flight(refer).surface_altitude
            elevacaoTerreno = foguete.flight(refer).elevation
            velVertNave = foguete.flight(refer).vertical_speed
            massa = foguete.mass
            empuxoMax = foguete.max_thrust                

            foguete.control.sas = True
            # vessel.control.rcs = True
            foguete.control.rcs = True
            # foguete.control.sas_mode = foguete.control.sas_mode.retrograde
            piloto.engage()
            piloto.target_pitch_and_heading(90, 90)

            naveAtual.control.brakes = True
            forcaGravidade = foguete.orbit.body.surface_gravity
            TWRMax = empuxoMax / (massa * forcaGravidade)
            acelMax = (TWRMax * forcaGravidade) - forcaGravidade
            tempoDaQueima = speed / acelMax
            distanciaDaQueima = speed * tempoDaQueima + 1 / 2 * acelMax * pow(tempoDaQueima, 2)
            distanciaPouso = alturaPouso

            global ultCalculo
            ultCalculo = 0  # tempo do ultimo calculo
            global valorEntrada
            valorEntrada = float(surAlt)
            global valorSaida
            valorSaida = float()
            global valorLimite
            valorLimite = float(distanciaPouso + distanciaDaQueima)  # variáveis de valores

            global ultValorEntrada
            ultValorEntrada = float()  # variáveis de cálculo de erro

            global kp
            kp = float(.022)  # .023
            global ki
            ki = float(.001)  # .001
            global kd
            kd = float(1)  # 1

            global amostraTempo
            amostraTempo = 25 / 1000  # tempo de amostragem

            global saidaMin
            global saidaMax
            saidaMin = float(-1)
            saidaMax = float(1)  # limitar saída dos valores

            #
            global agora
            global mudancaTempo
            agora = ksc.ut  # var busca tempo imediato
            mudancaTempo = agora - ultCalculo  # var compara tempo calculo

            global termoInt
            termoInt = float()

            def computarPID():            
                global ultCalculo
                global ultValorEntrada
                global valorSaida
                global termoInt

                agora = ksc.ut  # var busca tempo imediato
                mudancaTempo = agora - ultCalculo  # var compara tempo calculo

                if mudancaTempo >= amostraTempo:  # se a mudança for > q o tempo de amostra, o calculo é feito
                    # var calculo valor saida
                    erro = valorLimite - valorEntrada
                    termoInt += ki * erro
                    if termoInt > saidaMax:
                        termoInt = saidaMax
                    elif termoInt < saidaMax:
                        termoInt = saidaMin
                    dvalorEntrada = (valorEntrada - ultValorEntrada)
                    # computando valor saida
                    valorSaida = kp * erro + ki * termoInt - kd * dvalorEntrada
                    if valorSaida > saidaMax:
                        valorSaida = saidaMax
                    elif valorSaida < saidaMin:
                        valorSaida = saidaMin

                    # relembra valores atuais pra prox

                    ultValorEntrada = valorEntrada
                    ultCalculo = agora

                if termoInt > saidaMax:
                    termoInt = saidaMax
                elif termoInt < saidaMin:
                    termoInt = saidaMin
                if valorSaida > saidaMax:
                    valorSaida = saidaMax
                elif valorSaida < saidaMin:
                    valorSaida = saidaMin

                return (valorSaida)

            # Imprimir informacoes
            print "TWR           : %f" % TWRMax
            print "Dist. Queima  : %f" % distanciaDaQueima
            print "Altitude Voo  : %d" % surAlt
            print "Elev. Terreno : %d" % elevacaoTerreno
            print "Correcao      : %f" % computarPID()  # esse valor que nao esta atualizando, e deveria atualizar

            novaAcel = 1 / TWRMax + computarPID()  # calculo de aceleracao

            print "Acc Calculada : %f" % novaAcel
            print "                  "

            # text.content = 'Correcao: %f' % computarPID()  # mostra calculo na tela do jogo

            if surAlt <= 36000 and not reentry_burn and naveAtual.control.throttle != 0:
                print "Reentry burn..."
                reentry_burn = True

                # if sound:
                #     # play sound
                #     pygame.init()
                #     pygame.mixer.music.load("audio/reentryburn_falcon9.wav")
                #     pygame.mixer.music.play()                

            if surAlt <= 800 and not landing_burn and naveAtual.control.throttle != 0:
                print "Landing burn..."
                landing_burn = True

                # if sound:
                #     # play sound
                #     pygame.init()
                #     pygame.mixer.music.load("audio/landing_falcon9.wav")
                #     pygame.mixer.music.play()                

            if surAlt < 300 and naveAtual.control.throttle != 0:         
                naveAtual.control.gear = True  # altitude para trem de pouso

            if surAlt > 200:
                naveAtual.control.gear = False
            if situacao() == pousado or situacao() == pousado_agua:
                naveAtual.control.throttle = 0
                pouso = True

            elif speed <= 6:
                naveAtual.control.throttle = .1            
            else:
                naveAtual.control.throttle = novaAcel
            if speed <= 1:
                naveAtual.control.throttle = 0                    
            #time.sleep(0)

    if situacao() != pousado or situacao() != pousado_agua :
        landing_main()
    else:        
        print "ok"        

    naveAtual.control.throttle = 0
    vessel.control.rcs = True
    vessel.control.sas = True
    time.sleep(2)
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.brakes = False    
        
    print("LANDING!")

# Profile launch: Launch - Deploy probe - And.. next launch!
def ariane(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation):            
    pitch_row = False
    maq1 = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True

    maq1_v = 410

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    ## first stage 
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    ## second stage
    stage_2 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')       

    # solid boosters
    stage_solid = vessel.resources_in_decouple_stage(stage=2, cumulative=True)
    solid_boosters = conn.add_stream(stage_solid.amount, 'SolidFuel')  

    if sound:
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_ariane.wav")
        pygame.mixer.music.play()

    # call function for countdown - t10s
    countdown()
    time.sleep(1)    

    print "... Ignition center engine!"

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False          
    vessel.control.throttle = 0.30 

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    time.sleep(5)    

    while True:   
        srb_tx = (srb_fuel_2() - srb_fuel_1())

        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.throttle = 1
                vessel.control.activate_next_stage()
                srbs_separated = True
                print "... Ignition solid's boosters!"
                print "LIFTOOF!"                       

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row" 
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if solid_boosters() <= 1 and not boosters_separation:
            print "... Boosters Separation"
            vessel.control.activate_next_stage()
            boosters_separation = True
   
        if vessel.available_thrust == 0.0 and boosters_separation:
            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)            

            print "... Separation first stage"
            print "... Fairing separation"
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(3)                 

            print "SES-1"     
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"            
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO-1"
    vessel.control.rcs = True
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2"
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.50
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()
    print "SECO-2"

    # Resources
    vessel.control.sas = False
    vessel.control.rcs = False

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels" 
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True 

    ## call function for show message
    orbit()

# Profile launch: Launch - Suborbital insertion - Landing first stage..
def newshepard(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation):
    pitch_row = False
    maxq = False
    maq1 = False
    maq1_v = 410
    solar_panels = False

    sound = True

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    if srb_tx == 0:
        print "HOLD HOLD HOLD"
        print "[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!"
        time.sleep(60)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_newshepard.wav")
        pygame.mixer.music.play()

    countdown()    

    print "... IGNITION!"   
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False    
    vessel.control.throttle = 0.90
    
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
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                vessel.control.throttle = 1.0    
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"

            pitch_row = True

        if altitude() >= maxq_begin and not maxq:                                
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_newshepard.wav")
                pygame.mixer.music.play()

            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_2() <= srb_tx:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_newshepard.wav")
                pygame.mixer.music.play()

            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            print "... Separation first stage"
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(1)                    

            print "SES"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            # print "... T+", seconds, "... Approaching target apoapsis"
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO"
    vessel.control.throttle = 0.0

    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate   

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels" 
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True 

    ## call function for show message
    suborbital()

# Profile launch: Suborbital insertion and landing attemp in the KSC or VAB.... \o
def newshepard_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_row = False
    maxq = False
    maq1 = False
    maq1_v = 410
    meco = False
    solar_panels = False

    # sound = True

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    if srb_tx == 0:
        print "HOLD HOLD HOLD"
        print "[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!"
        time.sleep(60)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_newshepard.wav")
        pygame.mixer.music.play()
        countdown()

    print "... IGNITION!"
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 0.90
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:          
        # Gravity turn
        if altitude() >= turn_start_altitude and altitude() <= turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))       

            if not meco:
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.5:
                    turn_angle = new_turn_angle
                    vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                vessel.control.throttle = 1.0
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_newshepard.wav")
                pygame.mixer.music.play()                        

            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_2() <= srb_tx:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_newshepard.wav")
                pygame.mixer.music.play()
                meco = True

            if meco:
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.01:                
                    turn_angle = new_turn_angle
                    vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            print "... Separation first stage"
            vessel.control.activate_next_stage()    
            vessel.control.throttle = 0.50            
            time.sleep(1)                    
    
            print "SES"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO"
    vessel.control.throttle = 0.0

    # Plan circularization burn (using vis-viva equation)
    # time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    time.sleep(1)

    vessel.control.sas = False
    vessel.control.rcs = False

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    suborbital()


# Reference: <krpc.github.io/krpc/tutorials/launch-into-orbit.html>
# Profile launch: Not recovery first stage
def shuttle(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation):            
    pitch_row = False
    maq1 = False    
    boosters_separation = False
    maxq = False

    maq1_v = 410

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    ## STAGE
    stage_2_resources = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    ## first stage 
    # stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    # srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=1, cumulative=True)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    ## second stage
    # stage_2 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    # srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')       

    # solid boosters
    stage_solid = vessel.resources_in_decouple_stage(stage=1, cumulative=True)
    solid_boosters = conn.add_stream(stage_solid.amount, 'SolidFuel')   

    ## pre-check fuel
    # check_fuel(conn, vessel, srb_fuel, srb_fuel_1, srb_fuel_2, solid_boosters, srb_tx)

    # print srb_fuel()       
    print srb_fuel_1()
    # print srb_fuel_2()
    print solid_boosters()

    # time.sleep(10)

    # # play sound t-10
    # if sound:
    #     pygame.init()
    #     pygame.mixer.music.load("../audio/liftoff_ariane.wav")
    #     pygame.mixer.music.play()

    # call function for countdown - t10s
    # countdown() 

    time.sleep(1)
    print "... Ignition center engine!"         

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False    
    vessel.control.throttle = 0.30            

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    time.sleep(1)    

    while True:   
        # srb_tx = (srb_fuel_2() - srb_fuel_1())

        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            # if srb_fuel() < 0.1:
            # vessel.control.throttle = 1
            vessel.control.throttle = 0.50            
            vessel.control.activate_next_stage()
            srbs_separated = True
            print "LIFTOOF!"                        

        # if altitude() >= maxq_begin and altitude() <= maxq_end:
        #     vessel.control.throttle = 0.50            
        # else:
        #     vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            vessel.control.rcs = True
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if solid_boosters() <= 1 and not boosters_separation:
            print "... Boosters Separation"
            vessel.control.activate_next_stage()
            # vessel.control.rcs = True
            boosters_separation = True
            vessel.control.throttle = 1            
        
        if vessel.available_thrust == 0.0 and boosters_separation:
        # if srb_fuel_2() == 0 and boosters_separation:                        
        # if srb_fuel_1() == 0 and boosters_separation:                        
            print "External Tank Separation"
            vessel.control.throttle = 0.0
            vessel.control.activate_next_stage()            
            time.sleep(3)                 

            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO"
    vessel.control.rcs = False
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print "... Orientating ship for circularization burn"
    # vessel.control.light = True
    # vessel.control.rcs = True
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2"
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.50
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()

    # Resources
    vessel.control.sas = False
    vessel.control.rcs = False

    ## call function for show message
    orbit()

# def boostback(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation):        
def boostback(value):
    conn = krpc.connect(name='Launch into orbit')
    vessel = conn.space_center.active_vessel
    ksc = conn.space_center    
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame

    ## pre-check
    # vessel.control.sas = True
    # vessel.control.rcs = True  

    # Set up streams for telemetry
    # general
    ut = conn.add_stream(getattr, conn.space_center, 'ut')
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # Plan circularization burn (using vis-viva equation)
    time.sleep(1)
    print "... Calculate boostback burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r 
    # a3 = vessel.orbit.inclination
    # vessel.orbit.inclination == a3*2

    # a3 = vessel.orbit.semi_minor_axis
    v1 = math.sqrt(mu*((2./r)-(1./a1)))

    # v2  = -80             # dragao
    # v2  = -25             # lander mun
    # v2 = 150            # side boosters - not recomend for now

    # delta_v = (v2 - v1)    
    delta_v = (value - v1)   

    # print vessel.orbit.inclination  
    # new_inclination = (((1 - vessel.orbit.inclination) + vessel.orbit.inclination) - 1)
    # print new_inclination
    # print delta_v      

    # time.sleep(10)
    
    # delta_v = abs(v1)    
    # vessel.auto_pilot.target_pitch_and_heading()
    # vessel.orbit.inclination(0)
    node = vessel.control.add_node(ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)    

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    # # Orientate ship
    # print "... Orientating ship for boostback burn')    
    # # vessel.control.sas_mode = vessel.control.sas_mode.retrograde   
    # # vessel.control.sas.mode = node.reference_frame
    # # time.sleep(10)
    # # vessel.control.sas = True
    # vessel.control.rcs = True
    # vessel.auto_pilot.engage()
    # vessel.auto_pilot.reference_frame = node.reference_frame
    # vessel.auto_pilot.target_direction = (0, 1, 0)
    # vessel.auto_pilot.wait()

    # # Wait until burn
    # print "... Waiting until burn')
    # burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    # lead_time = 5   
    # # lead_time = 1   
    # conn.space_center.warp_to(burn_ut - lead_time)

    # # Execute burn
    # print "... Ready to execute burn')
    # time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    # # while time_to_apoapsis() - (burn_time/2.) > 0:
    # #     pass

    # print "Boostback now...')   
    # vessel.control.throttle = 1

    # time.sleep(burn_time - 0.1)
    # print "... Fine tuning')
    # vessel.control.throttle = 0.25
    # remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    # ## manuveur correction
    # while remaining_burn()[1] > 1:
    #     pass

    # vessel.control.throttle = 0.0
    # print "Preparing for reentry burn...')   
    # node.remove()

    # # Active resources for reentry
    # vessel.control.sas = False
    # vessel.control.rcs = True

    # foguete = ksc.active_vessel
    # foguete.control.sas_mode = foguete.control.sas_mode.retrograde    

def landing_advanced(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, profile, sound):               
    conn = krpc.connect(name='Suicide Burn')
    vessel = conn.space_center.active_vessel
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    situacao = conn.add_stream(getattr, vessel, 'situation')
    pousado_agua = conn.space_center.VesselSituation.splashed
    pousado = conn.space_center.VesselSituation.landed
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

    ksc = conn.space_center
    naveAtual = ksc.active_vessel

    secure_burn = False   
    reentry_engines_1 = False
    solar_panels = False

    def landing_main():                      
        global pouso
        pouso = False    
        reentry_burn = False
        landing_burn = False
        landing = False
        space = False
        atmosphere = False        
        reentry_engines = False        
        landing_legs = False   
        solar_panels = False

        cont_shut_engine = 0   

        ksc = conn.space_center
        foguete = ksc.active_vessel

        foguete.control.throttle = 0
        foguete.control.activate_next_stage()  # inicia zerando throttle e ligando motores   

        while pouso == False:
            # Variaveis
            # ksc = conn.space_center
            # foguete = ksc.active_vessel
            refer = foguete.orbit.body.reference_frame
            centroEspacial = conn.space_center
            # naveAtual = ksc.active_vessel
            vooNave = foguete.flight(refer)
            pontoRef = foguete.orbit.body.reference_frame
            UT = conn.space_center.ut
            TWRMax = float()
            distanciaDaQueima = float()
            tempoDaQueima = float()
            acelMax = float()

            #####################
            # alturaPouso = 20.0
            # alturaPouso = 30.0    # ideal
            # alturaPouso = 35.0 
            # alturaPouso = 40.0
            # alturaPouso = 50.0  # funcionando
            #####################

            nave = conn.space_center.active_vessel

            speed = float(foguete.flight(refer).speed)
            altitudeNave = foguete.flight(refer).bedrock_altitude
            elevacaoTerreno = foguete.flight(refer).elevation
            massaTotalNave = foguete.mass
            velVertNave = foguete.flight(refer).vertical_speed
            piloto = foguete.auto_pilot
            refer = foguete.orbit.body.reference_frame
            vooNave = foguete.flight(refer)
            surAlt = foguete.flight(refer).surface_altitude
            elevacaoTerreno = foguete.flight(refer).elevation
            velVertNave = foguete.flight(refer).vertical_speed
            massa = foguete.mass
            empuxoMax = foguete.max_thrust                

            if surAlt > 70000 and not space:
                print "Wait for reentry..."
                space = True

            if surAlt < 70000 and not atmosphere:
                print "Reentry atmosphere..."    
                atmosphere = True

            piloto.engage()
            piloto.target_pitch_and_heading(90, 90)

            ###################
            # foguete.control.sas = True
            # vessel.control.rcs = True
            # foguete.control.rcs = True
            # foguete.control.sas_mode = foguete.control.sas_mode.retrograde
            ###################

            naveAtual.control.brakes = True
            forcaGravidade = foguete.orbit.body.surface_gravity
            TWRMax = empuxoMax / (massa * forcaGravidade)
            acelMax = (TWRMax * forcaGravidade) - forcaGravidade
            tempoDaQueima = speed / acelMax
            distanciaDaQueima = speed * tempoDaQueima + 1 / 2 * acelMax * pow(tempoDaQueima, 2)
            distanciaPouso = alturaPouso

            global ultCalculo
            ultCalculo = 0  # tempo do ultimo calculo
            global valorEntrada
            valorEntrada = float(surAlt)
            global valorSaida
            valorSaida = float()
            global valorLimite
            valorLimite = float(distanciaPouso + distanciaDaQueima)  # variáveis de valores

            global ultValorEntrada
            ultValorEntrada = float()  # variáveis de cálculo de erro

            global kp
            kp = float(.022)  # .023
            global ki
            ki = float(.001)  # .001
            global kd
            kd = float(1)  # 1

            global amostraTempo
            amostraTempo = 25 / 1000  # tempo de amostragem

            global saidaMin
            global saidaMax
            saidaMin = float(-1)
            saidaMax = float(1)  # limitar saída dos valores

            global agora
            global mudancaTempo
            agora = ksc.ut  # var busca tempo imediato
            mudancaTempo = agora - ultCalculo  # var compara tempo calculo

            global termoInt
            termoInt = float()

            def computarPID():            
                global ultCalculo
                global ultValorEntrada
                global valorSaida
                global termoInt

                # reentry_engines = False
                # cont_shut_engine = 0  

                agora = ksc.ut  # var busca tempo imediato
                mudancaTempo = agora - ultCalculo  # var compara tempo calculo

                if mudancaTempo >= amostraTempo:  # se a mudança for > q o tempo de amostra, o calculo é feito
                    # var calculo valor saida
                    erro = valorLimite - valorEntrada
                    termoInt += ki * erro
                    if termoInt > saidaMax:
                        termoInt = saidaMax
                    elif termoInt < saidaMax:
                        termoInt = saidaMin
                    dvalorEntrada = (valorEntrada - ultValorEntrada)
                    # computando valor saida
                    valorSaida = kp * erro + ki * termoInt - kd * dvalorEntrada
                    if valorSaida > saidaMax:
                        valorSaida = saidaMax
                    elif valorSaida < saidaMin:
                        valorSaida = saidaMin

                    # relembra valores atuais pra prox

                    ultValorEntrada = valorEntrada
                    ultCalculo = agora

                if termoInt > saidaMax:
                    termoInt = saidaMax
                elif termoInt < saidaMin:
                    termoInt = saidaMin
                if valorSaida > saidaMax:
                    valorSaida = saidaMax
                elif valorSaida < saidaMin:
                    valorSaida = saidaMin

                return (valorSaida)

            # Imprimir informacoes
            print "TWR           : %f" % TWRMax
            print "Dist. Queima  : %f" % distanciaDaQueima
            print "Altitude Voo  : %d" % surAlt
            print "Elev. Terreno : %d" % elevacaoTerreno
            print "Correcao      : %f" % computarPID()  # esse valor que nao esta atualizando, e deveria atualizar

            # return (TWRMax)
            # return (distanciaDaQueima)
            # return (surAlt)
            # return (elevacaoTerreno)
            # return (computarPID())

            novaAcel = 1 / TWRMax + computarPID()  # calculo de aceleracao

            # return (novaAcel)

            print "Acc Calculada : %f" % novaAcel
            print "                  "

            # text.content = 'Correcao: %f' % computarPID()  # mostra calculo na tela do jogo

            if surAlt <= 36000 and not reentry_burn and naveAtual.control.throttle != 0 and profile=="Falkinho":
                print "Reentry burn..."
                reentry_burn = True

                if sound and profile=="Falkinho":
                    # play sound
                    pygame.init()
                    pygame.mixer.music.load("../audio/reentryburn_falcon9.wav")
                    pygame.mixer.music.play()                

            if surAlt <= altitude_landing_burn and not reentry_engines:
                print "Landing burn..."
                landing_burn = True

                for engines in vessel.parts.engines:            
                    if not reentry_engines:
                        print "... Shutdown engines" 
                        reentry_engines = True  

                    cont_shut_engine = cont_shut_engine + 1                         

                    if engines.active and cont_shut_engine > engines_landing:            
                        engines.active = False

                if sound and profile=="Falkinho" and reentry_burn and reentry_engines:
                    pygame.init()
                    pygame.mixer.music.load("../audio/landing_falcon9.wav")
                    # pygame.mixer.music.load("../audio/others/landingboosters_falconh.wav")
                    pygame.mixer.music.play()                                                                                      

            # landing legs
            if distanciaDaQueima <= deploy_legs and not landing_legs and reentry_engines:
                naveAtual.control.gear = True 
                landing_legs = True

            if surAlt > 200:
                naveAtual.control.gear = False
            if situacao() == pousado or situacao() == pousado_agua:
                naveAtual.control.throttle = 0
                pouso = True

            elif speed <= 6:
                naveAtual.control.throttle = .1            
            else:
                naveAtual.control.throttle = novaAcel
            if speed <= 1:
                naveAtual.control.throttle = 0                    

    if situacao() != pousado or situacao() != pousado_agua :
        landing_main()
    else:        
        print "ok"        

    for painelsolar in vessel.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels" 
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True 

    ## disabled all    
    naveAtual.control.throttle = 0
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.brakes = False    

    for engines in vessel.parts.engines:            
        if not reentry_engines_1:
            print "... Shutdown engines" 
            reentry_engines_1 = True  

        if engines.active:            
            engines.active = False    
        
    time.sleep(8)
    
    print("LANDING!")

# def falkinho_triplo_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa_beco, taxa_meco, orientation): 
def falkinho_triplo(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, profile): 
    pitch_row = False
    maxq = False
    maq1 = False
    beco = False
    maq1_v = 410

    sound = True

    conn = krpc.connect(name=profile)
    vessel = conn.space_center.active_vessel
    ksc = conn.space_center    
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame

    # Set up streams for telemetry
    # general
    ut = conn.add_stream(getattr, conn.space_center, 'ut')
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')
    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')   

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # check if landing
    if taxa > 0:
        landing_boolean = "Yes"
    else:
        landing_boolean = "No"    

    print "... Start launch in: " + profile
    print "... Mass rocket: ??"
    print "... Mass payload: ??"
    print "... Altitude target ??"
    print "... Landing first stage: " + landing_boolean

    # print srb_tx
    # print srb_fuel_1()
    # print srb_fuel_2()

    # time.sleep(10)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_falcon9.wav")
        pygame.mixer.music.play()

    countdown()
 
    print "... Ignition central core!"   
    # Activate the first stage    
    vessel.control.activate_next_stage()
    vessel.control.throttle = 0.30
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    time.sleep(1)

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1.0    
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:          
        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            
            new_turn_angle = frac * 90
            # if abs(new_turn_angle - turn_angle) > 0.5:
            if abs(new_turn_angle - turn_angle) > 0.1:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:                
                vessel.control.activate_next_stage()
                vessel.control.throttle = 1.00
                srbs_separated = True
                print "... Ignition side boosters!"
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"

            pitch_row = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_falcon9.wav")
                pygame.mixer.music.play()                        

            print "... Max-Q"
            maxq = True        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        
                
        if srb_fuel_2() <= srb_tx:           
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_falcon9.wav")
                pygame.mixer.music.play()

            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(2)
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(1)                    
 
            print "SES-1"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO-1"
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    ## call function for show message
    # suborbital()

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2" 
    print "... Circularization burn"
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.50
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()
    print "SECO-2"

    time.sleep(1)

    vessel.control.sas = False
    vessel.control.rcs = False

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    orbit()

# Profile launch: Launch - Deploy probe - And.. next launch!
def lce(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation):            
    pitch_row = False
    maq1 = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True

    maq1_v = 410

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    ## first stage 
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    ## second stage
    stage_2 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')       

    # solid boosters
    stage_solid = vessel.resources_in_decouple_stage(stage=2, cumulative=True)
    solid_boosters = conn.add_stream(stage_solid.amount, 'SolidFuel')  

    if sound:
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_apollo.wav")
        pygame.mixer.music.play()

    # call function for countdown - t10s
    countdown()

    print "... Ignition center engine!"

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False          
    vessel.control.throttle = 0.50 

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:   
        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            
            if not boosters_separation:
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.5:
                    turn_angle = new_turn_angle
                    vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                print "... Ignition solid boosters!"
                vessel.control.throttle = 1
                vessel.control.activate_next_stage()
                srbs_separated = True
                print "LIFTOOF!"                        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if solid_boosters() <= 1 and not boosters_separation:
            print "... Boosters Separation"
            vessel.control.activate_next_stage()
            boosters_separation = True
   
        if boosters_separation:
            new_turn_angle = frac * 90

            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        if vessel.available_thrust == 0.0 and boosters_separation:
            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)            

            print "... Separation first stage"
            # print "... Fairing separation" 
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(3)                 

            print "SES-1"      
            print "... Orbital burn manuveur" 
            vessel.control.activate_next_stage()                    
            time.sleep(1)               
            break        

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"            
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO-1"
    vessel.control.rcs = True
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2" 
    print "... Circularization burn"
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.50
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()
    print "SECO-2"

    time.sleep(1)

    vessel.control.sas = False
    vessel.control.rcs = False

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    orbit()

# Profile launch: Launch - Deploy payload.. and.. next launch!
def neutron(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation):            
    pitch_row = False
    maq1 = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True
    antena = False

    maq1_v = 410

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    ## first stage 
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    ## second stage
    stage_2 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')       

    if sound:
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_generic.wav")
        pygame.mixer.music.play()

    # call function for countdown - t10s
    countdown()

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False          
    vessel.control.throttle = 0.30 

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    # time.sleep(5)    

    while True:   
        srb_tx = (srb_fuel_2() - srb_fuel_1())

        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.throttle = 1
                vessel.control.activate_next_stage()
                srbs_separated = True
                print "LIFTOOF!"                       

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row" 
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True
   
        # if vessel.available_thrust == 0.0 and boosters_separation:
        if vessel.available_thrust == 0.0:
            print "MECO"
            vessel.control.throttle = 0.0
            # time.sleep(1)            

            print "... Separation first stage"
            print "... Fairing separation"
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            # time.sleep(1)                 

            print "SES-1"     
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"            
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO-1"
    vessel.control.throttle = 0.0

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2"
    print "... Orbital burn manuveur"
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.50
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()
    print "SECO-2"

    time.sleep(2)    
    print "... Deploy Satellites"    
    vessel.control.activate_next_stage()                    

    # Resources
    vessel.control.sas = False
    vessel.control.rcs = False

    ## call function for show message
    orbit()

# Profile launch: Launch - Deploy payload.. and.. next launch!
def velorg(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation):            
    pitch_row = False
    maq1 = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True

    maq1_v = 410

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    ## first stage    
    stage_solid = vessel.resources_in_decouple_stage(stage=1, cumulative=True)
    solid_boosters = conn.add_stream(stage_solid.amount, 'SolidFuel')  

    ## second stage 
    stage_2 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')

    ## second stage 
    stage_3 = vessel.resources_in_decouple_stage(stage=3, cumulative=True)
    srb_fuel_3 = conn.add_stream(stage_3.amount, 'LiquidFuel')

    # print srb_fuel()
    # time.sleep(10)

    if sound:
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_generic.wav")
        pygame.mixer.music.play()

    # call function for countdown - t10s
    countdown()
    # time.sleep(1)    

    # print "... Ignition center engine!"

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False          
    vessel.control.throttle = 0.30 

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    # time.sleep(5)    

    while True:   
        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            # if srb_fuel() < 0.1:
                vessel.control.throttle = 1
                # vessel.control.activate_next_stage()
                srbs_separated = True
                print "LIFTOOF!"                       

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            # print "... Heading/Pitch/Row" 
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if solid_boosters() <= 0 and not boosters_separation:
            # print "... Separation first stage"
            print "... Separation solid booster"
            time.sleep(1)
            print "MES-1"
            vessel.control.activate_next_stage()
            boosters_separation = True
   
        # if vessel.available_thrust == 0.0 and boosters_separation:
        #     print "MECO"
        #     vessel.control.throttle = 0.0
        #     time.sleep(1)            

        #     print "... Separation second stage"
        #     print "... Fairing separation"
        #     vessel.control.throttle = 0.30            
        #     vessel.control.activate_next_stage()            
        #     time.sleep(3)                 

        #     print "SES"     
        #     print "... Orbital burn manuveur"
        #     vessel.control.activate_next_stage()                    
        #     time.sleep(1)   
        #     break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"            
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "MECO-1"
    # vessel.control.rcs = True
    vessel.control.throttle = 0.0

    # # Wait until out of atmosphere
    # print "... Coasting out of atmosphere"
    # while altitude() < 70500:
    #     pass

    # Plan circularization burn (using vis-viva equation)
    # time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
        
    print "MES-2"
    print "... Orbital burn manuveur"
    print "... Fairing separation"
    vessel.control.activate_next_stage()
    vessel.control.throttle = 1

    # while True:
    #     if vessel.available_thrust == 0.0 and boosters_separation:
    #         print "MECO-2"
    #         vessel.control.throttle = 0.0
    #         time.sleep(1)            

    #         print "... Separation second stage"
    #         print "... Fairing separation"
    #         vessel.control.throttle = 1.00            
    #         vessel.control.activate_next_stage()            
    #         time.sleep(1)                 

    #         print "SES"     
    #         print "... Orbital burn manuveur-2"
    #         vessel.control.activate_next_stage()                    
    #         time.sleep(1)   
    #         break    

    time.sleep(burn_time - 0.1)
    # print "... Fine tuning"    
    # # vessel.control.throttle = 0.75
    # vessel.control.throttle = 0.30
    # remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)            

    # ## manuveur correction
    # while remaining_burn()[1] > correction_time:
    #     pass
    vessel.control.throttle = 0.0
    node.remove()
    print "MECO-2"

    # Resources
    vessel.control.sas = True
    vessel.control.rcs = False

    # for painelsolar in nave.parts.solar_panels:        
    #     if not solar_panels:
    #         print "... Deploy solar painels" 
    #         solar_panels = True  

    #     if painelsolar.deployable:            
    #         painelsolar.deployed = True 

    ## call function for show message
    orbit()

# Profile launch: Launch - Suborbital insertion - Landing first stage..
def newglenn(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation):        
    pitch_row = False
    maxq = False
    maq1 = False
    maq1_v = 410
    solar_panels = False

    sound = True

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    # stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    # srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    # stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=False)
    # srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    # solid_boosters = 0.0

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # check_fuel(conn, vessel, srb_fuel, srb_fuel_1, srb_fuel_2, solid_boosters)

    if srb_tx == 0:
        print "HOLD HOLD HOLD"
        print "[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!"
        time.sleep(60)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_newshepard.wav")
        pygame.mixer.music.play()

    # call function for countdown
    countdown()

    print "... IGNITION!"    
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:          
        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.05:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                vessel.control.throttle = 1.0
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_newshepard.wav")
                pygame.mixer.music.play()                        

            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_2() <= srb_tx or vessel.available_thrust == 0.0:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_newshepard.wav")
                pygame.mixer.music.play()

            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            print "... Separation first stage"
            time.sleep(1)                 
            print "... Fairing separation"
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(1)                    
    
            print "SES"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO"
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    suborbital()

# Profile launch: Suborbital insertion and landing attemp in the KSC or VAB.... \o
def newglenn_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_row = False
    maxq = False
    maq1 = False
    maq1_v = 410
    meco = False
    solar_panels = False
    fairing = False

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')  

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    #######################################
    ## payload mass
    # payload_mass = vessel.mass.dry_mass()     

    # print "FUEL:", srb_fuel_2()
    # print "FUEL TX:", srb_tx
    # print "MASS:", payload_mass()

    # ((altitude / payload) * fuel)÷1000000
    # time.sleep(10)    

    # tentar com isso
    # massatotal = conn.add_stream(getattr, nave, 'mass')
    # massaseca = conn.add_stream(getattr, nave, 'dry_mass')
    #######################################

    if srb_tx == 0:
        print "HOLD HOLD HOLD"
        print "[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!"
        
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/error.wav")
        pygame.mixer.music.play()

        time.sleep(60)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_newshepard.wav")
        pygame.mixer.music.play()

    # call function for countdown
    countdown()

    print "... IGNITION!"
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:          
        # Gravity turn
        if altitude() >= turn_start_altitude and altitude() <= turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))       

            if not meco:
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.5:
                    turn_angle = new_turn_angle
                    vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                vessel.control.throttle = 1.0
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_newshepard.wav")
                pygame.mixer.music.play()                        

            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_2() <= srb_tx:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_newshepard.wav")
                pygame.mixer.music.play()

            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            print "... Separation first stage"                          
            print "... Fairing separation"
            time.sleep(1)   
            
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(1)                    
    
            print "SES"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break   

        # ## funcionando - VERIFICAR!!!
        # if altitude() >= 60000 and not fairing:
        #     print "... Fairing separation??"        

        #     fairing = True

        # if altitude() >= 1 and not fairing:
        #     for coifa in nave.parts.fairing:        
        #         if not fairing:
        #             print "... Fairing separation"
        #             fairing = True  

        #         # if not fairing.jettison:            
        #             fairing.jettison = True

            # vessel.control.throttle = 0.30            
            
            # if not fairing.jettison:            
            #     fairing.jettison = True
             
            # print "... Fairing separation"
            # nave.fairing.jettison = True
            # time.sleep(3)                

            # fairing = True
            # vessel.control.throttle = 1            

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break        

    vessel.control.throttle = 1.0
    # Disable engines when target apoapsis is reached    
    while apoapsis() < target_altitude:
        pass
    print "SECO"
    vessel.control.throttle = 0.0

    # Plan circularization burn (using vis-viva equation)
    # time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    time.sleep(1)

    vessel.control.sas = False
    vessel.control.rcs = False

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    suborbital()

# Profile launch: Launch - Deploy probe - And.. next launch!
def atlas_x(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation, sepatron):            
    pitch_row = False
    maq1 = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True

    maq1_v = 410

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    ## first stage 
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    ## second stage
    stage_2 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')       

    # solid boosters
    stage_solid = vessel.resources_in_decouple_stage(stage=2, cumulative=True)
    solid_boosters = conn.add_stream(stage_solid.amount, 'SolidFuel')  

    if sound:
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_generic.wav")
        pygame.mixer.music.play()

    # call function for countdown - t10s
    countdown()
    # time.sleep(1)    

    print "... Ignition center engine!"

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False          
    vessel.control.throttle = 0.70

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    # time.sleep(5)    

    while True:   
        srb_tx = (srb_fuel_2() - srb_fuel_1())

        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.throttle = 1
                vessel.control.activate_next_stage()
                srbs_separated = True
                print "... Ignition solid's boosters!"
                print "LIFTOOF!"                       

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row" 
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        # if solid_boosters() <= 1 and not boosters_separation:
        if solid_boosters() <= sepatron and not boosters_separation:
            print "... Boosters Separation"
            vessel.control.activate_next_stage()
            boosters_separation = True
   
        if vessel.available_thrust == 0.0 and boosters_separation:
            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)            

            print "... Separation first stage"
            print "... Fairing separation"
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(3)                 

            print "SES-1"     
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"            
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO-1"
    vessel.control.rcs = True
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2"
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.50
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()
    print "SECO-2"

    # Resources
    vessel.control.sas = False
    vessel.control.rcs = False

    ## call function for show message
    orbit()

# Profile launch: Not recovery first stage
def atlas(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation):            
    pitch_row = False
    sound = True

    maq1 = False
    maq1_v = 410

    maxq = False

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')
    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    # srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # play sound t-10
    if sound:
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_generic.wav")
        pygame.mixer.music.play()

    # call function for countdown
    countdown()

    print "... IGNITION!"        
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1.0            

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
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                print "LIFTOOF!"                        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row" 
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if vessel.available_thrust == 0.0:                         
            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            print "... Separation first stage" 
            time.sleep(1)

            print "... Fairing separation" 
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(5)                    

            print "SES-1"     
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO-1"
    vessel.control.throttle = 0.0    

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.control.light = True
    vessel.control.rcs = True
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2"  
    vessel.control.throttle = 1.0            

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.10
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()

    # Resources
    vessel.control.sas = True
    vessel.control.rcs = False

    ## call function for show message
    orbit()

def landing_adv(alturaPouso, engines_landing, altitude_landing_burn, deploy_legs, profile, sound):               
    conn = krpc.connect(name='Suicide Burn')
    vessel = conn.space_center.active_vessel
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    situacao = conn.add_stream(getattr, vessel, 'situation')
    pousado_agua = conn.space_center.VesselSituation.splashed
    pousado = conn.space_center.VesselSituation.landed
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

    ksc = conn.space_center
    naveAtual = ksc.active_vessel

    secure_burn = False   
    reentry_engines_1 = False
    solar_panels = False

    def landing_main():                      
        global pouso
        pouso = False    
        reentry_burn = False
        landing_burn = False
        landing = False
        space = False
        atmosphere = False        
        reentry_engines = False        
        landing_legs = False   
        solar_panels = False

        cont_shut_engine = 0   

        ksc = conn.space_center
        foguete = ksc.active_vessel

        foguete.control.throttle = 0
        foguete.control.activate_next_stage()  # inicia zerando throttle e ligando motores   

        while pouso == False:
            # Variaveis
            ksc = conn.space_center
            foguete = ksc.active_vessel
            refer = foguete.orbit.body.reference_frame
            centroEspacial = conn.space_center
            naveAtual = ksc.active_vessel
            vooNave = foguete.flight(refer)
            pontoRef = foguete.orbit.body.reference_frame
            UT = conn.space_center.ut
            TWRMax = float()
            distanciaDaQueima = float()
            tempoDaQueima = float()
            acelMax = float()

            #####################
            # alturaPouso = 20.0
            # alturaPouso = 30.0    # ideal
            # alturaPouso = 35.0 
            # alturaPouso = 40.0
            # alturaPouso = 50.0  # funcionando
            #####################

            nave = conn.space_center.active_vessel

            speed = float(foguete.flight(refer).speed)
            altitudeNave = foguete.flight(refer).bedrock_altitude
            elevacaoTerreno = foguete.flight(refer).elevation
            massaTotalNave = foguete.mass
            velVertNave = foguete.flight(refer).vertical_speed
            velHorNave  = foguete.flight(refer).horizontal_speed

            piloto = foguete.auto_pilot
            refer = foguete.orbit.body.reference_frame
            vooNave = foguete.flight(refer)
            surAlt = foguete.flight(refer).surface_altitude
            elevacaoTerreno = foguete.flight(refer).elevation
            velVertNave = foguete.flight(refer).vertical_speed
            massa = foguete.mass
            empuxoMax = foguete.max_thrust                

            if surAlt > 70000 and not space:
                print "Wait for reentry..."
                space = True

            if surAlt < 70000 and not atmosphere:
                print "Reentry atmosphere..."    
                atmosphere = True
                       
            naveAtual.control.brakes = True
            forcaGravidade = foguete.orbit.body.surface_gravity
            TWRMax = empuxoMax / (massa * forcaGravidade)
            acelMax = (TWRMax * forcaGravidade) - forcaGravidade
            tempoDaQueima = speed / acelMax
            distanciaDaQueima = speed * tempoDaQueima + 1 / 2 * acelMax * pow(tempoDaQueima, 2)
            distanciaPouso = alturaPouso

            global ultCalculo
            ultCalculo = 0  # tempo do ultimo calculo
            global valorEntrada
            valorEntrada = float(surAlt)
            global valorSaida
            valorSaida = float()
            global valorLimite
            valorLimite = float(distanciaPouso + distanciaDaQueima)  # variáveis de valores

            global ultValorEntrada
            ultValorEntrada = float()  # variáveis de cálculo de erro

            global kp
            kp = float(.022)  # .023
            global ki
            ki = float(.001)  # .001
            global kd
            kd = float(1)  # 1

            global amostraTempo
            amostraTempo = 25 / 1000  # tempo de amostragem

            global saidaMin
            global saidaMax
            saidaMin = float(-1)
            saidaMax = float(1)  # limitar saída dos valores

            global agora
            global mudancaTempo
            agora = ksc.ut  # var busca tempo imediato
            mudancaTempo = agora - ultCalculo  # var compara tempo calculo

            global termoInt
            termoInt = float()

            def computarPID():            
                global ultCalculo
                global ultValorEntrada
                global valorSaida
                global termoInt

                # reentry_engines = False
                # cont_shut_engine = 0  

                agora = ksc.ut  # var busca tempo imediato
                mudancaTempo = agora - ultCalculo  # var compara tempo calculo

                if mudancaTempo >= amostraTempo:  # se a mudança for > q o tempo de amostra, o calculo é feito
                    # var calculo valor saida
                    erro = valorLimite - valorEntrada
                    termoInt += ki * erro
                    if termoInt > saidaMax:
                        termoInt = saidaMax
                    elif termoInt < saidaMax:
                        termoInt = saidaMin
                    dvalorEntrada = (valorEntrada - ultValorEntrada)
                    # computando valor saida
                    valorSaida = kp * erro + ki * termoInt - kd * dvalorEntrada
                    if valorSaida > saidaMax:
                        valorSaida = saidaMax
                    elif valorSaida < saidaMin:
                        valorSaida = saidaMin

                    # relembra valores atuais pra prox

                    ultValorEntrada = valorEntrada
                    ultCalculo = agora

                if termoInt > saidaMax:
                    termoInt = saidaMax
                elif termoInt < saidaMin:
                    termoInt = saidaMin
                if valorSaida > saidaMax:
                    valorSaida = saidaMax
                elif valorSaida < saidaMin:
                    valorSaida = saidaMin

                return (valorSaida)

            # Imprimir informacoes
            print "TWR           : %f" % TWRMax
            print "Dist. Queima  : %f" % distanciaDaQueima
            print "Altitude Voo  : %d" % surAlt
            print "Elev. Terreno : %d" % elevacaoTerreno
            print "*Velocidade Ver: %d" % velVertNave
            print "*Velocidade Hor: %d" % velHorNave
            print "Correcao      : %f" % computarPID()  # esse valor que nao esta atualizando, e deveria atualizar

            # return (TWRMax)
            # return (distanciaDaQueima)
            # return (surAlt)
            # return (elevacaoTerreno)
            # return (computarPID())

            novaAcel = 1 / TWRMax + computarPID()  # calculo de aceleracao

            #######################################################################            
            if velHorNave >= 10 and velVertNave < 0 and novaAcel < 1:
                vessel.control.sas = True
                vessel.control.rcs = True

                if velVertNave < 0:                                  
                    vessel.control.sas_mode = vessel.control.sas_mode.retrograde
            #######################################################################

            # begin_dogleg = 60000
            # end_dogleg   =  5000            

            # if surAlt <= begin_dogleg and surAlt >= end_dogleg:
            #     vessel.control.sas = True
            #     vessel.control.rcs = True

            #     # piloto.engage()
            #     # piloto.target_pitch_and_heading(-40, 90)

            #     vessel.control.sas_mode = vessel.control.sas_mode.radial   

            #     # dogleg = True
            # else:
            #     if velHorNave >= 10 and velVertNave < 0 and novaAcel < 1:
            #         vessel.control.sas = True
            #         vessel.control.rcs = True

            #         if velVertNave < 0:                                  
            #             vessel.control.sas_mode = vessel.control.sas_mode.retrograde                
            #         elif velVertNave >= 0:
            #             vessel.control.sas_mode = vessel.control.sas_mode.radial   

            # return (novaAcel)

            print "Acc Calculada : %f" % novaAcel
            print "                  "

            # text.content = 'Correcao: %f' % computarPID()  # mostra calculo na tela do jogo

            if surAlt <= 36000 and not reentry_burn and naveAtual.control.throttle != 0 and profile=="Falkinho":
                print "Reentry burn..."
                reentry_burn = True

                if sound and profile=="Falkinho":
                    # play sound
                    pygame.init()
                    pygame.mixer.music.load("../audio/reentryburn_falcon9.wav")
                    pygame.mixer.music.play()                

            if surAlt <= altitude_landing_burn and not reentry_engines:
                print "Landing burn..."
                landing_burn = True

                for engines in vessel.parts.engines:            
                    if not reentry_engines:
                        print "... Shutdown engines" 
                        reentry_engines = True  

                    cont_shut_engine = cont_shut_engine + 1                         

                    if engines.active and cont_shut_engine > engines_landing:            
                        engines.active = False

                if sound and profile=="Falkinho" and reentry_burn and reentry_engines:
                    pygame.init()
                    pygame.mixer.music.load("../audio/landing_falcon9.wav")
                    # pygame.mixer.music.load("../audio/others/landingboosters_falconh.wav")
                    pygame.mixer.music.play()                                                                                      

            # landing legs
            # if distanciaDaQueima <= deploy_legs and not landing_legs and reentry_engines:
            if distanciaDaQueima <= deploy_legs and not landing_legs:               #VERIFICAR ISSO!
                naveAtual.control.gear = True 
                landing_legs = True

            # if surAlt > 200:                                                        #NECESSARIO?
            #     naveAtual.control.gear = False
            if situacao() == pousado or situacao() == pousado_agua:
                naveAtual.control.throttle = 0
                pouso = True

            elif speed <= 6:
                naveAtual.control.throttle = .1            
            else:
                naveAtual.control.throttle = novaAcel
            if speed <= 1:
                naveAtual.control.throttle = 0                    

    if situacao() != pousado or situacao() != pousado_agua :
        landing_main()
    else:        
        print "ok"        

    if profile=="Falkinho" or profile=="New Shepard" or profile=="New Gleen":
        for painelsolar in vessel.parts.solar_panels:        
            if not solar_panels:
                print "... Deploy solar painels" 
                solar_panels = True  

            if painelsolar.deployable:            
                painelsolar.deployed = True 

    ## disabled all    
    naveAtual.control.throttle = 0
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.brakes = False    

    if profile=="Falkinho" or profile=="New Shepard" or profile=="New Gleen":
        for engines in vessel.parts.engines:            
            if not reentry_engines_1:
                print "... Shutdown engines" 
                reentry_engines_1 = True  

            if engines.active:            
                engines.active = False    

    time.sleep(10)
    
    print("LANDING!")

def hooper(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation):        
    pitch_row = False
    maxq = False
    maq1 = False
    maq1_v = 410
    meco = False
    solar_panels = False

    sound = False

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    ## first stage 
    stage_1 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    srb_tx = (srb_fuel_1())*taxa 

    # print srb_fuel()
    # print srb_fuel_1()
    # print srb_fuel_2()
    # print srb_tx

    if srb_tx == 0:
        print "HOLD HOLD HOLD"
        print "[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!"
        time.sleep(60)

    # if sound:
    #     # play sound t-10    
    #     pygame.init()
    #     pygame.mixer.music.load("../audio/liftoff_falcon9.wav")
    #     pygame.mixer.music.play()

    # call function for countdown
    # countdown()

    print "... IGNITION!"
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 0.75
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:          
        # Gravity turn
        if altitude() >= turn_start_altitude and altitude() <= turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))       

            if not meco:
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.1:
                    turn_angle = new_turn_angle
                    vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                vessel.control.throttle = 1.0
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True

        if altitude() >= maxq_begin and not maxq:            
            # if sound:
            #     # play sound
            #     pygame.init()
            #     pygame.mixer.music.load("../audio/maxq_falcon9.wav")
            #     pygame.mixer.music.play()                        

            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_1() <= srb_tx:    
            # if sound:
            #     # play sound
            #     pygame.init()
            #     pygame.mixer.music.load("../audio/meco_falcon9.wav")
            #     pygame.mixer.music.play()
            #     meco = True

            if meco:
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.01:                
                    turn_angle = new_turn_angle
                    vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

            print "MECO"
            vessel.control.throttle = 0.0

            print "... Separation first stage"
            print "... Fairing separation"
            time.sleep(3)                    

            vessel.control.activate_next_stage()    
            vessel.control.throttle = 0.50            
            time.sleep(1)                    
    
            print "SES"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO"
    vessel.control.throttle = 0.0

    # Plan circularization burn (using vis-viva equation)
    # time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    time.sleep(1)

    vessel.control.sas = False
    vessel.control.rcs = False

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    suborbital()

# Profile launch: Launch - Deploy probe - And.. next launch!
def titan_x(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation, sepatron):            
    pitch_row = False
    maq1 = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True

    maq1_v = 410

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    ## first stage 
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    ## second stage
    stage_2 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')       

    # solid boosters
    stage_solid = vessel.resources_in_decouple_stage(stage=2, cumulative=True)
    solid_boosters = conn.add_stream(stage_solid.amount, 'SolidFuel')  

    if sound:
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_generic.wav")
        pygame.mixer.music.play()

    # call function for countdown - t10s
    countdown()
    # time.sleep(1)    

    print "... Ignition center engine!"

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False          
    vessel.control.throttle = 0.70

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    # time.sleep(5)    

    while True:   
        srb_tx = (srb_fuel_2() - srb_fuel_1())

        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation)        

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.throttle = 1
                vessel.control.activate_next_stage()
                srbs_separated = True
                print "... Ignition solid's boosters!"
                print "LIFTOOF!"                       

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row" 
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        # if solid_boosters() <= 1 and not boosters_separation:
        if solid_boosters() <= sepatron and not boosters_separation:
            print "... Boosters Separation"
            vessel.control.activate_next_stage()
            boosters_separation = True
   
        if vessel.available_thrust == 0.0 and boosters_separation:
            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)            

            print "... Separation first stage"
            print "... Fairing separation"
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(3)                 

            print "SES-1"     
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"            
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO-1"
    vessel.control.rcs = True
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2"
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.50
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()
    print "SECO-2"

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    # Resources
    vessel.control.sas = False
    vessel.control.rcs = False

    ## call function for show message
    orbit()

def titan(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, orientation, profile, sound, correction_time): 
    pitch_row = False
    maxq = False
    maq1 = False
    beco = False
    maq1_v = 410
    boosters_separation = False

    # sound = True

    conn = krpc.connect(name=profile)
    vessel = conn.space_center.active_vessel
    ksc = conn.space_center    
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame

    # Set up streams for telemetry
    # general
    ut = conn.add_stream(getattr, conn.space_center, 'ut')
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')
    
    # second stage
    stage_1 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

    # side boosters
    stage_2 = vessel.resources_in_decouple_stage(stage=4, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')   

    # core central
    stage_3 = vessel.resources_in_decouple_stage(stage=3, cumulative=False)
    srb_fuel_3 = conn.add_stream(stage_3.amount, 'LiquidFuel')

    # srb_tx = ((srb_fuel_2() - srb_fuel_1()) - srb_fuel_3())
    # srb_tx = (srb_fuel_2() - srb_fuel_3() - srb_fuel_1())

    # # check if landing
    # if taxa > 0:
    #     landing_boolean = "Yes"
    # else:
    #     landing_boolean = "No"    

    # print "... Start launch in: " + profile
    # print "... Mass rocket: ??"
    # print "... Mass payload: ??"
    # print "... Altitude target ??"
    # print "... Landing first stage: " + landing_boolean

    # print srb_tx
    # print srb_fuel_1()
    # print srb_fuel_2()
    # print srb_fuel_3()

    # time.sleep(10)

    if sound:
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_generic.wav")
        pygame.mixer.music.play()

        countdown()
 
    print "... Ignition central core!"   
    # Activate the first stage    
    vessel.control.activate_next_stage()
    vessel.control.throttle = 0.50
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # time.sleep(1)

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1.0    
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:          
        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.1:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:                
                vessel.control.activate_next_stage()
                vessel.control.throttle = 1.00
                srbs_separated = True
                print "... Ignition side boosters!"
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and not maxq:                                   
            print "... Max-Q"
            maxq = True        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        
                
        if srb_fuel_2() <= 0 and not boosters_separation:
            print "... Separation side boosters"
            vessel.control.activate_next_stage()            
            boosters_separation = True
          
        if srb_fuel_3() <= 0 and boosters_separation:
            print "MECO"
            vessel.control.throttle = 0.50            
            vessel.control.activate_next_stage()            
            time.sleep(2)                    
            vessel.control.throttle = 1            
 
            print "SES-1"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO-1"
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    # Orientate ship
    print "... Orientating ship for circularization burn"
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.control.rcs = True
    vessel.auto_pilot.wait()

    # Wait until burn
    print "... Waiting until circularization burn"
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print "... Ready to execute burn"
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print "SES-2" 
    print "... Circularization burn"
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.50
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()
    print "SECO-2"

    # time.sleep(1)

    vessel.control.sas = False
    vessel.control.rcs = False

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    orbit()

# Profile launch: Suborbital insertion and landing attemp in the KSC or VAB.... \o
def falcao_landing_zone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_row = False
    maxq = False
    maq1 = False
    maq1_v = 410
    meco = False
    solar_panels = False

    # sound = True

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
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # print srb_tx()

    # time.sleep(3)

    if srb_tx == 0:
        print "HOLD HOLD HOLD"
        print "[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!"
        time.sleep(60)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_falcon9.wav")
        pygame.mixer.music.play()
        countdown()

    print "... IGNITION!"
    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 0.85
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:          
        # Gravity turn
        if not meco:
            if altitude() >= turn_start_altitude and altitude() <= turn_end_altitude:
                frac = ((altitude() - turn_start_altitude) /
                        (turn_end_altitude - turn_start_altitude))
                
                new_turn_angle = frac * 90
                if abs(new_turn_angle - turn_angle) > 0.5:
                    turn_angle = new_turn_angle
                    vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                vessel.control.throttle = 1.0
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "... Heading/Pitch/Row"
            pitch_row = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_falcon9.wav")
                pygame.mixer.music.play()                        

            print "... Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print "... Supersonic"
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_2() <= srb_tx:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_falcon9.wav")
                pygame.mixer.music.play()
                meco = True

            if meco:
                if altitude() >= turn_start_altitude and altitude() <= 90000:
                    frac = ((altitude() - turn_start_altitude) /
                            (turn_end_altitude - turn_start_altitude))       
                    
                    new_turn_angle = frac * 90
                    if abs(new_turn_angle - turn_angle) > 0.01:
                        turn_angle = new_turn_angle
                        vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

            print "MECO"
            vessel.control.throttle = 0.0

            print "... Separation first stage"
            # print "... Fairing separation"
            time.sleep(3)                    

            vessel.control.activate_next_stage()    
            vessel.control.throttle = 0.50            
            time.sleep(3)                    
    
            print "SES"      
            print "... Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "SECO"
    vessel.control.throttle = 0.0

    # Plan circularization burn (using vis-viva equation)
    # time.sleep(5)
    print "... Planning circularization burn"
    mu = vessel.orbit.body.gravitational_parameter
    r = vessel.orbit.apoapsis
    a1 = vessel.orbit.semi_major_axis
    a2 = r
    v1 = math.sqrt(mu*((2./r)-(1./a1)))
    v2 = math.sqrt(mu*((2./r)-(1./a2)))
    delta_v = v2 - v1
    node = vessel.control.add_node(
        ut() + vessel.orbit.time_to_apoapsis, prograde=delta_v)

    # Calculate burn time (using rocket equation)
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0 / math.exp(delta_v/Isp)
    flow_rate = F / Isp
    burn_time = (m0 - m1) / flow_rate    

    time.sleep(1)

    vessel.control.sas = False
    vessel.control.rcs = False

    for painelsolar in nave.parts.solar_panels:        
        if not solar_panels:
            print "... Deploy solar painels"
            solar_panels = True  

        if painelsolar.deployable:            
            painelsolar.deployed = True

    ## call function for show message
    suborbital()

#####################################
## via interface - only test for now
def sub_orbital():
    print "Suborbital"

def orbital_maneuver():
    print "Orbital Maneuver"

def landing_test():
    print "Landing"
#####################################

################################# END ESPECIFIC FUNCTIONS #################################