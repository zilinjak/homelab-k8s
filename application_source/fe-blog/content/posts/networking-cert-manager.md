---
date: '2025-03-14T12:00:00+00:00'
draft: false
tags: ['kubernetes', 'homelab', 'external-dns']
categories: ['infrastructure']
title: 'Networking - HTTPS + Cert Manager'
---

> Disclaimer:
> 
> This is a documentation of how I did networking in my homelab. It is not a tutorial, but rather a collection of notes and links to resources that helped me along the way. I will try to keep it up to date as I learn more about networking and Kubernetes.

# Cert Manager

## Introduction
Cert Manager is a Kubernetes controller that automates the management and issuance of TLS certificates from various issuing sources. It can be used to obtain certificates from Let's Encrypt, HashiCorp Vault, Venafi, and other certificate authorities. The main goal of Cert Manager is to simplify the process of obtaining and renewing TLS certificates for your applications running in Kubernetes. The source code of that controller can be found [here](https://github.com/cert-manager/cert-manager)


## Why was it needed?
I wanted to expose external application to the internet. I could have done that using Nginx Ingress Controller, but I wanted to have HTTPS enabled. 
I could have done that using self-signed certificates, but I wanted to have trusted certificates.

## How does it work?
Cert Manager works by creating and managing Kubernetes resources that represent the desired state of your TLS certificates. It watches for changes in these resources and takes action to ensure that the certificates are issued, renewed, and stored correctly.
Cert Manager uses a custom resource definition (CRD) to define the desired state of the certificate. 

I'm currently using LetsEncrypt to issue the certificates. Lets Encrypt has multiple ways how to verify that I own the domain under which I want to issue the certificate. The most common way is to use HTTP-01 challenge, which requires me to create a temporary file on my web server that contains a specific token. Lets Encrypt will then try to access that file and verify that I own the domain.

#### HTTP-01 challenge
The HTTP-01 challenge is a method used by Let's Encrypt to verify that you control a domain before issuing a TLS certificate. When you request a certificate, Let's Encrypt generates a unique token and expects you to serve it at a specific URL on your domain.

In following section **CM** is **Cert Manager**.

You can imagine that the process looks like this: 
 - I create Ingress resource for my application
 - CM creates an `Certificate` CRD resource
 - When new `Certificate` resource is created
    - it contacts the ACME server (Let's Encrypt) to request a certificate for the specified domain
    - `<chalange-token>` is received by ACME server.
 - CM creates a temporary `pod` - `cm-<challenge-id>` to serve the token, with which Lets Encrypt can verify that I own that domain
 - CM updates/creates Ingress path for `/.well-known/acme-challenge/<chalange-token>` to the Ingress resource
 - Lets Encrypt sends HTTP request to `http://<domain>/.well-known/acme-challenge/<chalange-token>` to verify that I own the domain
 - Once the verification is successful, CM receives a signed certificate from Let's Encrypt

#### Cluster Issuer
A ClusterIssuer is a cluster-scoped resource that defines how to obtain certificates. It specifies the certificate authority (CA) and the configuration for obtaining certificates. For example, you can use Let's Encrypt as a CA and specify the email address for notifications and the ACME server URL.

#### Ingress + Cluster Issuer
The Ingress resource is used to define how external traffic should be routed to your services. When you create an Ingress resource, you can specify annotations that tell Cert Manager to use a specific ClusterIssuer for obtaining TLS certificates. Once this is done, the rest is handled by Cert Manager. 
