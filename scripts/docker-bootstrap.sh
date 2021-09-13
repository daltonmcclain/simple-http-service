#/bin/bash
# Script to build and run the simple-http-service locally

SCRIPT_HOME=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_HOME

./docker-build.sh
./docker-create-dockernet.sh
./docker-start-mongo.sh
./docker-run.sh
