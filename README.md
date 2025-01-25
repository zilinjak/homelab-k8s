# homelab-k8s
I have decided to create a homelab, mainly to improve my skills in k8s and knowledge Im missing. Main reason is that I want to learn stuff that is being done by my colleagues at work (Yes, Im DevOps Engineer). I want to learn about whole infrastructure, how to manage it, what each component does and how do they work. I know that I will never understand everything and more I know means that I know that I dont know much (hope that makes sence), but lets give it a try and see how far I can get.

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
- [ ] HTTPS Certs
- [ ] LongHorn
- [ ] Add PrometheusStack ( Loki, Tempo, OtelCollector )
- [ ] Documentation App - how does the infra look like
- [ ] Plex server
- [ ] More nodes?

## Developer notes

### Ingress
Initially we wanted to use the `cloudflared` ingress controller, but after a while I have decided that I want to learn how to properly route the data via public internet, DNS and Ingress Nginx controller. Hence we are now using the `ingress-nginx` controller.
