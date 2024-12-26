# Initialize Kubernetes Cluster with all the required components
After nitializing the of the k8s, the cluster will contain the following components:
 - ArgoCD installation
 - ArgoCD application
## Prerequisites
...

## Install K8S / K3S
...

## Terraform

1. Install terraform
2. Check that correct cluster is selected -> `kubectl config get-contexts` and `kubectl config use-context <context-name>`
2. Run `terraform init`
3. Run `terraform plan` and `terraform apply`
