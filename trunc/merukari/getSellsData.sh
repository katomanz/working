#!/bin/sh

# Check Parameter
if [ $# -ne 1 ]; then
  echo "Please input keyword as a parameter." 1>&2
  exit 1
fi

echo "Let's start searching!"
# Run Searching and Create result csv file
python3.6 ./sclpMerukari/merukari.py $1

# Upload to google drive
cd dataUpload
python ./dataUpload.py $1
cd ..

# Send notification
python notification.py $1
