#!/bin/bash
for DB in PIKI ANDERS PILOTIT VASKI
do
  echo "Extracting ids from $DB..."
  cut -c1-9 ../data/${DB}.seq | uniq > ../data/${DB}_ids.txt
done
