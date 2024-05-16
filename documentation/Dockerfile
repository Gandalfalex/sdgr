FROM ubuntu:latest as build

ARG HUGO_VERSION="0.121.0"
RUN apt-get update -y && apt-get install -y wget

COPY install_hugo.sh .
RUN ls -la
RUN chmod +x install_hugo.sh && ./install_hugo.sh

WORKDIR /src
COPY docs/ /src
RUN hugo --baseURL="http://host.docker.internal/docs/" --environment production


FROM nginx:alpine
COPY default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/public /usr/share/nginx/html

EXPOSE 1313
