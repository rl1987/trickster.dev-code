#!/bin/bash

cat posts.csv | tail -n +2 | awk -F "," '{ print $2 }' | sort | uniq > users.txt 
