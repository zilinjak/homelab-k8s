# Use the official Nginx image from the Docker Hub
FROM nginx:latest

# Copy the content of the current directory to the Nginx html directory
RUN rm -rf /usr/share/nginx/html/*
COPY ./public /usr/share/nginx/html
RUN ls -la /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx when the container has started
CMD ["nginx", "-g", "daemon off;"]