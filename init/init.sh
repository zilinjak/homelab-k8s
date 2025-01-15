#!/bin/bash

if [ -f ~/.ready ]; then
    echo "Installing and starting"
    curl -sfL https://get.k3s.io | sh -s - --disable=traefik
    echo "K3S started"

    git clone https://github.com/zilinjak/homelab-k8s && cd homelab-k8s/init/terraform
    terraform init
    terraform apply -auto-approve

    exit 0
fi

echo "Updating and upgrading the system"
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y gnupg software-properties-common
 
# Terraform install - https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
 
wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null

gpg --no-default-keyring \
--keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
--fingerprint

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update

sudo apt-get install terraform 

echo "Setting cgroups"
echo "cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory" >>  /boot/firmware/cmdline.txt

echo "Reboot now"
echo "" >> ~/.ready
sudo reboot

