resource "helm_release" "argocd" {
  name = "argocd"

  chart            = "../../helm/argo-cd"
  namespace        = "argocd"
  create_namespace = true
  values          = ["${file("values/argocd.yaml")}"]
}

resource "argocd_repository" "private" {
  repo            = "git@github.com:zilinjak/homelab-k8s.git"
  username        = "argocd"
  ssh_private_key = file("./files/ssh_key")
  insecure        = true
  depends_on      = [ helm_release.argocd ]
}

resource "helm_release" "root-sync-app" {
  chart            = "../../helm/sync-app"
  name             = "root-sync-app"
  force_update     = true
  values           = ["${file("values/root-sync-app.yaml")}"]
  depends_on       = [helm_release.argocd, argocd_repository.private]
}
