#!/bin/bash
for DB in PILOTIT VASKI
do
  echo "Listing 336-338 fields from $DB..."
  python3 get-content-and-mediatype.py -i ${DB}_nonsub_recs.seq -o ${DB}_tyypit.txt
done
