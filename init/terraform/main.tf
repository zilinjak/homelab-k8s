resource "helm_release" "argocd" {
  name = "argocd"

  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argocd"
  create_namespace = true
  version          = "3.35.4"

  values = [file("values/argocd.yaml")]
}

resource "helm_release" "root-sync-app" {
  chart            = "root-sync-app"
  name             = "root-sync-app"
  values = [file("values/sync-app.yaml")]
}