# Instructions for setting up the app with Docker

## 1. Run a terminal inside a folder with Dockerfile and docker-compose.yml

First, make sure you have Docker installed on your machine and that the Dockerfile and docker-compose.yaml, which are provided, are in a directory of your choice. Run the terminal inside the said directory.

## 2. Login to your Docker account and pull images

Open Docker Desktop and run the command ***docker login*** to log into your Docker account. Once logged in, run the command ***docker-compose pull***. This will pull images from the Docker Hub onto your machine.

## 3. Build a Docker container and run it on your local machine

After pulling the images, run the command ***docker-compose up***. This will start the application and the proccess is complete


# ** NOTE: Both images are required for the application to work! Also, make sure that Dockerfile and docker-compose.yaml are in the same directory from which you are running the commands provided in this file **