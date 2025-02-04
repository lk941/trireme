# Stage 1: Build Angular App
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /frontend

# Copy package.json and package-lock.json into the container
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the Angular project files into the container
COPY . .

# Build the Angular app
RUN npm run build --prod

# Verify the build output (debugging step)
RUN ls -l /frontend/dist

# Stage 2: Serve the Angular App with NGINX
FROM nginx:stable-alpine

# Copy built Angular app from the previous stage
COPY --from=build /frontend/dist/frontend /usr/share/nginx/html

# Replace default NGINX configuration with custom one
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Verify the NGINX configuration (debugging step)
RUN cat /etc/nginx/conf.d/default.conf

# Verify the copied files (debugging step)
RUN ls -l /usr/share/nginx/html

# Expose the default NGINX port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]