#!/bin/sh

if ! [ $FREQUENCY -ge 1 -a $FREQUENCY -le 60 ]; then
    echo "Error: $FREQUENCY is not an integer between 1 and 60 (inclusive)"
    exit 1
fi

sed -i -e "s/5/$FREQUENCY/g" /etc/crontabs/root
echo Successfully set script to run every $FREQUENCY minutes
