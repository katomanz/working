#!/bin/sh

# Check Parameter
if [ $# -ne 1 ]; then
  echo "Please input keyword as a parameter." 1>&2
  exit 1
fi

echo "Let's start searching!"
# Run Searching and Create result csv file
python merukari.py $1

# Send notification
python notification.py $1
