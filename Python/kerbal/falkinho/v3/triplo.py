#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../../')
from base import suborbital_triplo

def main():
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	target_altitude         = 3000000					# target 
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = turn_end_altitude			# reduce aceleration stage - end
	taxa					= 0.20						# Landing first stage in %(Taxa/100)
	orientation				= 90						# NORMAL

	suborbital_triplo(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, orientation)

main()

# comentarios
# verificar BECO
# verificar MECO
# verificar SES-1

## PROVA REAL - 0.20 DE TAXA
# quantidade de combustivel em um core
# 12 * 1440 = 17280*0.20 		  = 3456
#
# quantidade de combustivel, nos tres boosters
# 36 * 1440 = 51840*0.20   		  = 1036800
#
# quantidade de tanques(3 boosters) restantes - BECO/MECO
# 10368 / 1440  = 7,2 / 3 		  = 2,4 tanques
# 10368 / 3		= 3456			  = unidades
#
# total de combustivel(3 boosters)
# 2 tanques cheios + 576 unidades = 1 booster
# 2 tanques cheios + 576 unidades = 1 core
# 2 tanques cheios + 576 unidades = 1 booster
# 
# valor n codigo(srb_tx) 	 	  = 10368.0
