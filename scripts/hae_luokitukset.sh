#!/bin/bash
for DB in PIKI ANDERS PILOTIT VASKI
do
  echo "Extracting classifications from $DB..."
  grep ' 084  ' ../data/${DB}_nonsub.seq | cut -c19- | cut -c4- | cut -d '$' -f 1 > ../data/${DB}-LUOKITUKSET.txt
done
