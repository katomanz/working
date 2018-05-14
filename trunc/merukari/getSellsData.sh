#!/bin/sh

# Check Parameter
if [ $# -ne 1 ]; then
  echo "Please input keyword as a parameter." 1>&2
  exit 1
fi

echo "Let's start searching!"
# Run Searching and Create result csv file
# Return value is csv file name of result
CSV_FILENAME=$(python3.6 ./sclpMerukari/merukari.py $1 2>&1 > /dev/null);
echo $CSV_FILENAME

# Upload csv file to google drive
cd dataUpload
python3.6 ./dataUpload.py $CSV_FILENAME
cd ..

echo "Let's start analysing!"
# Run Analysis and Create result csv file
# Return value is HTML file name of result
HTML_FILENAME=$(python3.6 ./analize/analize.py $CSV_FILENAME 2>&1 > /dev/null);
echo $HTML_FILENAME

# Upload html file to google drive
cd dataUpload
python3.6 ./dataUpload.py $HTML_FILENAME
cd ..

# Send notification
python3.6 notification.py $1 $CSV_FILENAME $HTML_FILENAME
