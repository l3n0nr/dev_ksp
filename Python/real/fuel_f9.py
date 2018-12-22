#!/usr/bin env python
#
###############################################
# AUTHOR: lenonr
#
# VERSION: 0.10
#
# CREATION DATE: 21/12/18
# LAST MODIFICATION: 21/12/18
#
# DESCRIPTION: 
#   Calculate fuel for reentry of the first stage falcon 9
#
# REFERENCE:
#   <https://www.flightclub.io/build/flightprofile>
#
# COMMENTS
#################
# ADSL = 0
# Land. Zone = 1
#################
#
# 0(OCISLY) 			- TESS: 9,49%
#		Weight:  362 kg
#
# 0/1(LZ1-LZ2/OCISLY) 	- Falcon Heavy: 40,01% side boosters | 19,61% central core
#		Weight: 1305 kg
#
# 0(LZ1)				- CRS-12: 16.32%
#		Weight: 1652 kg
#
# 0(LZ1)				- CRS-13: 16.32%
#		Weight: 1850 kg
#
# 1(OCISLY)				- Telstar 18V: 6,24%
#		Weight: 7050 kg
#
# 1(OCISLY)				- Telstar 19V: ????
#		Weight: 7060 kg
#
# 1(OCISLY)				- Bangabandu: 5,74%
#		Weight: 3700 kg
#
# 1(JRTI)				- SSO-A: 14.77%
#		Weight: 4000 kg
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