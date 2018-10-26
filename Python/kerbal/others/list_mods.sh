#!/usr/bin/env bash

usuario="/home/lenonr"
origem="$usuario/.steam/steamapps/common/Kerbal Space Program/GameData"
destino="$usuario/Github/dev_ksp/Python/kerbal/others/mods.txt"

echo "Kerbal Space Program mods" > $destino
echo "=========================" >> $destino
ls "$origem" >> $destino