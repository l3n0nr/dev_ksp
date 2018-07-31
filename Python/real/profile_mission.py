#!/usr/bin/env python
#
###############################################
# AUTHOR: lenonr
#
# VERSION: 0.15
#
# CREATION DATE: 23/07/18
# LAST MODIFICATION: 28/07/18
#
# DESCRIPTION: 
#	Show time profile by type rocket, one by one.
#		Ariane 5
#		Soyuz
#		F9/FH
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
	# start variables
	cont=0
	cont_dif=0
	convert=0

	## initial messages config's
	print ("Rocket's available's:")
	print (' or '.join(profile))

	rocket_name = raw_input("\nThe Vehicle for Launch: ")	

	# verify rocket
	if rocket_name == "ariane":		
		value = 0
		value_x = 0

		print ("\nSEQUENCE STARTED!")
		print ("#######################")		

		# walk the array
		for x in range(len(sequence_ariane)):	
			if x==0:
				print
				# print "T+", countdown_ariane[x][0:2], "h", countdown_ariane[x][2:4], "m", countdown_ariane[x][4:6], "s", " |", sequence_ariane[x]
				# print "* Next action: ", countdown_ariane[x+1][4:6], "seconds\n"								
			if x==1:
				value = countdown_ariane[x]
				value_x = countdown_ariane[x+1]
			else:
				value = countdown_ariane[x]
				value_x = countdown_ariane[x-1]

			hours = value[0:2]
			minutes = value[2:4]
			seconds = value[4:6]

			hours_x = value_x[0:2]
			minutes_x = value_x[2:4]
			seconds_x = value_x[4:6]

			hours_now_conv = int(hours) * 3600
			minute_now_conv = int(minutes) * 60
			second_now_conv = (hours_now_conv + minute_now_conv + int(seconds))			

			hours_now_conv_x = int(hours_x) * 3600
			minute_now_conv_x = int(minutes_x) * 60
			second_now_conv_x = (hours_now_conv + minute_now_conv + int(seconds_x))			

			next_action = second_now_conv_x - second_now_conv				
			
			print "T+", hours, "h", minutes, "m", seconds, "s", " |", sequence_ariane[x]
			print "* Next action: ", next_action, "seconds\n"												

		print ("#######################")

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