---
title: "Deployment Process"
date: 2023-12-08T19:22:33+01:00
tags: [docker, spring, react, django, start]
featured_image: ""
description: "Guide to deploy the full stack project using Docker, Django, Spring, and React."
---

# Deployment Guide

This guide outlines the steps to deploy the full stack project using Docker, Django, Spring, and React.

## Prerequisites

- Docker and Docker Compose installed.
- Python 3.11 environment for Django.
- Java 17 environment for Spring.
- Node.js environment for React (npm version 10.2.1, node version v21.4.0).

## Running the Full Project

### Basic Version (Without Monitoring)

Use `docker-compose` for a basic setup:

```bash
cd deployment/development
docker-compose up --build
```
### Full Version (With ELK, Graylog)
For a more comprehensive setup including monitoring tools:

````bash
cd deployment/production
docker compose up --build
````

## Running Individual Components
### RUN the postgres:
this part is important. If you change the user and password, make sure to change the values also in the django and spring app.
```bash
docker run  --name sus-db \
            --detach \
            --env POSTGRES_USER=sample \
            --env POSTGRES_PASSWORD=sample \
            --env POSTGRES_DB=sus-db \
            --publish 5432:5432 \
            postgres:14.2-alpine 
```

### Django Application:
#### Creating a Virtual Environment

Before setting up your Django application, it's recommended to create a virtual environment. This ensures that your project's dependencies are isolated from the global Python environment.

1. **Navigate to your project directory:**
```bash
cd data-training-app/djangoProject
```
2. **Create the virtual environment:**

For Windows:
```bash
python -m venv venv
```
For macOS and Linux:
```bash
python3 -m venv venv
```

3. **Activate the virtual environment:**

For Windows:
```bash
.\venv\Scripts\activate
```
For macOS and Linux:
```bash
source venv/bin/activate
```

4. **Install the required packages:**

For Windows:
```bash
pip install -r requirements.txt
```
For macOS and Linux:
```bash
pip3 install -r requirements.txt
```




#### First, set up the database models:
```bash
python manage.py makemigrations

python manage.py migrate
```

#### Then, run the Django server:
````bash
python manage.py runserver
````
your application will be available under [this address](http://localhost:8000)


### Spring Application 
1. Navigate into the springapp folder:
````bash
cd spring-backend
````
2. Run the maven goal
````bash
mvn spring-boot:run
````
**For your first run**

the database will still be empty, this blocks some functionality
After both Django and Spring have been initialized, you should fill the database.
Either set the __spring.sql.init.mode=neverr__ to __spring.sql.init.mode=allways__ in the application.properties for one time or fill the database directly:

````bash
docker ps -a

docker exec -it <id of the postgres container> bash

psql -d postgres -U sample
````
and copy the content of the data.sql in springs resource folder.

your application will be available under [this address](http://localhost:8080)

### React Application
1. Navigate into the frontend folder:
````bash
cd spring-backend
````
2. start the application
````bash
yarn start
````
your application will be available under [this address](http://localhost:3000)






# Stoping the deployment
### Individual Components
For single instances, use __Ctrl + C__ to stop them
 
### Docker Compose
If you used docker compose, stop all services with:
````bash
docker compose stop
````


