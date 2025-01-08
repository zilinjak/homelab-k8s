variable "argocd-user" {
  type        = string
  description = "ArgoCD username"
  sensitive   = true
}

variable "argocd-password" {
  type        = string
  description = "ArgoCD password"
  sensitive   = true
}

variable "argocd-server-addr" {
  type        = string
  description = "ArgoCD server address"
}