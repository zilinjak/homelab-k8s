# Jellyfin

Runs in the `plex-media-server` namespace and reads the existing Plex media volume
(`pms-config-plex-media-server-0`), so both servers see the same files during the migration.

- UI: `http://jellyfin.internal.zilinek.fun`
- The media volume is ReadWriteOnce, so a required pod affinity keeps Jellyfin on Plex's node.
- The library is mounted **read-only**; Jellyfin's database, metadata and images live in the
  separate `jellyfin-config` PVC. `/cache` (transcodes) is an emptyDir.

## Library paths

| Jellyfin library | Content type | Path in Jellyfin | Path in Plex             |
|------------------|--------------|------------------|--------------------------|
| Movies           | Movies       | `/media/movies`  | `/config/Library/Movies` |
| TV Shows         | Shows        | `/media/tv`      | `/config/Library/Series` |

## First start

1. Open the UI and finish the setup wizard (create the admin user) and add the libraries above.
2. Only after that, set `publicIngress.enabled: true` to expose `jellyfin.zilinek.cloud`.
3. Sonarr can notify Jellyfin at `http://jellyfin.plex-media-server.svc.cluster.local:8096`
   with an API key created in Dashboard -> API Keys.

## Finishing the migration

Once Plex is gone, move the media to a volume owned by Jellyfin (or have Jellyfin mount the
current PVC directly), and set `media.readOnly: false` if Jellyfin should manage files.

## Validate

```sh
helm lint helm/jellyfin
helm template jellyfin helm/jellyfin -n plex-media-server \
  | kubectl --context homelab apply --dry-run=server -f -
```
