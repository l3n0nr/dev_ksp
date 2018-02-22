#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# References:
#	KRPC - Github
#	<https://krpc.github.io/krpc/python/client.html>
#                                                                         
# Date: 18/03/02
# Author: Lenon Ricardo(lenonr)
# Version: 0.0.10
#	a = alpha, beta, stable, freeze;
#	b = bugs;
#	c = version;
# 
# Functions:
#   - P1: Launch;
#       	- Development: Start: 18/02/03 - Working: 18/02/03.
#   - P2: Control Speed;
#		-P2.1: Position Manuver: 
#       	- Development: Start: 18/02/03 - End: -.
#   - P3: Deploy
#		P3.1: Second Stage 
#			- Orbiter Manuver:
#		P3.2: First Stage  
#			- Suicide Burn:
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 
# script variables
in_atmosfere = 1200
out_atmosfere = 2400

# connect to the server
import krpc 	# import library

# conn = krpc.connect()	# open connection server
# print(conn.krpc.get_status().version)	# show version krpc

# # especific's information
# conn = krpc.connect(	# open connection server
#     name='SpaceX Style',	# name connection
#     address='127.0.0.1',		# ip connection
#     rpc_port=50000, stream_port=50001)	# others information's connection

# general information
conn = krpc.connect()
vessel = conn.space_center.active_vessel	# object representing the active vessel
vessel.name = "Falcon"						# name vessel
flight_info = vessel.flight()				#

# simples configurations
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90,270) # inclination/position
vessel.control.throttle = 1

# Liftoof
vessel.control.activate_next_stage()
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 
#