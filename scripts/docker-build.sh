#/bin/bash
# Script to build simple-http-service. 
# Starts in the script directory in order to grab Dockerfile in the parent directory.

SCRIPT_HOME=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_HOME/..

docker build -t simple-http-service:v1.0 .
