#!/usr/bin/env python
# -*- coding: utf-8 -*-

## import library's
import os, sys, math, time, krpc, pygame

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

################################# GENERIC FUNCTIONS #################################
## Generic countdown - T-10s
def countdown():
    sequence = [ "|---      ALL SYSTEMS NOMINAL FOR LAUNCH      ---|",
                "Director flight...",
                "Internal power...",
                "Computer flight...",
                "Temperatures...",                                                             
                "Gimbal rocket...",                 
                "Navigation system...",
                "Ground control...",                  
                "Ready for launch!",      
                "GO GO GO!!!" ]

    x = 1    
    for x in range(len(sequence)):           
        if x == 0:            
            print sequence[x]
        else:
            print "...", sequence[x]
        time.sleep(1)

    time.sleep(1)

## gereric error
def warning_error():
    print "|---       HOLD HOLD HOLD          ---|"
    print "|---       CHECK YOUR PROBE        ---|"
    print "|-NOT POSSIBLE CALCULATE LANDING FUEL-|"
    pygame.init()
    pygame.mixer.music.load("../audio/error.wav")
    pygame.mixer.music.play()
    time.sleep(60)

### Generic message - Orbital
def orbit():
    print "|---       ORBITAL INSERTION COMPLETE         ---|"    

### Generic message - SubOrbital
def suborbital():
    print "|---      SUB-ORBITAL INSERTION COMPLETE      ---|"    

################################# END GENERIC FUNCTIONS #################################
#
#
################################# BEGIN ESPECIFIC FUNCTIONS #################################
#
# Profile launch: Suborbital insertion for landing attempt in the KSC or VAB.... \o
def falkinho(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_roll = False
    maxq = False
    maxq_begin_key = False
    maxq_end_key = False
    supersonic = False    
    supersonic_v = 320    

    meco = False
    solar_panels = False
    fairing = False

    conn = krpc.connect(name='Falkinho')
    vessel = conn.space_center.active_vessel
    ksc = conn.space_center    
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame

    ## atmosphere
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    atmosphere = True

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
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    # first stage
    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    # calc remaing fuel
    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # error detected
    if srb_tx == 0 and taxa > 0:
        warning_error()

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_falcon9.wav")
        pygame.mixer.music.play()
        countdown()

    print "... IGNITION!"
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
        ## atmosphere check
        if surAlt >= 70000 and atmosphere:
            atmosphere = False        

        # Gravity turn
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
        
        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True

        if velocidade() >= supersonic_v and not supersonic and pitch_roll:
            print "... Supersonic"
            supersonic = True

        if not maxq_begin_key and altitude() >= maxq_begin and not maxq:
            vessel.control.throttle = 0.50     
            print "... Throttle down"
            maxq_begin_key = True
        elif maxq_begin_key and altitude() >= maxq_end and not maxq_end_key and maxq:
            vessel.control.throttle = 1.0                    
            print "... Throttle up"
            maxq_end_key = True    

        maxq_md = ( maxq_begin + maxq_end ) / 2

        if altitude() >= maxq_md and not maxq and maxq_begin_key:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_falcon9.wav")
                pygame.mixer.music.play()                        

            print "MAX-Q"
            maxq = True        

        if srb_fuel_2() <= srb_tx and maxq_end_key:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_falcon9.wav")
                pygame.mixer.music.play()
                meco = True

            print "MECO"
            print "... Separation first stage"
            print "... Fairing Separation"
            vessel.control.throttle = 0.0
            time.sleep(2)                 
            meco = True            

            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(1)                                   

        if meco:                        
            vessel.auto_pilot.target_pitch_and_heading(0, orientation) 

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
            

            if surAlt <= 800 and not landing_burn and naveAtual.control.throttle != 0:
                print "Landing burn..."
                landing_burn = True

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
    pitch_roll = False
    supersonic = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True

    supersonic_v = 320

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

        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll" 
            pitch_roll = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

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

    ## call function for show message
    orbit()

# Profile launch: Launch - Suborbital insertion - Landing first stage..
def newshepard(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_roll = False
    maxq = False
    maxq_begin_key = False
    maxq_end_key = False
    supersonic = False    
    supersonic_v = 320    

    meco = False
    solar_panels = False
    fairing = False

    conn = krpc.connect(name='New Glenn')
    vessel = conn.space_center.active_vessel
    ksc = conn.space_center    
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame

    ## atmosphere
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    atmosphere = True

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
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    # first stage
    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    # calc remaing fuel
    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # error detected
    if srb_tx == 0 and taxa > 0:
        warning_error()

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_newshepard.wav")
        pygame.mixer.music.play()
        countdown()

    print "... IGNITION!"
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 0.95
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:                
        ## atmosphere check
        if surAlt >= 70000 and atmosphere:
            atmosphere = False        

        # Gravity turn
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
        
        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True

        if velocidade() >= supersonic_v and not supersonic and pitch_roll:
            print "... Supersonic"
            supersonic = True

        if not maxq_begin_key and altitude() >= maxq_begin and not maxq:
            vessel.control.throttle = 0.50     
            print "... Throttle down"
            maxq_begin_key = True
        elif maxq_begin_key and altitude() >= maxq_end and not maxq_end_key and maxq:
            vessel.control.throttle = 1.0                    
            print "... Throttle up"
            maxq_end_key = True    

        maxq_md = ( maxq_begin + maxq_end ) / 2

        if altitude() >= maxq_md and not maxq and maxq_begin_key:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_newshepard.wav")
                pygame.mixer.music.play()                        

            print "MAX-Q"
            maxq = True        

        if srb_fuel_2() <= srb_tx and maxq_end_key:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_newshepard.wav")
                pygame.mixer.music.play()
                meco = True

            print "MECO"
            print "... Separation first stage"
            vessel.control.throttle = 0.0
            time.sleep(2)                 
            meco = True            

            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()                                              

        if meco:                        
            vessel.auto_pilot.target_pitch_and_heading(0, orientation) 

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

# Profile launch: Suborbital insertion and landing attemp in the KSC or VAB.... \o
def newshepard_landingzone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_roll = False
    maxq = False
    supersonic = False
    supersonic_v = 320
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
        
        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_newshepard.wav")
                pygame.mixer.music.play()                        

            print "... Max-Q"
            maxq = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

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
    pitch_roll = False
    supersonic = False    
    boosters_separation = False
    maxq = False

    supersonic_v = 320

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

        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            vessel.control.rcs = True
            maxq = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

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

## core + side boosters
def falkinho_triplo(turn_start_altitude,target_altitude, maxq_begin, maxq_end, taxa_central, taxa_side, orientation, sound):
    pitch_roll = False
    maxq = False
    maxq_begin_key = False
    maxq_end_key = False
    supersonic = False
    supersonic_v = 320
    meco = False
    beco = False
    solar_panels = False    
    fairing_sep = False

    conn = krpc.connect(name='Falkinho Triplo')
    vessel = conn.space_center.active_vessel
    ksc = conn.space_center    
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame

    ## atmosphere
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    atmosphere = False

    # Set up streams for telemetry
    # general
    ut = conn.add_stream(getattr, conn.space_center, 'ut')
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources solid
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    # second stage
    second_stage = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    second_stage_fuel = conn.add_stream(second_stage.amount, 'LiquidFuel')

    # first stage
    first_stage = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    first_stage_fuel = conn.add_stream(first_stage.amount, 'LiquidFuel')     

    # core central
    stage_2 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    central_fuel = conn.add_stream(stage_2.amount, 'LiquidFuel')

    # side boosters
    stage_3 = vessel.resources_in_decouple_stage(stage=4, cumulative=True)
    boosters_fuel = conn.add_stream(stage_3.amount, 'LiquidFuel')    

    # # calc ((first stage(3) - second ) * taxa fuel)
    central_fuel_tx  = ((central_fuel() - second_stage_fuel())  * taxa_central)
    boosters_fuel_tx = ((boosters_fuel() - second_stage_fuel()) * taxa_side)

    # check tx fuel
    if boosters_fuel_tx <= 0 or central_fuel_tx <= 0:
        warning_error()

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_falcon9.wav")
        pygame.mixer.music.play()
        countdown()

    print "... IGNITION!"
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()  
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1

    # max-thrust side boosters
    time.sleep(0.25) 
    
    # Main ascent loop
    srbs_separated = False
    turn_angle = 0

    while True:          
        ## atmosphere check
        if surAlt >= 70000 and not atmosphere:
            atmosphere = True

        turn_end_altitude = (target_altitude/1.5)

        if altitude() >= turn_start_altitude and altitude() <= turn_end_altitude:                    
            frac = ((altitude() - turn_start_altitude) /
            (turn_end_altitude - turn_start_altitude))                   

            new_turn_angle = frac * 90            
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90-turn_angle, orientation) 

        # Separate SRBs when finished
        if not srbs_separated:
            # solid fuel for ejection side boosters
            if srb_fuel() <= 10:
                vessel.control.activate_next_stage()
                srbs_separated = True
                vessel.control.throttle = 1.0
                print "LIFTOOF!"
        
        ## starting manauvers rocket
        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True

        if velocidade() >= supersonic_v and not supersonic and pitch_roll:
            print "... Supersonic"
            supersonic = True    

        # calc middle maxq
        maxq_md = ( maxq_begin + maxq_end ) / 2

        # maximium dynamic pressure
        if altitude() >= maxq_md and not maxq and maxq_begin_key:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_falcon9.wav")
                pygame.mixer.music.play()                        

            print "MAX-Q"
            maxq = True        

        # throttle down for input in maxq
        if not maxq_begin_key and altitude() >= maxq_begin and not maxq:
            vessel.control.throttle = 0.50     
            print "... Throttle down"
            maxq_begin_key = True
        # throttle up for output in maxq
        elif maxq_begin_key and altitude() >= maxq_end and not maxq_end_key and maxq:
            vessel.control.throttle = 1.0                    
            print "... Throttle up"
            maxq_end_key = True  

        ## beco - boosters engines cut off
        if first_stage_fuel() <= boosters_fuel_tx and not beco and maxq_end_key:
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/beco_falconh.wav")
                pygame.mixer.music.play()

            print "BECO"
            print "... Boosters separation"
            vessel.control.throttle = 0
            time.sleep(2)  

            vessel.control.activate_next_stage()    
            vessel.control.throttle = 1
            beco = True           
            time.sleep(3)      

        if beco and not meco:
            vessel.auto_pilot.target_pitch_and_heading(0, orientation)        
            vessel.control.rcs = True 
        else:
            vessel.control.rcs = False

        ## fairing separation
        if not atmosphere and beco and not fairing_sep:
            print "... Fairing separation"
            vessel.control.activate_next_stage()                    
            fairing_sep = True

        ## meco - main engin cut off
        if first_stage_fuel() <= central_fuel_tx and beco and not meco:
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_falcon9.wav")
                pygame.mixer.music.play()
                
            print "MECO"
            print "... Central core separation"
            vessel.control.throttle = 0.0
            time.sleep(1)
            meco = True            
            time.sleep(2)
            vessel.control.throttle = 0.5
    
        ## ses - second engine started
        if meco and beco:
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
def lce(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation):            
    pitch_roll = False
    supersonic = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True

    supersonic_v = 320

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

        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

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
def neutron(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation, sound):            
    pitch_roll = False
    supersonic = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    antena = False

    supersonic_v = 320

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
        # call function for countdown - t10s
        countdown()
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_generic.wav")
        pygame.mixer.music.play()    

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

        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll" 
            pitch_roll = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True
   
        if vessel.available_thrust == 0.0:
            print "MECO"
            vessel.control.throttle = 0.0   

            print "... Separation first stage"
            print "... Fairing separation"            
            vessel.control.activate_next_stage()            
            vessel.control.throttle = 0.30            
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
    vessel.control.throttle = 0.25
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    vessel.control.throttle = 0.0
    node.remove()
    print "SECO-2"

    # time.sleep(2)    
    # print "... Deploy Satellites"    
    # vessel.control.activate_next_stage()                    

    # Resources
    vessel.control.sas = False
    vessel.control.rcs = False

    ## call function for show message
    orbit()

# Profile launch: Launch - Deploy payload.. and.. next launch!
def velorg(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation, sound):            
    pitch_roll = False
    supersonic = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    # sound = False

    supersonic_v = 320

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

    if sound:
        countdown()
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_generic.wav")
        pygame.mixer.music.play()

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, orientation)    

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = True          
    vessel.control.throttle = 0.30 

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
            # if srb_fuel() < 0.1:
                vessel.control.throttle = 1
                # vessel.control.activate_next_stage()
                srbs_separated = True
                print "LIFTOOF!"                       

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll" 
            pitch_roll = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

        if solid_boosters() <= 0 and not boosters_separation:
            # print "... Separation first stage"
            print "... Separation solid booster"
            time.sleep(1)
            print "MES-1"
            vessel.control.activate_next_stage()
            boosters_separation = True
   
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

    # Wait until out of atmosphere
    print "... Coasting out of atmosphere"
    while altitude() < 70500:
        pass

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
    
    # Fairing separation
    vessel.control.activate_next_stage()
    print "... Fairing Separation"     

    print "MES-2"
    print "... Orbital burn manuveur"
    vessel.control.throttle = 1

    # CHECK #
    time.sleep(burn_time - 0.1)
    print "... Fine tuning"
    vessel.control.throttle = 0.25
    remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame)

    ## manuveur correction
    while remaining_burn()[1] > correction_time:
        pass
    
    vessel.control.throttle = 0.0
    node.remove()
    print "MECO-2"

    # Resources
    vessel.control.sas = True
    vessel.control.rcs = False

    ## call function for show message
    orbit()

# Profile launch: Suborbital insertion for landing attempt in the KSC or VAB.... \o
def newglenn(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_roll = False
    maxq = False
    maxq_begin_key = False
    maxq_end_key = False
    supersonic = False    
    supersonic_v = 320    

    meco = False
    solar_panels = False
    fairing = False

    conn = krpc.connect(name='New Glenn')
    vessel = conn.space_center.active_vessel
    ksc = conn.space_center    
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame

    ## atmosphere
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    atmosphere = True

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
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    # first stage
    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    # calc remaing fuel
    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # error detected
    if srb_tx == 0 and taxa > 0:
        warning_error()

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_newshepard.wav")
        pygame.mixer.music.play()
        countdown()

    print "... IGNITION!"
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
        ## atmosphere check
        if surAlt >= 70000 and atmosphere:
            atmosphere = False        

        # Gravity turn
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
        
        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True

        if velocidade() >= supersonic_v and not supersonic and pitch_roll:
            print "... Supersonic"
            supersonic = True

        if not maxq_begin_key and altitude() >= maxq_begin and not maxq:
            vessel.control.throttle = 0.50     
            print "... Throttle down"
            maxq_begin_key = True
        elif maxq_begin_key and altitude() >= maxq_end and not maxq_end_key and maxq:
            vessel.control.throttle = 1.0                    
            print "... Throttle up"
            maxq_end_key = True    

        maxq_md = ( maxq_begin + maxq_end ) / 2

        if altitude() >= maxq_md and not maxq and maxq_begin_key:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_newshepard.wav")
                pygame.mixer.music.play()                        

            print "MAX-Q"
            maxq = True        

        if srb_fuel_2() <= srb_tx and maxq_end_key:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_newshepard.wav")
                pygame.mixer.music.play()
                meco = True

            print "MECO"
            print "... Separation first stage"
            print "... Fairing Separation"
            vessel.control.throttle = 0.0
            time.sleep(2)                 
            meco = True            

            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(1)                                   

        if meco:                        
            vessel.auto_pilot.target_pitch_and_heading(0, orientation) 

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

# Profile launch: Launch - Deploy probe - And.. next launch - MOAR BOOSTERS!
def atlas_x(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation, sepatron):            
    pitch_roll = False
    supersonic = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True

    supersonic_v = 320

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

        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll" 
            pitch_roll = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

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

# Profile launch: Launch - Deploy probe - And.. next launch!
def atlas(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation, sound):            
    pitch_roll = False
    # sound = True

    supersonic = False
    supersonic_v = 320

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
        countdown()
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_generic.wav")
        pygame.mixer.music.play()

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

        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll" 
            pitch_roll = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

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

# function landing_advanced improviment
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
                       
            if atmosphere:                
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

            ## FUNCIONANDO
            # Imprimir informacoes
            print "TWR           : %f" % TWRMax
            print "Dist. Queima  : %f" % distanciaDaQueima
            print "Altitude Voo  : %d" % surAlt
            print "Elev. Terreno : %d" % elevacaoTerreno
            print "*Velocidade Ver: %d" % velVertNave
            print "*Velocidade Hor: %d" % velHorNave
            print "Correcao      : %f" % computarPID()  # esse valor que nao esta atualizando, e deveria atualizar            

            ## TESTANDO
            # return TWRMax
            # return distanciaDaQueima
            # return surAlt
            # return elevacaoTerreno
            # return computarPID()

            novaAcel = 1 / TWRMax + computarPID()  # calculo de aceleracao

            # return novaAcel

            print "Acc Calculada : %f" % novaAcel
            print "                  "

            # busca alvo
            target_vessel = conn.space_center.target_vessel

            ## WORKING
            #######################################################################            
            # if velHorNave >= 10 and velVertNave < 0 and novaAcel < 1:
            if velHorNave >= 1 and velVertNave < 1 and novaAcel < 1:
                vessel.control.sas = True
                vessel.control.rcs = True
                
                # encontrou alvo
                if target_vessel and surAlt >= altitude_landing_burn and distanciaDaQueima >= 2000:
                    ## target location - tentar usar isso para o pouso                    
                    target_vessel_lon = conn.space_center.target_vessel.flight(refer).longitude
                    target_vessel_lat = conn.space_center.target_vessel.flight(refer).latitude

                    vessel.control.sas_mode = vessel.control.sas_mode.anti_target
                # nao encontrou o alvo - the beast landing
                elif not target_vessel and profile=="Falcao" or profile=="Falkinho Triplo" or profile=="New Glenn" or surAlt <= 200:                                        
                    if surAlt <= altitude_landing_burn:
                        vessel.control.sas_mode = vessel.control.sas_mode.radial
                # qualquer outra coisa
                else:
                    vessel.control.sas_mode = vessel.control.sas_mode.retrograde
                # qualquer outra coisa    
                # else:
                #     vessel.control.sas_mode = vessel.control.sas_mode.radial
            #######################################################################

            ## DOGLEG
            #######################################################################
            # begin_dogleg = 1500000
            # end_dogleg   =  5000     
            # dogleg       = False       

            # vessel.control.rcs = True            
            # vessel.control.sas = False

            # if surAlt <= begin_dogleg and surAlt >= end_dogleg and not dogleg:                
            #     vessel.control.sas = False

            #     piloto.engage()
            #     piloto.target_pitch_and_heading(-90, 90)

            #     dogleg = True
            #     vessel.control.sas_mode = vessel.control.sas_mode.radial
            # elif velHorNave >= 3 and dogleg:
            #     vessel.control.sas = True
            #     vessel.control.sas_mode = vessel.control.sas_mode.retrograde                
            # else:
            #     vessel.control.sas = True
            #     vessel.control.sas_mode = vessel.control.sas_mode.radial                
            #######################################################################

            ## reentry burn
            if surAlt <= 36000 and not reentry_burn and not reentry_engines and naveAtual.control.throttle != 0:
                print "Reentry burn..."
                reentry_burn = True

                if sound and reentry_burn and profile=="Falkinho" or profile=="Falkinho Triplo" or profile=="Falcao":
                    # play sound
                    pygame.init()
                    pygame.mixer.music.load("../audio/reentryburn_falcon9.wav")
                    pygame.mixer.music.play()                

            ## shutdown 'n' engines
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

                ## landing burn
                if sound and reentry_engines and profile=="Falkinho" or profile=="Falkinho Triplo" or profile=="Falcao":                    
                    pygame.init()
                    pygame.mixer.music.load("../audio/landing_falcon9.wav")
                    pygame.mixer.music.play()                                                                                      

            # landing legs
            if distanciaDaQueima <= deploy_legs and not landing_legs:               
                naveAtual.control.gear = True 
                landing_legs = True

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

    # if profile=="Falkinho" or profile=="New Shepard" or profile=="New Glenn":
    #     for painelsolar in vessel.parts.solar_panels:        
    #         if not solar_panels:
    #             print "... Deploy solar painels" 
    #             solar_panels = True  

    #         if painelsolar.deployable:            
    #             painelsolar.deployed = True 

    ## disabled all    
    naveAtual.control.throttle = 0
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.brakes = False    

    ## engines off
    if profile=="Falkinho" or profile=="New Shepard" or profile=="New Glenn":
        for engines in vessel.parts.engines:            
            if not reentry_engines_1 and pouso:
                print "... Shutdown engines" 
                reentry_engines_1 = True  
                
            if engines.active:
                engines.active = False    

    time.sleep(3)
    
    if pouso:       
        print("LANDING!")

# Profile launch: Launch - Deploy probe - And.. next launch - MOAR BOOSTERS!
def titan_x(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation, sepatron):            
    pitch_roll = False
    supersonic = False    
    boosters_separation = False
    maxq = False
    solar_panels = False
    sound = True

    supersonic_v = 320

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

    ## second stage
    stage_2 = vessel.resources_in_decouple_stage(stage=1, cumulative=False)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')       

    ## first stage 
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')

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

        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll" 
            pitch_roll = True        

        if altitude() >= maxq_begin and not maxq:            
            print "... Max-Q"
            maxq = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

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

# Profile launch: Launch - Deploy probe - And.. next launch!
def titan(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, orientation, profile, sound, correction_time): 
    pitch_roll = False
    maxq = False
    supersonic = False
    beco = False
    supersonic_v = 320
    boosters_separation = False

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
        
        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

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

# landing the beast
def falcao_landing_zone(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_roll = False
    maxq = False
    maxq_begin_key = False
    maxq_end_key = False
    supersonic = False    
    supersonic_v = 320
    meco = False
    solar_panels = False

    conn = krpc.connect(name='Falkinho')
    vessel = conn.space_center.active_vessel
    ksc = conn.space_center    
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame

    ## atmosphere
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    atmosphere = False

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
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    # first stage
    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    # print srb_fuel_1()
    # print srb_fuel_2()

    # target_vessel
    
    # calc tx
    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    if srb_tx == 0:
        warning_error()

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_falcon9.wav")
        pygame.mixer.music.play()
        countdown()

    print "... IGNITION!"
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
        ## atmosphere check
        if surAlt >= 70000 and not atmosphere:
            atmosphere = True

        # Gravity turn
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
        
        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

        if not maxq_begin_key and altitude() >= maxq_begin and not maxq:
            vessel.control.throttle = 0.50     
            print "... Throttle down"
            maxq_begin_key = True
        elif maxq_begin_key and altitude() >= maxq_end and not maxq_end_key and maxq:
            vessel.control.throttle = 1.0                    
            print "... Throttle up"
            maxq_end_key = True    


        maxq_md = ( maxq_begin + maxq_end ) / 2

        if altitude() >= maxq_md and not maxq and maxq_begin_key:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_falcon9.wav")
                pygame.mixer.music.play()                        

            print "MAX-Q"
            maxq = True        

        if srb_fuel_2() <= srb_tx and maxq_end_key:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/meco_falcon9.wav")
                pygame.mixer.music.play()
                meco = True

            print "MECO"
            print "... Separation first stage"          
            vessel.control.throttle = 0.0
            time.sleep(2)                 
            meco = True

            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(1)                    
    
        if meco:
            vessel.auto_pilot.target_pitch_and_heading(0, orientation) 

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

# Single stage ascent to orbit
def ssto(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation, sound):        
    pitch_roll = False
    maxq = False
    maxq_begin_key = False
    maxq_end_key = False
    supersonic = False    
    supersonic_v = 320
    meco = False
    solar_panels = False

    conn = krpc.connect(name='Ascent single stage')
    vessel = conn.space_center.active_vessel
    ksc = conn.space_center    
    nave = ksc.active_vessel
    rf = nave.orbit.body.reference_frame

    ## atmosphere
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    atmosphere = False

    # Set up streams for telemetry
    # general
    ut = conn.add_stream(getattr, conn.space_center, 'ut')
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    velocidade = conn.add_stream(getattr, nave.flight(rf), 'speed')

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    # # second stage
    # stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    # srb_fuel_1 = conn.add_stream(stage_1.amount, 'SolidFuel')

    # # first stage
    # stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    # srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    # print srb_fuel_1()
    # print srb_fuel_2()
    # target_vessel
    
    # calc tx
    # srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

    # srb_tx = (srb_fuel_1()*taxa)

    # if srb_tx == 0:
    #     warning_error()

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../audio/liftoff_falcon9.wav")
        pygame.mixer.music.play()
        countdown()

    print "... IGNITION!"
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
        ## atmosphere check
        if surAlt >= 70000 and not atmosphere:
            atmosphere = True

        # Gravity turn
        if altitude() >= turn_start_altitude and altitude() <= turn_end_altitude:                        
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
                srbs_separated = True
                vessel.control.throttle = 1.0
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_roll:
            print "... Heading/Pitch/Roll"
            pitch_roll = True

        if velocidade() >= supersonic_v and not supersonic:
            print "... Supersonic"
            supersonic = True

        if not maxq_begin_key and altitude() >= maxq_begin and not maxq:
            vessel.control.throttle = 0.50     
            print "... Throttle down"
            maxq_begin_key = True
        elif maxq_begin_key and altitude() >= maxq_end and not maxq_end_key and maxq:
            vessel.control.throttle = 1.0                    
            print "... Throttle up"
            maxq_end_key = True    


        maxq_md = ( maxq_begin + maxq_end ) / 2

        if altitude() >= maxq_md and not maxq and maxq_begin_key:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../audio/maxq_falcon9.wav")
                pygame.mixer.music.play()                        

            print "MAX-Q"
            maxq = True        

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            print "... Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print "MECO"
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

################################# END ESPECIFIC FUNCTIONS #################################