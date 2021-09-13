#/bin/bash
docker run -p 5000:5000 --network dockernet simple-http-service:v1.0
