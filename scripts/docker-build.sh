#/bin/bash
SCRIPT_HOME=$(dirname "${BASH_SOURCE[0]}")

cd $SCRIPT_HOME/..

docker build -t simple-http-service:v1.0 .
