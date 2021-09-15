#/bin/bash
# Runs the simple-http-service in the dockernet network

docker run --name simple-http-service -p 5000:5000 --network dockernet simple-http-service:v1.0
