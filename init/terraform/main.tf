resource "helm_release" "argocd" {
  name = "argocd"

  chart            = "../../helm/argo-cd"
  namespace        = "argocd"
  create_namespace = true
  values          = ["${file("values/argocd.yaml")}"]
}

resource "helm_release" "root-sync-app" {
  chart            = "../../helm/sync-app"
  name             = "root-sync-app"
  values           = ["${file("values/root-sync-app.yaml")}"]
  depends_on       = [helm_release.argocd]
}

# TODO: Add ssh key to access the repo