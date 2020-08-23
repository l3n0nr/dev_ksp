#!/usr/bin env python
#
###############################################
# AUTHOR: lenonr
#
# VERSION: 0.20
#
# CREATION DATE: 21/12/18
# LAST MODIFICATION: 23/08/20
#
# DESCRIPTION: 
#   Calculate fuel for reentry of the first stage Falcon - SpaceX
#
# REFERENCE:
#   <https://www.flightclub.io/build/flightprofile>
#
# COMMENTS
#################
# LAND_Z = 0
# ADSL   = 1
#################
#
# 0(OCISLY) 			- TESS: 9,49%
#		Payload mass:  362 kg to Highly elliptical orbit
#
# 0/1(LZ1-LZ2/OCISLY) 	- Falcon Heavy: 40,01% side boosters | 19,61% central core
#		Payload mass: 1305 kg to Solar Orbit / Mars
#
# 0(LZ1)				- CRS-12: 16.32%
#		Payload mass: 1652 kg to LOW-ORBIT
#
# 0(LZ1)				- CRS-13: 16.32%
#		Payload mass: 1850 kg to LOW-ORBIT
#
# 1(OCISLY)				- Telstar 18V: 6,24%
#		Payload mass: 7050 kg to GTO
#
# 1(OCISLY)				- Telstar 19V: ????
#		Payload mass: 7060 kg to GTO
#
# 1(OCISLY)				- Bangabandu: 5,74%
#		Payload mass: 3700 kg to GTO
#
# 1(JRTI)				- SSO-A + Rideshares: 14.77%
#		Payload mass: 4000 kg to LOW-ORBIT
#
###############################################
# BODY
import os, sys, decimal
from decimal import Decimal

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

## start variables
fuel_mission = 0.0		# MAX VALUE = 418700.0
fuel_reentry = 0.0
tx_fuel_reentry = 0

def calculate(fuel_reentry, fuel_mission):
	tx_fuel_reentry = (fuel_reentry*100) / fuel_mission

	print "Landing fuel first stage:" , round(tx_fuel_reentry, 2) , "%"	

def main():
	fuel_mission = 409.500 			# change here
	fuel_reentry = 60.471 			# change here

	calculate(fuel_reentry, fuel_mission)

main()