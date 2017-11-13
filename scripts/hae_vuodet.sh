#!/bin/bash
for DB in PIKI ANDERS PILOTIT VASKI
do
  echo "Listing years from $DB..."
  grep ' 008  ' ../data/${DB}_nonsub_recs.seq | cut -c19- | cut -c8-11 > ../data/$DB-VUODET.txt
done
