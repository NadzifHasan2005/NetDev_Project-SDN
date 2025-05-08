# Minikube 
Minikube adalah alat yang menyiapkan lingkungan **Kubernetes** di PC atau laptop lokal.
1. Update repository
    :::success
    ```
    sudo apt update && sudo apt upgrade -y
    ```
    Output:
    ![Screenshot 2025-04-30 235029](https://hackmd.io/_uploads/HycfluLgel.png)

2. Install depedensi penginstalan Docker
    ```
    sudo apt install -y curl wget apt-transport-https ca-certificates gnupg lsb-release gnupg2 software-properties-common conntrack
    ```
    Output:

3. Install Docker
    :::success
    ```
    sudo apt
        ```
    Output:
    ![Screenshot 2025-04-30 235624](https://hackmd.io/_uploads/HklMb_Ilex.png)
    Docker sebagai depedensi untuk deployment.

4. Install Containerd
    :::success
    ```
    sudo apt install -y containerd
    ```
    Output:</br>
    ![Screenshot 2025-04-30 235739](https://hackmd.io/_uploads/ry1SW_Iele.png) </br>
   
    Containerd sebagai komponen untuk menjalankan dan mengelola container dalam suatu sistem. Containerd ini yang digunakan untuk menjalankan Kubernetes, cenderung lebih cepat dibandingkan Docker dan sebagai standar untuk Kubernetes.

6. Menyalakan Containerd
    :::success
    ```
    sudo systemctl enable --now containerd
    ```
    Output:</br>
    ![Screenshot 2025-04-30 235759](https://hackmd.io/_uploads/SJEvZOUlgg.png)
</br>
# Mininet </br>
Mininet adalah sebuah aplikasi emulasi jaringan berbasis light-weight Linux virtualiation yang memungkinkan kita membuat jaringan virtual lengkap dengan switch, router, dan host yang realistis dan berinteraksi dengan real kernel dan program lainnya.


1. Instalasi Git </br>
  - Update repository 

    ```  
    sudo apt update
    ```
  - Install Github

    ```
    sudo apt install git -y
    ```
2. Cloning Mininet
```
git clone https://github.com/mininet/mininet.git
```

3. Instalasi Mininet
```
mininet/util/install.sh -a
```

4. Verivikasi mininet
```
sudo mn
```
</br>
# Ryu Controller
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
</br>
# Wireshark
Wireshark adalah salah satu program untuk menganalisa suatu jaringan, baik itu jaringan kabel maupun jaringan nirkabel. Perangkat ini diguakan untuk pemecahan masalah jaringan, analisis, perangkat lunak dan pengembangan protokol komunikasi.

1. Update dan upgrade `apt`
    ```markdown=
        sudo apt update && sudo apt upgrade
    ```
2. Install wireshark
    ```markdown=
        sudo apt install wireshark -y
    ```
3. Verifikasi wireshark
    
    ```markdown=
        wireshark
    ```

    Note :Hanya menuliskan **wireshark** pada terminal. 
    
