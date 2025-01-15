# homelab-k8s

## Description

### Ingress
Initially we wanted to use the `cloudflared` ingress controller, but after a while I have decided that I want to learn how to properly route the data via public internet, DNS and Ingress Nginx controller. Hence we are now using the `ingress-nginx` controller.

## Links

- [ArgoCD](http://argocd.zilinek.fun)


# TODOS

## Init 

- [x] ArgoCD
- [ ] Ingress nginx controller 
## Apps

- [x] Ingress Cloudflare tunnel - https://github.com/STRRL/cloudflare-tunnel-ingress-controller
    - needs to be uninstalled and then added to helmchart :]
    - decided to not use it after all
- [ ] Prometheus
- [ ] Grafana
- [ ] Loki
- [ ] Tempo
- [ ] OtelCollector
- [ ] Documentation App ( React ?)
