# Stage 1: Build the React application
FROM node:latest AS build

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install
COPY . ./
RUN yarn build

# stage 2, build the nginx container
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY default.conf /etc/nginx/conf.d/

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]