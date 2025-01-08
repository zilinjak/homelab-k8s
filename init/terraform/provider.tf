terraform {
  required_providers {
    argocd = {
      source = "claranet/argocd"
      version = "5.6.0-claranet0"
    }
  }
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

provider "argocd" {
  server_addr = var.argocd-server-addr
  username    = var.argocd-user
  password    = var.argocd-password
}