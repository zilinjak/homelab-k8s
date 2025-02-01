curl -sfL https://get.k3s.io > k3s.sh
chmod +x k3s.sh

./k3s.sh server \
    --disable=servicelb \
    --disable=traefik \
    --etcd-expose-metrics true \
    --kube-proxy-arg metrics-bind-address=0.0.0.0 \
    --kube-controller-manager-arg address=0.0.0.0 \
    --kube-controller-manager-arg bind-address=0.0.0.0 \
    --kube-scheduler-arg bind-address=0.0.0.0 \
    --kube-scheduler-arg address=0.0.0.0

sudo cat /etc/rancher/k3s/k3s.yaml