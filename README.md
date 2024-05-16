# Simulationsumgebung Multimodale Daten

## Overview

We are using Maven as our project management tool, and we're adhering to the standard directory layout. That means that our backend application sources and resources are located in the `src` directory, the `target` directory contains all build output files. The Frontend sources are located in the `frontend` directory.
The `frontend-maven-plugin` is used to create a production build of the frontend whenever the backend is built, which enables us to package the frontend and backend together in a single jar file. This is possible because the npm build creates a static bundle which can be served by the Spring Servlet. Please note that this is only useful for a standalone build and not for development purposes.

## Building

A single jar file containing both the frontend and backend can be created by running the `clean package` goals. The jar file is placed in the `target` directory.

## Development

### Frontend

The frontend development build can be launched by running `npm start` in the `frontend` directory.

### Backend

The backend can be spun up for development by running the `spring-boot:run -Dskip.npm` goal. The additional parameter is used to skip the frontend build.

### Postgres

To set up the database, install docker and run: 
```shell
docker run  --name simulationsDB \
            --detach \
            --env POSTGRES_USER=sample \
            --env POSTGRES_PASSWORD=sample \
            --env POSTGRES_DB=simulationsDB \
            --publish 5432:5432 \
            postgres:14.2-alpine 
```

### Swagger-UI
http://localhost:8080/swagger-ui/index.html

### Prometheus metrics
http://localhost:8080/actuator/prometheus

## Deployment

The whole simulation environment can be deployed using the docker compose script in the `deployment/production` directory. It contains the developed application itself (frontend and backend in a single container) along with a postgres database for persistent data storage and a kafka broker as middleware between our application and the different data consumers. The compose scripts builds the image for our application from the jar file generated during the build process. For this reason, the application needs to be built once before the docker compose deployment can be used. Create the necessary jar file by running `mvn clean package` in the root directory. Optionally, the parameter `-DskipTests=true` can be used to skip test execution in the build process.

If you need to update the generated docker image (for example when new features or bugfixes have been added to the app), create the updated jar file through the build process outlined above and run `docker compose build` in the `deployment/production` directory. Docker might also just update the image automatically depending on its configuration when you run `docker compose up -d`.

With the default configuration, the web interface will be available on `localhost:8080` and the kafka broker will be accessible on `localhost:9092`.