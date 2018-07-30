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
sequence_ariane = [ "ignition_mainstage", "ignition_solidbooster/LIFTOFF!!", "pitch/yaw", "roll", 
					"solid_separation", "fairing deploy", "second-stg_separation", "third-stg_ignition1", 
					"shutdown_third-stg", "third-stg_ignition2", "shutdown_third-stg", "finalized" ]

# hours - minutes - seconds
countdown_ariane = [ "000000", "000007", "000012", "000017", 
		  			 "000219", "000344", "000901", "000919", 
		  			 "001958", "032750", "033408", "041259" ]

# # seconds
# countdown_ariane = [ 0, 7, 12, 17, 
# 		  			 139, 224, 541, 559, 1198,
# 		  			 12470, 12848, 15132]	

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
		print ("\nSEQUENCE STARTED!")
		print ("##################")

		# time.clock()

		# walk the array
		for x in range(len(sequence_ariane)):	
			# #capture time
			count=countdown_ariane[x]
			count_int=int(countdown_ariane[x])

			# check time before of value captured
			count_dif=countdown_ariane[x-1]
			count_dif_int=int(countdown_ariane[x-1])

			print "cont",count
			print "cont_dif",count_dif

			# calculate time real
			convert=count_dif-count
			convert_int=count_dif_int-count_int	

			# print convert				

			hours = count[0:2]
			# hours = int(count[0:2])
			minute = count[2:4]
			# minute = int(count[2:4])
			second = count[4:6]
			# second = int(count[4:6])

			hours_conv = (hours * 3600)
			minute_conv = (minute * 60)
			second_conv = (hours_conv + minute_conv + second)

			if x==0:								
				print "T+", countdown_ariane[x], "s", "  |", sequence_ariane[x]									
				time.sleep(convert)				
			else:															
				# format output in column exactly
				if count<=9:					
					print "* Next action: ", countdown_ariane[x][4:6], "seconds\n"
					print "T+", countdown_ariane[x], "s", "  |", sequence_ariane[x]
				elif count<=99:					
					print "* Next action: ", countdown_ariane[x][2:6], "\n"
					print "T+", countdown_ariane[x], "s", " |", sequence_ariane[x]
				else:
					print "* Next action: ", countdown_ariane[x][0:6], "\n"	
					print "T+", countdown_ariane[x], "s", "|", sequence_ariane[x]

				# print second_conv				
				time.sleep(convert)

		print ("##################")

## CALL SCRIPT
rocket_profile_mission()

## FOOT