#/bin/bash
# Downloads mongo:4.2 and runs a mongo database in the dockernet network.
# The container is given the "docker-mongo-server" hostname so that the simple-http-service can find it

docker pull mongo:4.2

docker run --name mongo -d --network dockernet --hostname="docker-mongo-server" -p 27017:27017 mongo
