#!/bin/sh

# Check Parameter
if [ $# -lt 1 ]; then
  echo "Please input keyword as a parameter." 1>&2
  exit 1
fi

echo "Let's start searching!"
date '+%T'
# Run Searching and Create result csv file
# Return value is csv file name of result
CSV_FILENAME=$(python3.6 ./sclpMerukari/merukari.py $1 $2 2>&1 > ./merukari.log);
echo $CSV_FILENAME

# Upload csv file to google drive
cd dataUpload
python3.6 ./dataUpload.py $CSV_FILENAME
cd ..

echo "Let's start analysing!"
date '+%T'
# Run Analysis and Create result csv file
# Return value is HTML file name of result
HTML_FILENAME=$(python3.6 ./analize/analize.py $CSV_FILENAME 2>&1 > ./analize.log);
echo $HTML_FILENAME

# Upload html file to google drive
cd dataUpload
python3.6 ./dataUpload.py $HTML_FILENAME
cd ..

# Send notification
python3.6 notification.py $1 $CSV_FILENAME $HTML_FILENAME
