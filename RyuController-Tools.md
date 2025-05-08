### Ryu Controller
Ryu Controller adalah pengendali jaringan berbasis perangkat lunak (SDN) terbuka yang dirancang untuk meningkatkan kelincahan jaringan dengan mempermudah pengelolaan dan penyesuaian penanganan lalu lintas.
```
#!/bin/bash

echo "[INFO] Creating ConfigMap, Deployment, and Service for Ryu..."

    cat <<EOF | kubectl apply -f -
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: ryu-app
    data:
      startup.sh: |
        #!/bin/sh

        echo "[INFO] Installing dependencies..."
        apt-get update && apt-get install -y gcc libffi-dev libssl-dev python3-venv

        echo "[INFO] Creating Python virtual environment..."
        python -m venv /tmp/venv

        echo "[INFO] Installing Python packages..."
        /tmp/venv/bin/pip install --upgrade pip==20.2.4 setuptools==57.5.0
        /tmp/venv/bin/pip install ryu eventlet==0.30.2

        echo "[INFO] Starting Ryu controller with built-in simple_switch_13..."
        exec /tmp/venv/bin/ryu-manager --observe-links --ofp-tcp-listen-port 6653 ryu.app.simple_switch_13
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ryu-controller
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: ryu
      template:
        metadata:
          labels:
            app: ryu
        spec:
          containers:
          - name: ryu
            image: python:3.9-slim
            command: ["/bin/sh"]
            args: ["-c", "/bin/sh /app/startup.sh"]
            volumeMounts:
            - name: ryu-app-volume
              mountPath: /app
              readOnly: true
            ports:
            - containerPort: 6653
            - containerPort: 6633
          volumes:
          - name: ryu-app-volume
            configMap:
              name: ryu-app
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: ryu-service
    spec:
      selector:
        app: ryu
      type: NodePort
      ports:
        - name: of-port
          protocol: TCP
          port: 6653
          targetPort: 6653
          nodePort: 30001
        - name: legacy-port
          protocol: TCP
          port: 6633
          targetPort: 6633
          nodePort: 30002
    EOF

    echo "[DONE] Deployment complete. You can check the pod logs with:"
    echo "kubectl logs -f deploy/ryu-controller"
```
