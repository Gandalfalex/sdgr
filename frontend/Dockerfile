# Stage 1: Build the React application
FROM node:latest AS build

WORKDIR /app

COPY package.json package-lock.json yarn.lock ./
RUN npm install
RUN npm install react-scripts@5.0.1 -g
COPY . ./

RUN npm run build

# stage 2, build the nginx container
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]