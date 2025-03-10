# Use the official Nginx image from the Docker Hub
FROM nginx:latest

# Copy the content of the current directory to the Nginx html directory
COPY ./public /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx when the container has started
CMD ["nginx", "-g", "daemon off;"]