#!/usr/bin/env python
#
###############################################
# AUTHOR: lenonr
#
# VERSION: 0.10
#
# CREATION DATE: 23/07/18
# LAST MODIFICATION: 23/07/18
#
# DESCRIPTION: 
#	Show time profile by type rocket, one by one.
#
###############################################
# BODY
import os, sys
os.system('cls' if os.name == 'nt' else 'clear')

## VARIABLES
###############################################
## SETAR TEMPO AUTOMATICAMENTE
# style launch
profile = ["ariane", "soyuz", "falcon9_nolanding", "falcon9_landing", "falconh"]

# status profile
sequence_ariane = [ "ignition_mainstage", "ignition_solidbooster", "liftoff", "pitch", "roll", 
					"eap_separation", "fairing", "epc_separation", "eps_ignition1", "shutdown_eps1",  
		  			"eps_ignition2", "shutdown_eps2" ]
		  
countdown_ariane = [ "0s", "7s", "12s", "17s", 
		  			 "2m19s", "3m44s", "9m01s", "9m19s", "19m58s",
		  			 "3h27m50s", "3h34m08s" ]

# soyuz  = [liftoff, maxq, sepation1, meco, sepation2, seco, sepation2, deploy]
# falcon9_landing = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]
# falcon9_nolanding  = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]
# falconh  = [liftoff, maxq, meco, sepation1, seco, reentry_burn, landing, deploy]

## FUNCION PROFILE MISSION
###############################################
def rocket_profile_mission():
	print ("Profile's availables: " + str(profile))

	rocket_name = raw_input("The Vehicle for Launch: ")	

	# verify rocket
	if rocket_name == "ariane":
		print (countdown_ariane)

## CALL SCRIPT
rocket_profile_mission()