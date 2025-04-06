---
date: '2025-03-14T12:00:00+00:00'
draft: false
tags: ['kubernetes', 'homelab', 'external-dns']
categories: ['infrastructure']
title: 'Networking - External DNS + Pihole'
---

> Disclaimer:
> 
> This is a documentation of how I did networking in my homelab. It is not a tutorial, but rather a collection of notes and links to resources that helped me along the way. I will try to keep it up to date as I learn more about networking and Kubernetes.

# External DNS

## Introduction

External DNS is a Kubernetes controller that manages DNS records dynamically. It automates the process of creating and updating DNS records in external DNS providers based on the services and ingress resources in your Kubernetes cluster. Source code can be found [here](https://github.com/kubernetes-sigs/external-dns). 

## Why was it needed?

When Ingress resources are created in Kubernetes, they typically have a hostname associated with them. This hostname isn't registered in any DNS provider by default. Ingress controller (as described [here](/posts/networking-nginx-controllers/)) doesn't handle the DNS records, it uses only `HOSTNAME` header in the request to route traffic to the correct service.

This means that the hostname must be registered automatically when the Ingress resource is created. Here comes the External DNS. It watches for changes in the Ingress resources and automatically creates or updates the corresponding DNS records in the external DNS provider.

## How does it work?

### Providers

External DNS needs to be configured to work with something called **Provider**. **Provider** is configuration that tells External DNS how to handle the creation/deletion of DNS records.

Example of providers:
 - AWS Route53
 - Google Cloud DNS
 - CloudFlare
 - PiHole

Many more... newly released Providers are in separate repository, see [this](https://github.com/kubernetes-sigs/external-dns?tab=readme-ov-file#new-providers)

### PiHole + External DNS

#### Pihole
When you want to have custom DNS records in your own local network, you need to host your own DNS server. When I was doing some research about what DNS server to use, I found out about awesome project - [PiHole](https://pi-hole.net/). Pihole is a DNS server and in addition to that, it acts as an adblocker. The adblocking is done on the DNS level, this means that the hostnames that are known to be serving adds disabled and the DNS server wont resolve them. I thought that this feature is pretty cool and is nice addition the the DNS server. 

#### External DNS + Pihole
External DNS can be configured to work with Pihole. The configuration is pretty simple. Deploy Pihole - see [this](https://github.com/zilinjak/homelab-k8s/blob/main/apps/pihole.yaml)
and then deploy External DNS with the following configuration:
```yaml
- --source=ingress
- --registry=noop
- --policy=sync
- --provider=pihole # specify the provider
- --pihole-server={{ .Values.piholeServer }} # specify the pihole server
- --domain-filter={{ .Values.domainFilter }} # specify the domain filter
- --log-level={{ .Values.logLevel }} # specify the log level
- --log-format=text
- --interval={{ .Values.interval }} # specify the interval how often does the external-dns check for changes
```

- **pihole-server** -> important to set as for example 'http://pihole-web.pihole.svc.cluster.local'. This avoids the chicken and egg problem, where the external-dns needs to resolve the pihole server before it can create the DNS record for the pihole server itself. This means that the communication between external-dns and pihole is done over the internal network, the dns for the service is stored in kubernetes internal DNS - see [CoreDNS](https://kubernetes.io/docs/tasks/administer-cluster/coredns/).

- **domain-filter** -> this is the domain that you want to use for your services. For example, if you want to use `foo.com` as the domain for your services, you need to set this to `foo.com`. This means that the external-dns will only create DNS records for the services that have this domain in their Ingress resource. For example `bar.foo.com` will be created, but `bar.com` will NOT be created.