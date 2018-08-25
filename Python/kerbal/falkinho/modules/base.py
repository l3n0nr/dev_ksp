# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os, math, time, krpc, logging, math

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# Reference: https://krpc.github.io/krpc/tutorials/launch-into-orbit.html
# profile launch - low orbit
def launch(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, correction_time, taxa, orientation):        
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

    # resources stages
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    stage_1 = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel_1 = conn.add_stream(stage_1.amount, 'LiquidFuel')
    stage_2 = vessel.resources_in_decouple_stage(stage=0, cumulative=True)
    srb_fuel_2 = conn.add_stream(stage_2.amount, 'LiquidFuel')     

    srb_tx = (srb_fuel_2() - srb_fuel_1())*taxa

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
    time.sleep(1)    

    print('----T-01s: Ignition!')    
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
                # print('----Strongback separated')
                print('LIFTOOF!')                        

        if altitude() >= maxq_begin and altitude() <= maxq_end:
            vessel.control.throttle = 0.50            
        else:
            vessel.control.throttle = 1.0        

        if altitude() == maxq_begin:
                print ('MAX-Q')

        if srb_fuel_2() <= srb_tx or vessel.available_thrust == 0.0:                         
            print('MECO')
            vessel.control.throttle = 0.0
            time.sleep(1)

            print('----Separation first stage') 
            vessel.control.throttle = 0.30            
            vessel.control.activate_next_stage()            
            time.sleep(5)                    

            print('MES-1')      
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
    print('MECO-2')
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
    print('MES-2')   
    # vessel.control.throttle = 1.0            
    vessel.control.throttle = 0.5

    # while True:
    #     if vessel.available_thrust == 0.0:       
    #         vessel.control.throttle = 0.50

    #         vessel.control.activate_next_stage()        
    #         print('MECO-3')        
    #         time.sleep(3)

    #         print('----Separation second stage')            

    #         vessel.control.activate_next_stage()        
    #         print('MES-3')        
    #         break

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

# Reference: 
def landing(secure_burn):    
    conn = krpc.connect(name='Suicide Burn')
    vessel = conn.space_center.active_vessel
    refer = conn.space_center.active_vessel.orbit.body.reference_frame
    surAlt = conn.space_center.active_vessel.flight(refer).surface_altitude
    situacao = conn.add_stream(getattr, vessel, 'situation')
    pousado_agua = conn.space_center.VesselSituation.splashed
    pousado = conn.space_center.VesselSituation.landed
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

    # canvas = conn.ui.stock_canvas
    # screen_size = canvas.rect_transform.size
    # panel = canvas.add_panel()
    # rect = panel.rect_transform
    # rect.size = (400, 100)
    # rect.position = (250 - (screen_size[0] / 2), -100)
    # text = panel.add_text("Telemetria")
    # text.rect_transform.position = (-30, 0)
    # text.color = (1, 1, 1)
    # text.size = 16

    while altitude() <= secure_burn:
        pass

    global pouso
    pouso = False    

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
        main()
    else:
        print("Foguete atualmente pousado")
        print("Encerrando processo...")
    text.content = 'Foguete Pousado'
    naveAtual.control.throttle = 0
    vessel.control.rcs = True
    vessel.control.sas = True
    # vessel.control.sas_mode = conn.space_center.SASMode.stability_assist
    print('TOUCHDOWN!!!!!')
    time.sleep(2)
    print('estabilizando')
    time.sleep(6)
    print('pouso terminado, desligando tudo, tchau!!')
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.brakes = False