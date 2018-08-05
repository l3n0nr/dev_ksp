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
profile = [ "ariane", "soyuz", "f9_noland", "f9_land", "falconh" ]

# status profile
# Ariane 5 - VA244 Galileo (25/07/18)
# Reference: https://youtu.be/VcBtLTGi-R4?t=1280
sequence_ariane = [ "ignition_mainstage", "ignition_solidbooster - LIFTOFF!!", "pitch/yaw", "roll", 
					"solid_separation", "fairing deploy", "second-stg_separation", "third-stg_ignition1", 
					"shutdown_third-stg", "third-stg_ignition2", "shutdown_third-stg", "finalized" ]

# hours - minutes - seconds
countdown_ariane = [ "000000", "000007", "000012", "000017", 
		  			 "000219", "000344", "000901", "000919", 
		  			 "001958", "032750", "033408", "041259" ]

# # seconds
# countdown_ariane = [ 0, 7, 12, 17, 
# 		  			 139, 224, 541, 559, 1198,
# 		  			 12470, 12848, 15179]	

# Falcon 9 - Iridium 7 (25/07/18)
sequence_f9_land = [ "LIFTOFF", "Max-Q", "Meco", "1stage separation", 
					 "2stage ignition", "fairing deploy", "1stage reentry burn", "landing",
					 "SECO-1", "2stage engine restart", "SECO-2", "Start deploy's", "End deploy's" ]

# countdown_f9_land = [ 0, ]
# soyuz  = [liftoff, maxq, sepation1, meco, sepation2, seco, sepation2, deploy]
# falcon9_landing = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]
# falcon9_nolanding  = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]
# falconh  = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]

## FUNCION PROFILE MISSION
###############################################
def rocket_profile_mission():
	## initial messages config's
	# print ("Rocket's available's:")
	# print (' or '.join(profile))

	# rocket_name = raw_input("\nThe Vehicle for Launch: ")	

	# verify rocket
	# if rocket_name == "ariane":		

	print ("SEQUENCE STARTED!")
	print ("####################")	

	# walk the array
	for x in range(len(sequence_ariane)):		
		hours = 0
		minutes = 0
		seconds = 0
		value = 0
		value_x = 0

		# values (0-1)
		if x<=1:			
			# capture values
			value = int(countdown_ariane[x])
			value_x = int(countdown_ariane[x+1])

			# convert time
			next_action = abs(value - value_x)

			# show message
			print "T+", countdown_ariane[x][0:2], "h", countdown_ariane[x][2:4], "m", countdown_ariane[x][4:6], "s", " |", sequence_ariane[x]
			print "* Next action: ", next_action, "seconds\n"			

			# time.sleep(next_action)
		# value (2-*)
		else:						
			value = countdown_ariane[x]
			value_x = countdown_ariane[x-1]

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
			
			# rocket_profile_missiont hours, "hours", minutes, "minutes", seconds, "seconds"
			# print hours_x, "hours", minutes_x, "minutes", seconds_x, "seconds"
			# print "X:", value, ", X-1:", value_x, "|", second_now_conv, "-", second_now_conv_x, "=", (second_now_conv - second_now_conv_x)

			# case necessary, convert positive number
			# next_action = abs(second_now_conv_x - second_now_conv)
			next_action = second_now_conv - second_now_conv_x						

			print "T+", hours, "h", minutes, "m", seconds, "s", " |", sequence_ariane[x]
			print "* Next action: ", next_action, "seconds\n"			

			print "sleep:",next_action

			# time.sleep(next_action)

	print ("####################")

## CALL SCRIPT
rocket_profile_mission()

## FOOT

# #capture time - general
# count=countdown_ariane[x]
# count_dif=countdown_ariane[x-1]

# count_int=int(countdown_ariane[x])			
# count_dif_int=int(countdown_ariane[x-1])

# # print "cont",count
# # print "cont_dif",count_dif

# # calculate time real
# # convert=count_dif-count
# # convert_int=count_int-count_dif_int

# # print convert				

# ######### calculate time - seconds 
# hours_now = int(count[0:2])
# minute_now = int(count[2:4])
# second_now = int(count[4:6])

# # print hours_now
# # print minute_now
# # print second_now

# # print 

# # calculate time - seconds previous
# hours_now_conv = (hours_now * 3600)
# minute_now_conv = (minute_now * 60)
# second_now_conv = (hours_now + minute_now + second_now)						

# hours_prev = int(count_dif[0:2])
# minute_prev = int(count_dif[2:4])
# second_prev = int(count_dif[4:6])

# # print hours_prev
# # print minute_prev
# # print second_prev

# # print 

# hours_prev_conv = (hours_prev * 3600)
# minute_prev_conv = (minute_prev * 60)
# second_prev_conv = (hours_prev_conv + minute_prev_conv + second_prev)				

# second = int(second_prev - second_now)

# print second

# if x==0:								
# 	print "T+", countdown_ariane[x][4:6], "s", " |", sequence_ariane[x]									
# 	print "* Next action: ", countdown_ariane[x+1][4:6], "seconds\n"								

# 	time.sleep(float(second))

# 	# print second
# else:																		
# 	# print second_conv				
# 	time.sleep(float(second))

# 	print second

# format output in column exactly			
# if second<=9:					
# 	print "T+", countdown_ariane[x][4:6], "s", " |", sequence_ariane[x]
# 	# print "* Next action: ", countdown_ariane[x+1][4:6], "seconds\n"								
# 	print "* Next action: ", countdown_ariane[x+1][2:4], "minutes", countdown_ariane[x+1][4:6], "seconds\n"
# elif second<=60:					
# 	print "T+", countdown_ariane[x][4:6], "s", " |", sequence_ariane[x]
# 	print "* Next action: ", countdown_ariane[x+1][2:4], "minutes", countdown_ariane[x+1][4:6], "seconds\n"
# else:
# 	print "T+", countdown_ariane[x][0:6], "s", "|", sequence_ariane[x]
# 	print "* Next action: ", countdown_ariane[x+1][0:2], "hours", countdown_ariane[x][2:4], "minutes", countdown_ariane[x+1][4:6], "seconds\n"