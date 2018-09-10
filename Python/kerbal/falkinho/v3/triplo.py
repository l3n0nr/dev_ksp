#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../../')
from base import suborbital_triplo

def main():
	turn_start_altitude     = 1000						# inclination begin
	turn_end_altitude       = 45000						# inclination end
	# target_altitude         = 1500000					# target 
	target_altitude         = 410000					# target 
	maxq_begin              = 25000						# reduce aceleration stage - begin
	maxq_end                = 70000						# reduce aceleration stage - end
	taxa_beco				= 0.16						# Landing side boosters
	taxa_meco				= taxa_beco*2				# Landing central core
	orientation				= 90						# NORMAL
	angle_ascend			= 0.5
	# angle_ascend			= 0.1

	suborbital_triplo(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa_beco, taxa_meco, orientation, angle_ascend)

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
