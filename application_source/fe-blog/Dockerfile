# Stage 1: Build the Hugo site
FROM --platform=$BUILDPLATFORM peaceiris/hugo:v0.145.0 AS builder

WORKDIR /src

# Copy the Hugo site files
COPY . .

# Build the Hugo site
RUN hugo

# Stage 2: Serve with Nginx
FROM nginx:latest

# Copy the built site from the builder stage
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /src/public /usr/share/nginx/html
RUN ls -la /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx when the container has started
CMD ["nginx", "-g", "daemon off;"]