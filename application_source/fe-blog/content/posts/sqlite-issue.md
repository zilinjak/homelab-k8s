---
title: "Homelab - How I managed to kill my K3S cluster with SQLite"
date: 2025-03-16T12:30:00+00:00
draft: false
tags: ["kubernetes", "devops", "homelab", "sqlite", "k3s"]
categories: ["infrastructure"]
ShowToc: false
---

# How it started

One day I have tried to use my plex instance and it was unreachable. I started digging into it. 

There were couple of containers that wouldn't start and also inspection using `k9s` CLI was taking ages.

## Started digging
I have started looking into logs, I saw couple of issues related to SQL - like `slow queries`. 

Then I remembered that K3S is using SQLite as default database, which may not be ideal, for long living clusters.

I have checked out the size of it, and oh my, it WAS HUGE! 

```bash
root@raspberrypi:/var/lib/rancher/k3s/server/db# du -hs state.db 
25G	state.db
```

## The solution

I have been googling around a bit and found out, that you can pretty easily migrate from SQLite to embedded `etcd`.
The migration is done by adding `--init-cluster` argument to k3s and then restarting it. 

How I did it?

```bash
systemctl stop k3s
vim /etc/systemd/system/k3s.service
```

I have added the `--init-cluster` argument to the `ExecStart` line, which resulted into something like this:

```text
ExecStart=/usr/local/bin/k3s \
    server \
	'--disable=servicelb' \
	'--disable=traefik' \
    '--cluster-init' \
	'--etcd-expose-metrics' \
    ...
```

Then I have restarted the server and the service:

```bash
sudo reboot
sudo systemctl start k3s
```

The start few seconds, if I compare it before, when debugging when I tried restarting the k3s instance, it was eating 4CPU cores and didnt boot to usable state after 10+ minutes. But after that the migration completed, k3s started running and all the containers were up and running.

This is the end :)