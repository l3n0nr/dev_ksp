#!/usr/bin/env python
#
###############################################
# AUTHOR: lenonr
#
# VERSION: 0.18
#
# CREATION DATE: 23/07/18
# LAST MODIFICATION: 05/08/18
#
# DESCRIPTION: 
#	Show time profile by type rocket, one by one.
#		Ariane 5
#		Soyuz
#		F9/FH
#
# COMENTS
#	ERROR: CHECK SOLID_SEPARATION
#
###############################################
# BODY
import os, sys, time

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

## VARIABLES
###############################################
# style launch
profile = [ "ariane", 
			"soyuz", 
			"f9_noland", 
			"f9_land", 
			"falconh" 
		  ]

# status profile
# Ariane 5 - VA244 Galileo (25/07/18)
# Reference: <youtu.be/VcBtLTGi-R4?t=1280>
# Presskit: <>

sequence_ariane = [ "ignition_mainstage", "ignition_solidbooster - LIFTOFF!!", "pitch/yaw", "roll", 
					"solid_separation", "fairing deploy", "second-stg_separation", "third-stg_ignition1", 
					"shutdown_third-stg", "third-stg_ignition2", "shutdown_third-stg", "finalized" ]

# hours - minutes - seconds
countdown_ariane = [ "000000", "000007", "000012", "000017", 
		  			 "000219", "000344", "000901", "000919", 
		  			 "001958", "032750", "033408", "041259" ]

# Falcon 9 - Iridium 7 NEXT (25/07/18)
# Reference: <>
# Presskit: <>
sequence_f9_land = [ "LIFTOFF", "Max-Q", "Meco", "1stage separation", 
					 "2stage ignition", "fairing deploy", "1stage reentry burn", "landing",
					 "SECO-1", "2stage engine restart", "SECO-2", "Start deploy's paiload", "End deploy's paiload" ]

countdown_f9_land = [ "000000", "000112", "000224", "000227", 
					  "000229", "000311", "000539", "000717", 
					  "000833", "005128", "005137", "005638", 
					  "011138" ]

# soyuz  = [liftoff, maxq, sepation1, meco, sepation2, seco, sepation2, deploy]
# falcon9_nolanding  = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]
# falconh  = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]

var_sleep=0
# hours = 0
# minutes = 0
# seconds = 0
# value = 0
# value_x = 0	

## FUNCION PROFILE MISSION
###############################################
def ariane():
	print ("SEQUENCE STARTED!")
	print ("####################")			

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
			print "* Next action: ", next_action, "seconds\n"			

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
			print "* Next action: ", next_action, "seconds\n"			

			if var_sleep==1:
				time.sleep(next_action)

def f9_land():
	print ("SEQUENCE STARTED!")
	print ("####################")			

	last_value_list=(len(countdown_f9_land)-1)

	# walk the array
	for x in range(len(sequence_f9_land)):	
		if x==last_value_list:
			print "T+", countdown_f9_land[x][0:2], "h", countdown_f9_land[x][2:4], "m", countdown_f9_land[x][4:6], "s", " |", sequence_f9_land[x]			

			break
		if x<=1:			
			# capture values
			value = int(countdown_f9_land[x])
			value_x = int(countdown_f9_land[x+1])

			# convert time
			next_action = abs(value - value_x)

			# show message
			print "T+", countdown_f9_land[x][0:2], "h", countdown_f9_land[x][2:4], "m", countdown_f9_land[x][4:6], "s", " |", sequence_f9_land[x]
			print "* Next action: ", next_action, "seconds\n"			

			if var_sleep==1:
				time.sleep(next_action)
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
			print "* Next action: ", next_action, "seconds\n"			

			if var_sleep==1:
				time.sleep(next_action)

def rocket_profile_mission():
	## initial messages config's
	print ("Rocket's available's:")
	print (' or '.join(profile))

	rocket_name = raw_input("\nThe Vehicle for Launch: ")			

	## verify rocket
	if rocket_name == "ariane":				
		ariane()
	elif rocket_name == "f9_land":	
		f9_land()
	else:
		print ""

	print ("####################")

## CALL SCRIPT
rocket_profile_mission()

## FOOT