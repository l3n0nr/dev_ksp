# -*- coding: utf-8 -*-
#!/usr/bin/env python

## import library's
import os, sys, math, time, krpc, pygame

### global variables
pitch_row = False
maxq = False
maq1 = False
maq1_v = 410
sound = True

## global parameters
turn_end_altitude       = 45000						# inclination end
maxq_begin              = 25000						# reduce aceleration stage - begin
maxq_end                = 70000						# reduce aceleration stage - end

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# Reference: <krpc.github.io/krpc/tutorials/launch-into-orbit.html>
# Profile launch: Not recovery first stage
def launch(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, taxa, orientation):            
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
        pygame.mixer.music.load("../audio/apollo.wav")
        pygame.mixer.music.play()

    print('T-10: All systems nominal for launch!')    
    time.sleep(1)    

    print('----T-09s: Internal Power!')
    time.sleep(1)

    print('----T-08s: Pressure tanks OK!')
    time.sleep(1)  

    print('----T-07s: Flight computer: GO - for launch!')
    time.sleep(1)        

    print('----T-06s: Trust Level Low!')
    vessel.control.throttle = 0.25
    time.sleep(1)              

    print('----T-05s: Director flight: GO - for launch!')
    time.sleep(1)

    print('----T-04s: Trust Level Intermediate')
    vessel.control.throttle = 0.50
    time.sleep(1)

    print('----T-03s: Kerbonauts: GO - for launch')
    time.sleep(1)

    print('----T-02s: Trust Level High')
    vessel.control.throttle = 1.00
    time.sleep(2)    

    print('----T-01s: IGNITION!')        
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
                print('LIFTOOF!')                        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print ('----Heading/Pitch/Row') 
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print ('----Max-Q')
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print ('----Supersonic')
            maq1 = True

        if srb_fuel_2() <= srb_tx or vessel.available_thrust == 0.0:                         
            print('MECO')
            vessel.control.throttle = 0.0
            time.sleep(1)

            print('----Separation first stage') 
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(5)                    

            print('SES-1')      
            vessel.control.activate_next_stage()                    
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
    print('SECO-1')
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print('----Coasting out of atmosphere')
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print('----Planning circularization burn')
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
    print('----Orientating ship for circularization burn')
    vessel.control.light = True
    vessel.control.rcs = True
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print('----Waiting until circularization burn')
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print('----Ready to execute burn')
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print('SES-2')   
    # vessel.control.throttle = 1.0            
    vessel.control.throttle = 0.5

    time.sleep(burn_time - 0.1)
    print('----Fine tuning')
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

    print('Launch complete')

# Reference: https://krpc.github.io/krpc/tutorials/launch-into-orbit.html
# Profile launch: Suborbital insertion
# The possible recovery of the first stage
def suborbital(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation):        
    pitch_row = False
    maxq = False
    maq1 = False
    maq1_v = 410

    sound = True

    seconds = 0
    seconds_unit = 0

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

    if srb_tx == 0:
        print('[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!')
        time.sleep(60)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../../audio/liftoff.wav")
        pygame.mixer.music.play()

    print('T-10: All systems nominal for launch!')    
    time.sleep(1)    

    print('----Internal power!')
    time.sleep(1)

    print('----Pressure tanks OK!')
    time.sleep(1)  

    print('----Flight computer: GO!')
    time.sleep(1)        

    print('----Trust level low.')
    vessel.control.throttle = 0.25
    time.sleep(1)              

    print('----Director flight: GO!')
    time.sleep(1)

    print('----Trust level intermediate.')
    vessel.control.throttle = 0.50
    time.sleep(1)

    print('----Kerbonauts: GO!')
    time.sleep(1)

    print('----Trust level high.')
    vessel.control.throttle = 1.00
    time.sleep(1)       

    print('----IGNITION!')    
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
        seconds_unit = seconds_unit + 1

        seconds = seconds_unit

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
        
        if altitude() >= turn_start_altitude and not pitch_row:
            # print "----T+", seconds, "----Heading/Pitch/Row"
            print "----Heading/Pitch/Row"

            pitch_row = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../../audio/maxq.wav")
                pygame.mixer.music.play()                        

            # print "----T+", seconds, "----Max-Q"
            print "----Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print ('----Supersonic')
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_2() <= srb_tx or vessel.available_thrust == 0.0:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../../audio/meco.wav")
                pygame.mixer.music.play()

            # print "----T+", seconds, "MECO"
            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            # print "----T+", seconds, "----Separation first stage"
            print "----Separation first stage"
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(5)                    

            # print "----T+", seconds, "SES-1"      
            print "SES-1"      
            print "----Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            # print "----T+", seconds, "----Approaching target apoapsis"
            print "----Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print('SECO-1')
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    # print "----T+", seconds, "----Coasting out of atmosphere"
    print "----Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    # print "----T+", seconds, "----Planning circularization burn"
    print "----Planning circularization burn"
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

    # print "----T+", seconds, "SUB-ORBITAL INSERTION COMPLETE"
    print "SUB-ORBITAL INSERTION COMPLETE"

# Autor: SirMazur
# Reference: <github.com/MrsMagoo/suicideBurn-Ksp>
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
        print ('Reentry Atmosphere...')    

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
            foguete = ksc.active_vessel
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
            # alturaPouso = 20.0
            alturaPouso = 50.0
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
            vessel.control.rcs = True
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
                print ('Reentry burn...')
                reentry_burn = True

                if sound:
                    # play sound
                    pygame.init()
                    pygame.mixer.music.load("audio/reentry_burn.wav")
                    pygame.mixer.music.play()                

            if surAlt <= 800 and not landing_burn and naveAtual.control.throttle != 0:
                print ('Landing burn...')
                landing_burn = True

                if sound:
                    # play sound
                    pygame.init()
                    pygame.mixer.music.load("audio/landing.wav")
                    pygame.mixer.music.play()                

            if surAlt < 200:         
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
        print ('ok')        

    naveAtual.control.throttle = 0
    vessel.control.rcs = True
    vessel.control.sas = True
    time.sleep(2)
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.brakes = False    
        
    print("LANDING!")

def circularize(target_altitude):    
    conn = krpc.connect(name='Circularize')
    ut = conn.add_stream(getattr, conn.space_center, 'ut')
    vessel = conn.space_center.active_vessel
    
    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print('----Planning circularization burn')
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

def fine(correction_time):
    conn = krpc.connect(name='Circularize')
    ut = conn.add_stream(getattr, conn.space_center, 'ut')
    vessel = conn.space_center.active_vessel

    # Plan circularization burn (using vis-viva equation)
    print('----Planning circularization burn')
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
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)

    # Execute burn
    print('----Ready to execute burn')
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    # while time_to_apoapsis() - (burn_time/1.) > 0:
    #     pass
         
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print('----Fine tuning')
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

# Reference: https://krpc.github.io/krpc/tutorials/launch-into-orbit.html
# Profile launch: Suborbital insertion
# The possible recovery of the first stage
def suborbital_triplo(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa_beco, taxa_meco, orientation):        
    pitch_row = False
    maxq = False
    maq1 = False
    beco = False
    maq1_v = 410

    sound = True

    seconds = 0
    seconds_unit = 0

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

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa_beco
    srb_tx_central = (srb_fuel_2() - srb_fuel_1())*taxa_meco

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../../audio/liftoff.wav")
        pygame.mixer.music.play()

    print('T-10: All systems nominal for launch!')    
    time.sleep(1)    

    print('----Internal power!')
    time.sleep(1)

    print('----Pressure tanks OK!')
    time.sleep(1)  

    print('----Flight computer: GO!')
    time.sleep(1)        

    print('----Trust level low.')
    vessel.control.throttle = 0.25
    time.sleep(1)              

    print('----Director flight: GO!')
    time.sleep(1)

    print('----Trust level intermediate.')
    vessel.control.throttle = 0.50
    time.sleep(1)

    print('----Kerbonauts: GO!')
    time.sleep(1)

    print('----Trust level high.')
    vessel.control.throttle = 1.00
    time.sleep(1)    
 
    print('----IGNITION!')    
    # Activate the first stage    
    vessel.control.activate_next_stage()
    vessel.control.throttle = 0.30
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
                vessel.control.throttle = 1.00
                srbs_separated = True
                print "LIFTOOF!"
        
        if altitude() >= turn_start_altitude and not pitch_row:
            # print "----T+", seconds, "----Heading/Pitch/Row"
            # print "----Heading/Pitch/Row"

            pitch_row = True

        if velocidade() >= maq1_v and not maq1:
            print ('----Supersonic')
            maq1 = True

        if altitude() >= maxq_begin and not maxq:            
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../../audio/maxq.wav")
                pygame.mixer.music.play()                        

            # print "----T+", seconds, "----Max-Q"
            print "----Max-Q"
            maxq = True        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        # side boosters separation
        if srb_fuel_2() <= srb_tx and not beco:              
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../../audio/beco.wav")
                pygame.mixer.music.play()

            print "BECO"
            print "----Separation side boosters"            

            vessel.control.throttle = 0
            time.sleep(1)
            vessel.control.activate_next_stage()            
            vessel.control.throttle = 0.10                
            time.sleep(2)
            vessel.control.throttle = 1.0                          

            stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
            srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

            stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
            srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')
            stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
            srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

            # testing margin for recuperation of the central core
            srb_tx_central = (srb_fuel_2() - srb_fuel_1())*taxa_meco

            beco = True

        # re-calculate resources central core
        # if beco:            
        #     stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
        #     srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

        #     stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
        #     srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')
        #     stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
        #     srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

        #     # testing margin for recuperation of the central core
        #     srb_tx_central = (srb_fuel_2() - srb_fuel_1())*taxa_meco

        # central core separation
        if srb_fuel_2() <= srb_tx_central and beco:    
            if sound:
                # play sound
                pygame.init()
                pygame.mixer.music.load("../../audio/meco.wav")
                pygame.mixer.music.play()

            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            print "----Separation central core"
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(5)                    
 
            print "SES-1"      
            print "----Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            # print "----T+", seconds, "----Approaching target apoapsis"
            print "----Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print('SECO-1')
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    # print "----T+", seconds, "----Coasting out of atmosphere"
    print "----Coasting out of atmosphere"
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    # print "----T+", seconds, "----Planning circularization burn"
    print "----Planning circularization burn"
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

    # print "----T+", seconds, "SUB-ORBITAL INSERTION COMPLETE"
    print "SUB-ORBITAL INSERTION COMPLETE"

# Reference: <krpc.github.io/krpc/tutorials/launch-into-orbit.html>
# Profile launch: Not recovery first stage
def ariane(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, orientation):            
    pitch_row = False
    maq1 = False    
    boosters_sepation = False
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

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    ## first stage 
    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')
    ## second stage + first stage
    stage_2 = vessel.resources_in_decouple_stage(stage=1, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')       

    # solid boosters
    stage_solid = vessel.resources_in_decouple_stage(stage=2, cumulative=True)
    solid_boosters = conn.add_stream(stage_solid.amount, 'SolidFuel')  

    # print srb_tx

    # time.sleep(10)

    # play sound t-10
    if sound:
        pygame.init()
        pygame.mixer.music.load("../../audio/ariane_countdown.wav")
        pygame.mixer.music.play()

    print('T-10: All systems nominal for launch!')    
    time.sleep(1)    

    print('----T-09s: Internal Power!')
    time.sleep(1)

    print('----T-08s: Pressure tanks OK!')
    time.sleep(1)  

    print('----T-07s: Flight computer: GO - for launch!')
    time.sleep(1)        

    print('----T-06s: Trust Level Low!')
    vessel.control.throttle = 0.25
    time.sleep(1)              

    print('----T-05s: Director flight: GO - for launch!')
    time.sleep(1)

    print('----T-04s: Trust Level Intermediate')
    vessel.control.throttle = 0.50
    time.sleep(1)

    print('----T-03s: Kerbonauts: GO - for launch')
    time.sleep(1)

    print('----T-02s: Trust Level High')
    vessel.control.throttle = 1.00
    time.sleep(3)    

    print('----T-01s: Ignition Main Engine!')         

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

    time.sleep(4)    

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
                vessel.control.activate_next_stage()
                srbs_separated = True
                print('LIFTOOF!')                        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() >= turn_start_altitude and not pitch_row:
            print ('----Heading/Pitch/Row') 
            pitch_row = True        

        if altitude() >= maxq_begin and not maxq:            
            print ('----Max-Q')
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print ('----Supersonic')
            maq1 = True

        if solid_boosters() <= 3 and not boosters_sepation:
            print('----Boosters Separation')
            vessel.control.activate_next_stage()
            boosters_sepation = True
   
        if srb_tx < 1:                      
            print('MECO')
            vessel.control.throttle = 0.0
            time.sleep(1)            

            print('----Separation first stage') 
            print('----Fairing separation') 
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(3)                 

            print('SES-1')      
            print "----Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
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
    print('SECO-1')
    vessel.control.throttle = 0.0

    # Wait until out of atmosphere
    print('----Coasting out of atmosphere')
    while altitude() < 70500:
        pass

    # Plan circularization burn (using vis-viva equation)
    time.sleep(5)
    print('----Planning circularization burn')
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
    print('----Orientating ship for circularization burn')
    vessel.control.light = True
    vessel.control.rcs = True
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.auto_pilot.wait()

    # Wait until burn
    print('----Waiting until circularization burn')
    burn_ut = ut() + vessel.orbit.time_to_apoapsis - (burn_time/2.)
    lead_time = 5   
    conn.space_center.warp_to(burn_ut - lead_time)

    # Execute burn
    print('----Ready to execute burn')
    time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
    while time_to_apoapsis() - (burn_time/2.) > 0:
        pass
    print('SES-2')   
    vessel.control.throttle = 1

    time.sleep(burn_time - 0.1)
    print('----Fine tuning')
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

    print('LAUNCH COMPLETE')

# def newshepard(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation):
def newshepard(turn_start_altitude,target_altitude, taxa, orientation)
    # pitch_row = False
    # maxq = False
    # maq1 = False
    # maq1_v = 410

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
        print('[ERROR] CHECK YOUR PROBE, NOT POSSIBLE CALCULATE LANDING FUEL!')
        time.sleep(60)

    if sound:
        # play sound t-10    
        pygame.init()
        pygame.mixer.music.load("../../audio/liftoff.wav")
        pygame.mixer.music.play()

    print('T-10: All systems nominal for launch!')    
    time.sleep(1)    

    print('----Internal power!')
    time.sleep(1)

    print('----Pressure tanks OK!')
    time.sleep(1)  

    print('----Flight computer: GO!')
    time.sleep(1)        

    print('----Trust level low.')
    vessel.control.throttle = 0.25
    time.sleep(1)              

    print('----Director flight: GO!')
    time.sleep(1)

    print('----Trust level intermediate.')
    vessel.control.throttle = 0.50
    time.sleep(1)

    print('----Kerbonauts: GO!')
    time.sleep(1)

    print('----Trust level high.')
    vessel.control.throttle = 1.00
    time.sleep(1)       

    print('----IGNITION!')    
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
        
        if altitude() >= turn_start_altitude and not pitch_row:
            print "----Heading/Pitch/Row"

            pitch_row = True

        if altitude() >= maxq_begin and not maxq:                                
            print "----Max-Q"
            maxq = True

        if velocidade() >= maq1_v and not maq1:
            print ('----Supersonic')
            maq1 = True

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50                       
        else:
            vessel.control.throttle = 1.0        

        if srb_fuel_2() <= srb_tx:    
            print "MECO"
            vessel.control.throttle = 0.0
            time.sleep(1)

            print "----Separation first stage"
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(1)                    

            print "SES-1"      
            print "----Orbital burn manuveur"
            vessel.control.activate_next_stage()                    
            time.sleep(1)   
            break

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude*0.9:
            # print "----T+", seconds, "----Approaching target apoapsis"
            print "----Approaching target apoapsis"
            break  

    # Disable engines when target apoapsis is reached
    vessel.control.throttle = 1.0
    while apoapsis() < target_altitude:
        pass
    print('SECO-1')
    vessel.control.throttle = 0.0

    print "----Planning circularization burn"
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

    print "SUB-ORBITAL INSERTION COMPLETE"

## via interface - only test for now
def sub_orbital():
    print ('Suborbital')

def orbital_maneuver():
    print ('Orbital Maneuver')

def landing_test():
    print ('Landing')