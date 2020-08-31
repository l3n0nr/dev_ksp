#!/usr/bin/env bash

usuario="/home/lenonr"
origem="$usuario/Github/dev_ksp/Python/kerbal/audio"
destino="$usuario/Github/dev_ksp/Python/kerbal/others/audio.txt"

echo "Audio list" > $destino
echo "=========================" >> $destino
ls "$origem" >> $destino