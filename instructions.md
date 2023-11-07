# Instructions for setting up the app with Docker

## 1. Clone repository

***cd  git clone https://github.com/yourusername/your-hakathon-app.git***

## 2. Open Docker Web or Docker Desktop and login to your account

The Docker images have been pushed to the Docker Hub. To set up the app, you need to **pull** the images on your machine.

## 2. Pull the Docker images

To pull the images to your machine, use the following commands (In your computer terminal or Visual Studio Code):

***docker pull sveotac/mdsaas:v1.0***  to pull the application image
***docker pull sveotac/database:v1.0*** to pull the database image

**NOTE: Both images are required for the application to work!**

## 3. Run the container