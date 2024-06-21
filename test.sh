#!/bin/sh

if pgrep -x "afuse" > /dev/null
then
    echo "Running"
else
    echo "Stopped"
fi

