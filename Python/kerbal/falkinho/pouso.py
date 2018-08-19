# -*- coding: utf-8 -*-
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
    target_altitude         = 84500
    maxq_begin              = 12000
    maxq_end                = target_altitude
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

def calcula_gravidade(AltitudeNave, nave):
    parametro_gravitacional = nave.orbit.body.gravitational_parameter
    RaioAstro = nave.orbit.body.equatorial_radius
    R = RaioAstro + AltitudeNave()
    g = parametro_gravitacional / (R ** 2.)
    return -g

def calcula_queima_suicida(Velocidade, Impulso, Massa, altitude, nave):
    global altitude_nivel_mar
    margem_de_seguranca = 1.0 #se não está dando tempo de reduzir velocidade, tente entre 1.1 e 1.2
    gravidade = calcula_gravidade(altitude, nave)
    va = ((Impulso()/Massa()) + gravidade)
    A = (Velocidade() ** 2) / (2 * va)
    return A * margem_de_seguranca		

def ControlePouso(nave, velocidade_vertical, velocidade, altitude, massatotal, impulso, atmosfera = True):
    print(atmosfera, altitude(), (calcula_queima_suicida(velocidade, impulso, massatotal, altitude, nave) - velocidade_vertical()), velocidade(), -velocidade_vertical())
    if altitude() < 3000:
        if altitude() <= (calcula_queima_suicida(velocidade, impulso, massatotal, altitude, nave) - velocidade_vertical()):
            nave.control.throttle = 1.0

    if velocidade_vertical() > -15:
        gravidade = calcula_gravidade(altitude, nave)
        try:
            zeraraceleracao = (massatotal() * -gravidade) / impulso()
        except:
            zeraraceleracao = nave.control.throttle
        if atmosfera:
            if velocidade_vertical() > -15:
                if velocidade_vertical() < -5 and velocidade_vertical() > -15:
                    nave.control.throttle = zeraraceleracao
                elif velocidade_vertical() > -5:
                    nave.control.throttle = zeraraceleracao - 0.1
                elif velocidade_vertical() < -10:
                    nave.control.throttle = zeraraceleracao + 0.1
        else:
            if altitude() > 90 and altitude() < 300:
                if velocidade_vertical() < -9 and velocidade_vertical() > -10:
                    nave.control.throttle = zeraraceleracao
                elif velocidade_vertical() > -9:
                    nave.control.throttle = zeraraceleracao - 0.1
                elif velocidade_vertical() < -10:
                    nave.control.throttle = zeraraceleracao + 0.1
            elif altitude() > 30 and altitude() < 90:
                if velocidade_vertical() < -5 and velocidade_vertical() > -6:
                    nave.control.throttle = zeraraceleracao
                elif velocidade_vertical() > -5:
                    nave.control.throttle = zeraraceleracao - 0.1
                elif velocidade_vertical() < -6:
                    nave.control.throttle = zeraraceleracao + 0.1
            elif altitude() > 20 and altitude() < 30:
                if velocidade_vertical() < -1 and velocidade_vertical() > -3:
                    nave.control.throttle = zeraraceleracao
                elif velocidade_vertical() > -1:
                    nave.control.throttle = zeraraceleracao - 0.1
                elif velocidade_vertical() < -3:
                    nave.control.throttle = zeraraceleracao + 0.1
            elif altitude() < 20:
                if velocidade_vertical() < -0.75 and velocidade_vertical() > -1.25:
                    nave.control.throttle = zeraraceleracao
                elif velocidade_vertical() > -0.5:
                    nave.control.throttle = zeraraceleracao - 0.1
                elif velocidade_vertical() < -1.1:
                    nave.control.throttle = zeraraceleracao + 0.1
    try:
        if velocidade_horizontal() > 300.0:
            if nave.control.sas_mode is not ksc.SASMode.retrograde:
                nave.control.sas_mode = ksc.SASMode.retrograde
        else:
            if nave.control.sas_mode is not ksc.SASMode.radial:
                nave.control.rcs = True
                nave.control.sas_mode = ksc.SASMode.radial
                nave.auto_pilot.sas_mode = ksc.SASMode.radial
    except:
        pass

def landing():    	
	print ('Reentry core')
	# nave.control.rcs = False
	# nave.control.sas = True
	# nave.control.brakes = True

	altitude_mantis = conn.add_stream(getattr, nave.flight(rf), 'surface_altitude')
	velocidade_mantis = conn.add_stream(getattr, nave.flight(rf), 'speed')
	velocidade_vertical_mantis = conn.add_stream(getattr, nave.flight(rf), 'vertical_speed')
	impulso_mantis = conn.add_stream(getattr, nave, 'max_thrust')
	massatotal_mantis = conn.add_stream(getattr, nave, 'mass')
	
	def pousar(nave):
		global t, Mantis
		del(t)
		t = tela()
		nave.auto_pilot.sas = True
		nave.auto_pilot.rcs = True
		try:
			nave.auto_pilot.sas_mode = ksc.SASMode.retrograde
		except:
			pass
		sleep(5)
		ksc.warp_to(ut() + 180)
		while not nave.parts.legs[0].is_grounded:
			if altitude_mantis() < 5000:
				ControlePouso(nave, velocidade_vertical_mantis, velocidade_mantis, altitude_mantis, massatotal_mantis, impulso_mantis, True)
	        if not nave.control.brakes:
	            if altitude_mantis() < 50000:
	                nave.control.brakes = True
	                # t.mensagem('Ativando aerofreios')
	                sleep(2)
	                # t.mensagem('')
	        if not nave.control.gear:
	            if velocidade_vertical_mantis() > -100 and altitude_mantis() < 500:
	                nave.control.gear = True
	                # t.mensagem('Baixando as pernas')
		nave.control.throttle = 0.0
		nave.control.brakes = False
		nave.auto_pilot.sas = True
		nave.auto_pilot.sas_mode = ksc.SASMode.radial
	    # t.mensagem('')
	    # del(t)

## call functions
launch()
landing()

## nao esta chamando as funcoes corretamente, mais perto do que nunca para o suicide burn