---
title: "Networking - MetalLB"
date: 2025-03-15T12:00:00+00:00
draft: false
tags: ["kubernetes", "devops", "homelab", "networking"]
categories: ["infrastructure", "networking"]
summary: "Take a look at K3S and MetalLB"
ShowToc: false
---

> Disclaimer:
> 
> This is a documentation of how I did networking in my homelab. It is not a tutorial, but rather a collection of notes and links to resources that helped me along the way. I will try to keep it up to date as I learn more about networking and Kubernetes.

# MetalLB

## Why was it needed?

This was already descibed in the Nginx Controller post, feel free to read it [here](/posts/networking-nginx-controllers). Basically without ability to create multiple LoadBalancer services, I wasn't able to create multiple Nginx Ingress Controllers. This was needed for my homelab setup, because I wanted to have one controller for internal traffic and one for external traffic.

## How does it work?

MetalLB provides LoadBalancer IPs for bare-metal Kubernetes clusters. It consists of two main components:

**Controller** – Assigns IPs to services.
**Speaker** – Advertises IPs using ARP (Layer 2) or BGP.

These components are deployed as pods in the cluster.

#### Controller: The IP Allocator
Watches for LoadBalancer services. Assigns an available IP from a configured pool, updates the service’s .status.loadBalancer.ingress.ip.

#### Speaker: The IP Advertiser

- Runs as a DaemonSet (one pod per node).
- In Layer 2 mode, one node responds to ARP requests for the assigned IP.
- If the node fails, another Speaker takes over (failover).

##### About ARP

A device on the network asks, "Who has IP 192.168.1.100?" (ARP request).
The elected Speaker responds, "I do! My MAC is XX:XX:XX:XX:XX."
Traffic for 192.168.1.100 flows to that node, then to the service.
