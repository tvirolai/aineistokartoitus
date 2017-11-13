#!/bin/bash
# for DB in PIKI ANDERS PILOTIT VASKI MELINDA
for DB in MELINDA
do
  echo "Listing record types from $DB..."
  grep ' FMT  ' ../data/${DB}_nonsub.seq | cut -c19- > ../data/${DB}_types.txt
done
