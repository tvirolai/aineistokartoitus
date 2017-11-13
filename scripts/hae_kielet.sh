#!/bin/bash
for DB in PIKI ANDERS PILOTIT VASKI
do
  echo "Listing languages from $DB..."
  grep ' 008  ' ../data/${DB}_nonsub.seq | cut -c54-56 > ../data/$DB-KIELET.txt
done
