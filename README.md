# simple-http-service

This is a simple service that exposes an HTTP endpoint at /manage_file. The service is written in Python 3 and uses the Flask library. The application runs on a [waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/) server. 
The endpoint accepts a JSON payload which must include one of the following:
* { "action" : "download" }
* { "action" : "read" }
The endpoint only uses the `GET` method.

### The Download Action
If the JSON payload includes { "action" : "download" }, the file at https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt will be downloaded and stored in a MongoDB database. The client receives a "Success" message when the file is successfully save to the database. 

### The Read Action
If the JSON payload includes { "action" : "read" }, the contents of the file at https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt will be returned to the client. The file contents are read from the database, so if the download action has not already been taken the server will return a 404 error stating that the entry for the url was not found. 


## Building the Service
The service is built into a Docker image with Ubuntu 20.04 as a base. In addition to the Dockerfile, this repository also includes scripts to run the `docker build`, start the built simple-http-service Docker container, and run a MongoDB Docker container.

#### Full Build and Install
./docker-bootstrap.sh

*Alternatively, the following scripts can be run individually:*
#### Build the simple-http-service Docker Image
./docker-build.sh

#### Create the `dockernet` network
./docker-create-dockernet.sh
> Note: This script should be run before starting the simple-http-service and MongoDB, since this creates the network they live on.

#### Start a MongoDB Docker Container
./docker-start-mongo.sh

#### Start the simple-http-service Docker container
./docker-run.sh


## Ansible Playbooks
This repository also includes Ansible playbooks for building and running the service from a remote node. In my testing, I built and ran the services in a Raspberry Pi 4 running Ubuntu Server. Some of these playbooks have some redundant steps if your build node and server node is the same. I wanted to run this on a Raspberry Pi, which meant I needed to build the docker image with the arm architecture. To do so, I made the Raspberry Pi both the build node and the server node. 

### Roles:
#### docker-setup
Installs docker.io and python3-docker, then sets up the docker group and the "dockernet" network that the services run in.

#### build
1. Copies the app, Dockerfile, and requirements.txt to the `build_host` defined in your ansible inventory.
2. Builds the `simple-http-service` image.

#### fetch
Saves the `simple-http-service` image and downloads it to the control node as a .tar archive. 

#### deploy
Copies the archive of the `simple-http-service` from the control node to the managed node(s), then loads the archive into the docker daemon. 

#### run-mongo
Pulls the `mongo:4.2` docker image (I had trouble with the latest version running in Docker), then runs it in the `dockernet` network. 

#### run-simple-http-service
Runs the `simple-http-service` in the `dockernet` network. 

#### stop-mongo
Stops the `mongo` container.

#### stop-service
Stops the `simple-http-service` container.

### Playbooks:
#### bootstrap.yml
Does a complete build and install using your defined `build_host` and `docker_hosts`

#### build.yml
Builds the `simple-http-service` image on the `build_host`. This is intended to be used when you want the image to be available locally.

#### build-fetch.yml
Builds the `simple-http-service` image on the `build_host`. This is intended to be used when you want to build the image on a remote build host, then save the image locally for deployment elsewhere. 

#### deploy.yml
Deploys the `simple-http-service`, assuming you have a local image .tar available. 

#### docker-setup.yml
Runs the docker-setup role. 

#### run-services.yml
Starts a `mongo` container and a `simple-http-service` container.

#### stop-services.yml
Stops currently running `mongo` container and `simple-http-service` container.

## Screenshots
> The ansible bootstrap playbook, building and deploying to a raspberry pi. 

![image](https://user-images.githubusercontent.com/8879159/133369076-49912ccb-8a54-42ab-bd44-4dcf1688abfe.png)

> The containers running in the raspberry pi.

> Interacting with the endpoint using [Postman](https://www.postman.com/)

> Invalid HTTP Method (service only accepts GET)

![image](https://user-images.githubusercontent.com/8879159/133369598-a87e72bb-7a94-42ec-a116-239b5407c2f8.png)

> No JSON in the payload

![image](https://user-images.githubusercontent.com/8879159/133369633-3a136e92-0d99-4479-b3ee-ebb39448a538.png)

> No "action" in the JSON

![image](https://user-images.githubusercontent.com/8879159/133369693-f47ffd55-70c2-4315-914b-8f2faf5742a0.png)

> Invalid "action"

![image](https://user-images.githubusercontent.com/8879159/133369728-19b50c67-6d5b-412a-affd-e780262c828a.png)

> "action" : "read" without having performed a download

![image](https://user-images.githubusercontent.com/8879159/133370046-cdd78457-3a60-4ac5-90a8-afee0dcc84f4.png)

> "action" : "download"

![image](https://user-images.githubusercontent.com/8879159/133370083-00a44c87-684c-4d56-aab1-ccd74d170baa.png)

> "action" : "read" successfully delivering the text

![image](https://user-images.githubusercontent.com/8879159/133370117-50a29e90-cf25-4d29-b89e-0886b19645db.png)

