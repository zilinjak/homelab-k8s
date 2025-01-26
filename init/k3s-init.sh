k3s server \
--etcd-expose-metrics true \
--kube-proxy-arg metrics-bind-address=0.0.0.0 \
--kube-controller-manager-arg address=0.0.0.0 \
--kube-controller-manager-arg bind-address=0.0.0.0 \
--kube-scheduler-arg bind-address=0.0.0.0 \
--kube-scheduler-arg address=0.0.0.0 \
--disable=servicelb,traefik
