#!/bin/bash

#start_time="1448841600";
#stop_time="1448842200";


start_time="1448860800";
stop_time="1448861400";

for i in {1..110}; do
#for i in {1..144}; do

  echo "$i $start_time $stop_time";
  ./new-download.sh $start_time $stop_time;

  start_time=`echo "$start_time" | awk '{print $1+600;}'`;
  stop_time=`echo "$stop_time" | awk '{print $1+600;}'`;

done;


