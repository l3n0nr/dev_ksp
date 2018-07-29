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
					"solid_separation", "fairing deploy", "second-stg_separation", "third-stg_ignition1", "shutdown_third-stg",  
		  			"third-stg_ignition2", "shutdown_third-stg", "finalized" ]

# seconds - minutes - hours		  
# countdown_ariane = [ "0s", "7s", "12s", "17s", 
# 		  			 "2m19s", "3m44s", "9m01s", "9m19s", "19m58s",
# 		  			 "3h27m50s", "3h34m08s", "4h12m59s" ]

# seconds
countdown_ariane = [ 0, 7, 12, 17, 
		  			 139, 224, 541, 559, 1198,
		  			 12470, 12848, 15132]	

# Falcon 9 - Iridium 7 (25/07/18)
sequence_f9_land = [ "LIFTOFF", "Max-Q", "Meco", "1stage separation", 
					 "2stage ignition", "fairing deploy", "1stage reentry burn", "landing",
					 "SECO-1", "2stage engine restart", "SECO-2", "Start deploy's", "End deploy's" ]

countdown_f9_land = [ 0, ]
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

		# walk the array
		for x in range(len(sequence_ariane)):		
			if x==0:				
				time.sleep(convert)
				print "T+", countdown_ariane[x], "s", " |", sequence_ariane[x]									
			else:				
				#capture time
				cont=countdown_ariane[x]

				# check time before of value captured
				cont_dif=countdown_ariane[x-1]

				# calculate time real
				convert=cont-cont_dif

				# format output in column exactly
				if cont<=9:					
					print "*", convert, "seconds for next action...\n"

					# wait time
					time.sleep(convert)			

					# show status
					print "T+", countdown_ariane[x], "s", " |", sequence_ariane[x]
				else:
					print "*", convert, "seconds for next action...\n"

					# wait time
					time.sleep(convert)			

					# show status
					print "T+", countdown_ariane[x], "s", "|", sequence_ariane[x]

		print ("##################")

## CALL SCRIPT
rocket_profile_mission()

## FOOT