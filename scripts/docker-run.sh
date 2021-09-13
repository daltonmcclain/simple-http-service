#/bin/bash
# Runs the simple-http-service in the dockernet network

docker run -p 5000:5000 --network dockernet simple-http-service:v1.0
