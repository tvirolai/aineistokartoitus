#!/bin/bash
for DB in PIKI ANDERS PILOTIT VASKI
#for DB in PIKI PILOTIT VASKI
do
  echo "Generating CSV report from $DB..."
  python3 batch-to-fieldtable.py -i ../data/${DB}.seq -o ../data/${DB}_fields.csv
done
