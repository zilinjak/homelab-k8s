---
title: "Homelab - Networking"
date: 2025-03-15T12:00:00+00:00
draft: false
tags: ["kubernetes", "devops", "homelab", "networking"]
categories: ["infrastructure", "networking"]
summary: "Documentation about how I did networking in my homelab"
ShowToc: false
---

# Networking
> This is a documentation of how I did networking in my homelab. It is not a tutorial, but rather a collection of notes and links to resources that helped me along the way. I will try to keep it up to date as I learn more about networking and Kubernetes.

## Nginx Ingress Controller

### What it does
Nginx Ingress Controller allows you to expose your services using Ingress resource.

### How it works
Nginx Ingress Controller is a reverse proxy. This proxy is running in a single POD and does a lot of work. It checks for all ingresses with associated ingress class. Once Ingress with proper ingress class is found it's registered for this proxy to handle.

Each proxy has a kubernetes Service of type LoadBalancer. When any request comes to this service, the nginx will proxy the request to proper service in cluster. 

### Example

#### Create Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: ...  
spec:
  ingressClassName: nginx
  rules:
  - host: foo.com
    http:
      paths:
      - backend:
          service:
            name: foo-service
            port:
              number: 80
        path: /
        pathType: Prefix
```

This Ingress requires `nginx` ingress class to be in cluster. 

#### Acceptance by Nginx Controller
Once this Ingress is created, Nginx Ingress Controller will accept it and register it for this proxy. In the Ingress resource you will see something like this:
```yaml
spec: 
  ...
status:
  loadBalancer:
    ingress:
    - ip: 192.168.0.240
```
The IP address is the IP address of the LoadBalancer service. This is the IP address that you will use to access your service.

#### Testing the Ingress
```bash
curl -H "Host: foo.com" 192.168.0.240
```
This will send a request to the LoadBalancer service, which will be proxied to the Nginx Ingress Controller. The Nginx Ingress Controller will then proxy the request to the `foo-service` service in the cluster.

## External & Internal Traffic

### Why
Inside the cluster, we typically want to have 2/3 types of traffic:
 - Internal traffic - traffic that is only in internal network
 - External traffic - traffic that is coming from the internet
 - Cluster traffic - traffic that is coming from the cluster itself

This is important step for every cluster, since we 100% don't want to expose our internal traffic to the internet.

### How

How is pretty simple, since now we know how does Nginx Ingress Controller works. Basically we just need to setup 2 difference Ingress Controllers. Since every controller is asocciated with:
 - it's own Kubernetes Load Balancer service - has its own IP address
 - it's own Ingress class - has its own Ingress class

This allows us to create Ingresses that will be related only to one controller. The only setup we need to do inside our network, is to point external traffic ONLY to the external Ingress Controller IP address. Once it's done, you can simple create ingresses with 2 different classes:
 - `nginx-internal` - for internal traffic
 - `nginx-external` - for external traffic

Traffic should be safe and perfectly separated.