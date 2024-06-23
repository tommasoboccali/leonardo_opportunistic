#!/bin/sh

# if afuse not running, start it
if pgrep -x "afuse" > /dev/null
then
    echo "Running"
else
    echo "Stopped"
fi


#if still no CVMFS, find it
if ls /cvmfs/cms.cern.ch ; then
    echo "Command succeeded"
else
    echo "Command failed"
fi

