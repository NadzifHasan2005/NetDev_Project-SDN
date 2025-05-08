### 2. Minikube 
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
