#!/bin/bash

start_time="1448841600";
stop_time="1448842200";

for i in {1..144}; do

  echo "$i $start_time $stop_time";
  ./download.sh $start_time $stop_time;

  start_time=`echo "$start_time" | awk '{print $1+600;}'`;
  stop_time=`echo "$stop_time" | awk '{print $1+600;}'`;

done;


