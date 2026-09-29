# Sonarr

Sonarr runs in `plex-media-server` and shares the existing Plex/Transmission
media PVC. Required pod affinity keeps it on Plex's node so the ReadWriteOnce
volume can be mounted by both pods. Sonarr's configuration and database use a
separate persistent `sonarr-config` PVC.

UI: http://sonarr.internal.zilinek.fun

## Connections

- TV root folder in Sonarr: `/downloads/Library/Series`.
- The same folder in Plex: `/config/Library/Series` (existing **TV Shows** library).
- Transmission host: `transmission-service.plex-media-server.svc.cluster.local`.
- Transmission port: `9091`; URL base: `/transmission/`.
- Transmission category: `sonarr`; leave the directory override empty. With the
  current Transmission download directory, Sonarr downloads go into
  `/downloads/Library/sonarr`, separate from the final `Series` library.
- Enable completed download handling and hardlinks in Sonarr. Downloads and the
  TV library share one filesystem, allowing imports without duplicating files
  while Transmission seeds. No remote path mapping is needed.
- Plex connection host: `plex-media-server.plex-media-server.svc.cluster.local`,
  port `32400`; enable library updates on import/upgrade using the existing Plex
  server token. Map paths from `/downloads` to `/config` for Plex library
  updates. Keep tokens in Sonarr's persistent configuration, out of Git.

Set up UI authentication on first visit. Add your preferred indexers and series
in Sonarr to enable automated downloads. Existing series can be added through
**Series → Library Import** without moving their files.

## Deployment

The root Argo CD application watches `apps/` on `main`. Commit and push changes
to `apps/sonarr.yaml` and this chart; Argo CD automatically syncs Sonarr with
pruning and self-healing enabled.

Validate changes before pushing:

```sh
helm lint helm/sonarr
helm template sonarr helm/sonarr --namespace plex-media-server \
  | kubectl --context homelab --namespace plex-media-server apply --dry-run=server -f -
```

Application-level connections are stored in the configuration PVC; Helm does
not overwrite them on sync.
