---
title: "Networking - Nginx Ingress Controller"
date: 2025-03-15T12:00:00+00:00
draft: false
tags: ["kubernetes", "devops", "homelab", "networking"]
categories: ["infrastructure", "networking"]
summary: "Nginx Ingress Controller and k8s routing"
ShowToc: false
---

> Disclaimer:
> 
> This is a documentation of how I did networking in my homelab. It is not a tutorial, but rather a collection of notes and links to resources that helped me along the way. I will try to keep it up to date as I learn more about networking and Kubernetes.

# Nginx Ingress Controller

### What it does
Nginx Ingress Controller allows you to expose your services using Ingress resource.

### How it works
The Nginx Ingress Controller acts as a reverse proxy running in a pod. It:
1. Monitors for Ingress resources with its associated ingress class
2. Configures the Nginx proxy when it finds a matching Ingress
3. Routes traffic to the appropriate services

Each controller has a Kubernetes Service of type `LoadBalancer`. When requests arrive at this service, Nginx proxies them to the correct service within the cluster.
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

---

## External & Internal Traffic

### Important Pre-requisite
Before implementing this separation, ensure your Kubernetes cluster supports multiple LoadBalancer Services with distinct IP addresses. 

#### K3S Consideration (ServiceLB Limitation)
K3S comes with `ServiceLB` (formerly called Klipper Load Balancer) which has a significant limitation:
- Only supports **one** LoadBalancer Service
- Assigns the **same IP address** to all LoadBalancer Services

This becomes problematic when trying to run:
```bash
1 External Nginx Ingress Controller (requires LoadBalancer)
1 Internal Nginx Ingress Controller (requires LoadBalancer)
```
Both will get the same IP address, defeating the purpose of separation. Or only one will start since the other will not have working LoadBalancer service.

#### K3S Setup

1. Install K3s with
```
curl -sfL https://get.k3s.io | sh -s - --disable servicelb
```
2. Install MetalLB, see [SyncApp](https://github.com/zilinjak/homelab-k8s/blob/main/apps/metal-lb.yaml) and [Helm](https://github.com/zilinjak/homelab-k8s/tree/main/helm/metallb)

### Why its needed
Inside the cluster, we typically want to have 2/3 types of traffic:
 - Internal traffic - traffic that is only in internal network
 - External traffic - traffic that is coming from the internet
 - Cluster traffic - traffic that is coming from the cluster itself

This is important step for every cluster, since we 100% don't want to expose our internal traffic to the internet.

### How it's done

Since we understand how the Nginx Ingress Controller works, we can implement separation by:

Deploying two separate Ingress Controllers

Each controller has:
- Its own Kubernetes LoadBalancer service (different IP)
- Its own ingress class identifier

This allows us to create Ingresses that will be related only to one controller. The only setup we need to do inside our network, is to point external traffic ONLY to the external Ingress Controller IP address. Once it's done, you can simple create ingresses with 2 different classes:
 - `nginx-internal` - for internal traffic
 - `nginx-external` - for external traffic

Traffic should be safe and perfectly separated.