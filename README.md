# simple-http-service

This is a simple service that exposes an HTTP endpoint at /manage_file. The service is written in Python 3 and uses the Flask library.
The endpoint accepts a JSON payload which must include one of the following:
* { "action" : "download" }
* { "action" : "read" }
The endpoint only uses the `GET` method.

### The Download Action
If the JSON payload includes { "action" : "download" }, the file at https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt will be downloaded and stored in a MongoDB database. The client receives a "Success" message when the file is successfully save to the database. 

### The Read Action
If the JSON payload includes { "action" : "read" }, the contents of the file at https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt will be returned to the client. The file contents are read from the database, so if the download action has not already been taken the server will return a 404 error stating that the entry for the url was not found. 


## Building the Service
The service is built into a Docker image with Ubuntu 20.04 as a base. In addition to the Dockerfile, this repository also includes scripts to run the `docker build`, start the built http-service Docker container, and run a MongoDB Docker container.

#### Build the HTTP-Service Docker Image
./docker-build.sh

#### Start a MongoDB Docker Container
./docker-start-mongo.sh
> Note: This script should be run before starting the HTTP-Service, since it also creates a Docker network (dockernet) for the service and the database to exist on. 

#### Run an HTTP-Service Docker Container
./docker-run.sh

## Ansible Playbooks
This repository also includes Ansible playbooks for building and running the service from a remote node. In my testing, I built and ran the services in a Raspberry Pi 4 running Ubuntu Server. 

#### docker-setup.ylm
Installs docker.io and python3-docker, then sets up the docker group and the "dockernet" network that the services run in.

#### build-and-save.yml
1. Copies the app, Dockerfile, and requirements.txt to the `build_host` defined in your ansible inventory.
2. Builds the `simple-http-service` image.
3. Saves the `simple-http-service` image and downloads it to the control node. 

#### load.yml
Copies the archive of the `simple-http-service` from the control node to the managed node(s), then loads the archive into the docker daemon. 

#### run-mongo.yml
Pulls the `mongo:4.2` docker image (I had trouble with the latest version running in Docker), then runs it in the `dockernet` network. 

#### run-simple-http-service.yml
Runs the `simple-http-service` in the `dockernet` network. 
