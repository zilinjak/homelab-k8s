# homelab-k8s

## Description
 This project 
## Current solution 

- [x] ArgoCD
- [x] Ingress nginx controller
- [x] PiHole
- [x] Forwarded dns traffic on the router to PiHole ( secondary DNS is google - 8.8.8.8 )
- [x] PrometheusStack ( Prometheus, Grafana )
- [x] OpenVPN setup 

## In progress
- external-dns - currently only in dry mode, is supposed to sync *.internal.zilinek.fun to pihole, this needs to be finished

## To Do
- [ ] Separete ingress for *.public.zilinek.fun and *.private.zilinek.fun
- [ ] Secrets solution, possible this - https://utkuozdemir.org/blog/argocd-helm-secrets/
   - We dont want secrets in repo, currently they are there
- [ ] Fix PrometheusStack ( Alerts + Metrics from etcd, proxy, scheduler - more [here](https://github.com/k3s-io/k3s/issues/6207) and [here](https://github.com/k3s-io/k3s/issues/3619) ) 
- [ ] Add PrometheusStack ( Loki, Tempo, OtelCollector )
- [ ] LongHorn
- [ ] Documentation App - how does the infra look like
- [ ] Plex server
- [ ] More nodes?

## Apps

- [x] Ingress Cloudflare tunnel - https://github.com/STRRL/cloudflare-tunnel-ingress-controller
    - needs to be uninstalled and then added to helmchart :]
    - decided to not use it after all
- [ ] LongHorn - Storage interface
- [ ] Prometheus
- [ ] Grafana
- [ ] Loki
- [ ] Tempo
- [ ] OtelCollector
- [ ] Documentation App ( React ?)
- [ ] Plex

## Developer notes

### Ingress
Initially we wanted to use the `cloudflared` ingress controller, but after a while I have decided that I want to learn how to properly route the data via public internet, DNS and Ingress Nginx controller. Hence we are now using the `ingress-nginx` controller.
