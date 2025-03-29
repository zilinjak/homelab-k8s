---
title: "Homelab"
date: 2025-03-16T12:00:00+00:00
draft: false
tags: ["kubernetes", "devops", "homelab"]
categories: ["infrastructure"]
summary: "Documentation of my Kubernetes homelab journey"
ShowToc: false
---

## Before It Started...

When I began working as a DevOps engineer at Košík.cz, I started using Kubernetes daily for the first time. I quickly realized I had basically no clue how it worked or how to properly manage it. After reading many blogs and exploring Kubernetes for about a year, I noticed much of the setup had been done by my colleagues. 

I decided to buy a **Raspberry Pi 5 8GB** and start my own homelab where I would set up an entire Kubernetes cluster myself. My goal was to gain fundamental knowledge about core components of cloud computing.

---

## Homelab Progress Checklist

| Category                                                   | Task                                       | Status |
|-------------------|-------------------------------------------------------------------------------------|--------|
| [**Networking**](/posts/homelab-networking/#networking)    | LoadBalancer setup on bare metal           | ✅     |
| [**Networking**](/posts/homelab-networking/#networking)    | Configure Ingress for internet traffic     | ✅     |
| [**Networking**](/posts/homelab-networking/#networking)    | TLS certificates management (HTTPS setup)  | ✅     |
| [**Networking**](/posts/homelab-networking/#networking)    | Internal vs External traffic configuration | ✅     |
| [**Networking**](/posts/homelab-networking/#networking)    | VPN setup                                  | ✅     |
| [**Networking**](/posts/homelab-networking/#networking)    | CertManager implementation                 | ✅     |
| [**Networking**](/posts/homelab-networking/#networking)    | Make this website Google indexed           | ✅     |
| **Observability** | Grafana & Prometheus monitoring                                              | ❌     |
| **Observability** | Loki & Tempo logging/tracing                                                 | ❌     |
| **Observability** | OpenTelemetry Collector                                                      | ❌     |
| **Observability** | Cluster log scraping                                                         | ❌     |
| **ArgoCD**       | Installation script                                                           | ✅     |
| **ArgoCD**       | App synchronization for cluster bootstrapping                                 | ✅     |
| **ArgoCD**       | Projects deep dive                                                            | ❌     |
| **Cluster**      | Add additional nodes                                                          | ❌     |
| **Cluster**      | Dedicated master for core services                                            | ❌     |
| **Cluster**      | Storage vs non-storage nodes configuration                                    | ❌     |
| **Security**     | Secrets management with ArgoCD + Kubernetes                                   | ✅     |
| **Security**     | Network security (Firewall, VPN, etc.)                                        | ❌     |
| **Projects**     | Plex media server                                                             | ✅     |
| **Projects**     | Torrent server                                                                | ✅     |
| **Projects**     | PiHole + DNS configuration                                                    | ✅     |
| **Projects**     | Longhorn storage system                                                       | ✅     |
| **Projects**     | Longhorn multi-node deep dive                                                 | ❌     |
| **Projects**     | Documentation application                                                     | ❌     |
| **Projects**     | Cloud K6 load testing                                                         | ❌     |
| **Projects**     | Performance benchmarks 📈                                                     | ❌     |

---

> Many more to be added as the homelab evolves...