# STAGE 1: Build
FROM node:22-alpine AS builder

# Accept build-time API URL
ARG REACT_APP_API_BASE_URL_HELLO
ARG REACT_APP_API_BASE_URL_PROFILE
ENV REACT_APP_API_BASE_URL_HELLO=$REACT_APP_API_BASE_URL_HELLO
ENV REACT_APP_API_BASE_URL_PROFILE=$REACT_APP_API_BASE_URL_PROFILE

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy the rest of the application code to the working directory
COPY . .

RUN npm run build

# STAGE 2: Serve
FROM nginx:alpine

# Install curl for healthchecks
RUN apk add --no-cache curl

# Set the working directory in the container to /usr/share/nginx/html
RUN rm -rf /usr/share/nginx/html/*

# Copy only the necessary files from the builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom Nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose
EXPOSE 80

# Build the application
CMD ["nginx", "-g", "daemon off;"]