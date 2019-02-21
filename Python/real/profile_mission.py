#!/usr/bin/env python
#
###############################################
# AUTHOR: lenonr
#
# VERSION: 0.46
#
# CREATION DATE: 23/07/18
# LAST MODIFICATION: 21/02/19
#
# DESCRIPTION: 
#	Show rocket profile by time(T+)
#		Ariane V
#		Soyuz
#		Falcon 9 Landing/No-Landing
#		Falcon Heavy
#		Delta IV Heavy
#
###############################################
# BODY
import os, sys, time

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

## VARIABLES
###############################################
var_sleep=1			# 0 = disabled = countdown instantaneous
					# 1 = enable   = countdown real time

## VECTORS
# style launch
profile = [ "ariane", 
			"soyuz", 
			"f9_noland", 
			"f9_land", 
			"falconh", 
			"deltaiv_h"
		  ]

# status profile
# Ariane V - VA244 Galileo - (25/07/18)
# Livestream: <youtu.be/VcBtLTGi-R4?t=1280>
# Presskit: <>
sequence_ariane = [ "Ignition_mainstage", "Ignition_solidbooster - LIFTOFF!!", "Pitch/yaw", "Roll", 
					"Solid_separation", "Fairing deploy", "Second-stg_separation", "Third-stg_ignition1", 
					"Shutdown_third-stg", "Third-stg_ignition2", "Shutdown_third-stg", "Finalized" ]

# hours - minutes - seconds
countdown_ariane = [ "000000", "000007", "000012", "000017", 
		  			 "000219", "000344", "000901", "000919", 
		  			 "001958", "032750", "033408", "041259" ]

# # Falcon 9 - Iridium 7 NEXT - (25/07/18)
# # Livestream: <youtu.be/vsDknmK30C0?t=1313>
# # Presskit: <spacex.com/sites/spacex/files/iridium7_press_kit_7_24.pdf>
# sequence_f9_land = [ "LIFTOFF", "Max-Q", "MECO", "1stage separation", 
# 					 "2stage ignition", "Fairing deploy", "1stage reentry burn", "LANDING",
# 					 "SECO-1", "2stage engine restart", "SECO-2", "Start deploy's payload's", "End deploy's payload's" ]

# countdown_f9_land = [ "000000", "000112", "000224", "000227", 
# 					  "000229", "000311", "000539", "000717", 
# 					  "000833", "005128", "005137", "005638", 
# 					  "011138" ]

# Falcon 9 - Telstar 18V - (10/09/18)
# Livestream: <>
# Presskit: <https://www.spacex.com/sites/spacex/files/telstar18vantagepresskit.pdf>
# sequence_f9_land = [ "LIFTOFF", "Max-Q", "MECO", 
# 					"Separation", "SES-1", "Fairing deploy", 
# 					"Reentry burn", "SECO-1", "LANDING",
# 					"SES-2", "SECO-2", "Deploy's payload's", 
# 					"Final mission" ]

# countdown_f9_land = [ "000000", "000107", "000233", 
# 					  "000237", "000245", "000329", 
# 					  "000617", "000814", "000832", 
# 					  "002617", "002700", "003201", 
# 					  "003206" ]

# Falcon 9 - Nusantara Satu + Beresheet + GTO 1 - (21/02/18)
# Livestream: <>
# Presskit: <https://www.spacex.com/sites/spacex/files/nusantara_satu_press_kit.pdf>
sequence_f9_land = [ "LIFTOFF", "Max-Q", "MECO", 
					"First Stage Separation", "SES-1", "Fairing deployment", 
					"Reentry burn", "SECO-1", "LANDING",
					"SES-2", "SECO-2", "Beresheet deployment", 
					"Nusantara Satu and Air Force Research Laboratory S5 deployment" ]

countdown_f9_land = [ "000000", "000107", "000237", 
					  "000240", "000248", "000346", 
					  "000644", "000807", "000832", 
					  "002703", "002808", "003339", 
					  "004438" ]

# Falcon Heavy - Test Flight - (06/02/18)
# Livestream: <youtu.be/wbSwFU6tY1c?t=1309>
# Presskit: <https://www.spacex.com/sites/spacex/files/falconheavypresskit_v1.pdf>
sequence_falconh = [ "LIFTOFF", "Max-Q", "Side boosters - BECO", 
					 "Side cores separate", "Side cores - boostback burn", "Center Core - MECO", 
					 "Center Core - 2stage separation", "2stage engine started", "Center core - boostback burn", 
					 "Fairing deployment", "Side cores - Reentry burn", "Center core - Reentry burn", 
					 "Side cores - LANDING", "Center core - LANDING", "SECO-1", 
					 "2stage engine restart", "SECO-2"]

countdown_falconh = [ "000000", "000106", "000229", 
					  "000233", "000250", "000304", 
					  "000307", "000315", "000324", 
					  "000349", "000641", "000647", 
					  "000758", "000819", "000831", 
					  "002822", "002852" ]

## Delta IV Heavy - Parker Solar Probe - (11/08/18)
# Livestream: <>
# Presskit: <https://www.ulalaunch.com/docs/default-source/launch-booklets/divh_parkersolarprobe_mob.pdf>

## orion test flight
# sequence_deltaivheavy = [ "LIFTOFF", "Max-Q", "BECO", 
# 						  "MECO", "1stage sepation", "2stage ignition #1",
# 						  "Fairing sepation", "SECO #1", "2stage ignition #2", 
# 						  "SECO #2", "Deploy"]

# countdown_deltaivheavy = [ "000000", "000123", "000356", 
# 						   "000530", "000533", "000549", 
# 						   "000615", "001739", "015526", 
# 						   "020009", "020010"]

sequence_deltaivheavy = [ "LIFTOFF", "Port and Starboard booster Jettison", "MECO", 
						  "1stage separation", "MES-1", "Fairing injection",
						  "MECO-1", "MES-2", "MECO-2", 
						  "2stage sepation", "3stage ignition", "3stage burnout",
						  "Parker Solar Probe sepation"]

countdown_deltaivheavy = [ "000000", "000357", "000535", 
						   "000542", "000555", "000605", 
						   "001037", "002225", "003638", 
						   "003709", "003729", "003858", 
						   "004318"]

# soyuz  = [liftoff, maxq, sepation1, meco, sepation2, seco, sepation2, deploy]
# falcon9_nolanding  = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]
# falconh  = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]

## FUNCION PROFILE MISSION
###############################################
def ariane():
	print ("SEQUENCE STARTED!")
	print ('#' * 20)

	last_value_list=(len(countdown_ariane)-1)

	# walk the array
	for x in range(len(sequence_ariane)):	
		if x==last_value_list:
			print "T+", countdown_ariane[x][0:2], "h", countdown_ariane[x][2:4], "m", countdown_ariane[x][4:6], "s", " |", sequence_ariane[x]			

			break
		if x<=1:			
			# capture values
			value = int(countdown_ariane[x])
			value_x = int(countdown_ariane[x+1])

			# convert time
			next_action = abs(value - value_x)

			# show message
			print "T+", countdown_ariane[x][0:2], "h", countdown_ariane[x][2:4], "m", countdown_ariane[x][4:6], "s", " |", sequence_ariane[x]
			# print "* Next action: ", next_action, "seconds - ", sequence_ariane[x+1], "\n"
			print "* Next action: ", countdown_ariane[x+1][0:2], "h", countdown_ariane[x+1][2:4], "m", countdown_ariane[x+1][4:6], "s -", sequence_ariane[x+1], "\n"

			if var_sleep==1:
				time.sleep(next_action)
		else:
			value = countdown_ariane[x]
			value_x = countdown_ariane[x+1]

			hours = value[0:2]
			minutes = value[2:4]
			seconds = value[4:6]			

			hours_now_conv = int(hours) * 3600
			minute_now_conv = int(minutes) * 60
			second_now_conv = (hours_now_conv + minute_now_conv + int(seconds))			

			hours_x = value_x[0:2]
			minutes_x = value_x[2:4]
			seconds_x = value_x[4:6]

			hours_now_conv_x = int(hours_x) * 3600
			minute_now_conv_x = int(minutes_x) * 60
			second_now_conv_x = (hours_now_conv_x + minute_now_conv_x + int(seconds_x))			

			next_action = second_now_conv_x - second_now_conv

			print "T+", hours, "h", minutes, "m", seconds, "s", " |", sequence_ariane[x]
			print "* Next action: " , hours_x, "h", minutes_x, "m", seconds_x, " - ", sequence_ariane[x+1], "\n"			

			if var_sleep==1:
				time.sleep(next_action)

def f9_land():
	print ("SEQUENCE STARTED!")
	print ('#' * 20)			

	last_value_list=(len(countdown_f9_land)-1)

	# walk the array
	for x in range(len(sequence_f9_land)):	
		if x==last_value_list:
			print "T+", countdown_f9_land[x][0:2], "h", countdown_f9_land[x][2:4], "m", countdown_f9_land[x][4:6], "s", " |", sequence_f9_land[x]

			break
		else:
			value = countdown_f9_land[x]
			value_x = countdown_f9_land[x+1]

			hours = value[0:2]
			minutes = value[2:4]
			seconds = value[4:6]			

			hours_now_conv = int(hours) * 3600
			minute_now_conv = int(minutes) * 60
			second_now_conv = (hours_now_conv + minute_now_conv + int(seconds))			

			hours_x = value_x[0:2]
			minutes_x = value_x[2:4]
			seconds_x = value_x[4:6]

			hours_now_conv_x = int(hours_x) * 3600
			minute_now_conv_x = int(minutes_x) * 60
			second_now_conv_x = (hours_now_conv_x + minute_now_conv_x + int(seconds_x))			

			next_action = second_now_conv_x - second_now_conv

			print "T+", hours, "h", minutes, "m", seconds, "s", " |", sequence_f9_land[x]
			print "* Next action: " , hours_x, "h", minutes_x, "m", seconds_x, "s", "-", sequence_f9_land[x+1], "\n"

			if var_sleep==1:
				time.sleep(next_action)

def falconh():
	print ("SEQUENCE STARTED!")
	print ('#' * 20)

	last_value_list=(len(countdown_falconh)-1)

	# walk the array
	for x in range(len(sequence_falconh)):	
		if x==last_value_list:
			print "T+", countdown_falconh[x][0:2], "h", countdown_falconh[x][2:4], "m", countdown_falconh[x][4:6], "s", " |", sequence_falconh[x]

			break
		else:
			value = countdown_falconh[x]
			value_x = countdown_falconh[x+1]

			hours = value[0:2]
			minutes = value[2:4]
			seconds = value[4:6]			

			hours_now_conv = int(hours) * 3600
			minute_now_conv = int(minutes) * 60
			second_now_conv = (hours_now_conv + minute_now_conv + int(seconds))			

			hours_x = value_x[0:2]
			minutes_x = value_x[2:4]
			seconds_x = value_x[4:6]

			hours_now_conv_x = int(hours_x) * 3600
			minute_now_conv_x = int(minutes_x) * 60
			second_now_conv_x = (hours_now_conv_x + minute_now_conv_x + int(seconds_x))			

			next_action = second_now_conv_x - second_now_conv

			print "T+", hours, "h", minutes, "m", seconds, "s", " |", sequence_falconh[x]
			print "* Next action: " , hours_x, "h", minutes_x, "m", seconds_x, "s", "-", sequence_falconh[x+1], "\n"

			if var_sleep==1:
				time.sleep(next_action)

def deltaiv_h():
	print ("SEQUENCE STARTED!")
	print ('#' * 20)

	last_value_list=(len(countdown_deltaivheavy)-1)

	# walk the array
	for x in range(len(sequence_deltaivheavy)):	
		if x==last_value_list:
			print "T+", countdown_deltaivheavy[x][0:2], "h", countdown_deltaivheavy[x][2:4], "m", countdown_deltaivheavy[x][4:6], "s", " |", sequence_deltaivheavy[x]

			break
		else:
			value = countdown_deltaivheavy[x]
			value_x = countdown_deltaivheavy[x+1]

			hours = value[0:2]
			minutes = value[2:4]
			seconds = value[4:6]			

			hours_now_conv = int(hours) * 3600
			minute_now_conv = int(minutes) * 60
			second_now_conv = (hours_now_conv + minute_now_conv + int(seconds))			

			hours_x = value_x[0:2]
			minutes_x = value_x[2:4]
			seconds_x = value_x[4:6]

			hours_now_conv_x = int(hours_x) * 3600
			minute_now_conv_x = int(minutes_x) * 60
			second_now_conv_x = (hours_now_conv_x + minute_now_conv_x + int(seconds_x))			

			next_action = second_now_conv_x - second_now_conv

			print "T+", hours, "h", minutes, "m", seconds, "s", " |", sequence_deltaivheavy[x]
			print "* Next action: " , hours_x, "h", minutes_x, "m", seconds_x, "s", "-", sequence_deltaivheavy[x+1], "\n"

			if var_sleep==1:
				time.sleep(next_action)

def rocket_profile_mission():
	## initial messages config's
	print ("Rocket's available's:")
	print (' or '.join(profile))

	rocket_name = raw_input("\nThe Vehicle for Launch: ")			

	print ('#' * 20)
	## verify rocket
	if rocket_name == "ariane":				
		ariane()
	elif rocket_name == "f9_land":	
		f9_land()
	elif rocket_name == "f9_noland":	
		print "F9 LAND"
	elif rocket_name == "falconh":
		falconh()
	elif rocket_name == "soyuz":
		print "Soyuz"		
	elif rocket_name == "deltaiv_h":
		deltaiv_h()
	else:
		print "ERROR"

	print ('#' * 20)

## CALL SCRIPT
rocket_profile_mission()

## FOOT