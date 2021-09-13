#/bin/bash
docker pull mongo

docker run -d --network dockernet --hostname="docker-mongo-server" -p 27017:27017 mongo
