# QoS (Quality of Sevice)

Quality of Service (QoS) di Kubernetes adalah sistem yang mengelola dan memprioritaskan alokasi sumber daya (CPU dan memori) di antara Pod, memastikan bahwa aplikasi penting mendapatkan sumber daya yang dibutuhkan dan sistem tetap stabil. Kubernetes membagi Pod menjadi tiga kelas QoS: Guaranteed (Dijamin), Burstable (Dapat Dilanggar), dan BestEffort (Upaya Terbaik). 

#### 1. Definisi:
QoS di Kubernetes adalah mekanisme untuk menentukan bagaimana Pod mendapatkan sumber daya, terutama CPU dan memori, dalam kondisi persaingan. 

#### 2. Kelas QoS:
Guaranteed: Pod ini memiliki permintaan dan batas sumber daya yang sama. Jika permintaan dan batas sama, Kubernetes menjamin bahwa Pod selalu mendapatkan jumlah sumber daya yang dibutuhkan. 
Burstable: Pod ini memiliki permintaan sumber daya yang lebih rendah daripada batasnya. Pod dapat menggunakan lebih banyak sumber daya jika tersedia, tetapi terbatas pada batas yang telah ditetapkan. 
BestEffort: Pod ini tidak memiliki permintaan atau batas sumber daya. Pod dapat menggunakan sumber daya yang tersedia, tetapi tidak memiliki jaminan untuk mendapatkan sumber daya yang dibutuhkan. 

#### 3. Manfaat QoS:
Jaminan Sumber Daya: QoS memastikan bahwa aplikasi penting selalu mendapatkan sumber daya yang diperlukan, bahkan dalam kondisi beban yang berat. 
Pengendalian Sumber Daya: QoS membantu mengelola sumber daya secara efektif dan mencegah satu Pod menghabiskan terlalu banyak sumber daya yang dibutuhkan oleh Pod lain. 
Penjadwalan dan Penghapusan: QoS memengaruhi bagaimana Pod dijadwalkan dan dihapus jika sistem kekurangan sumber daya. Pod dengan QoS yang lebih tinggi (seperti Guaranteed) memiliki prioritas yang lebih tinggi dalam penjadwalan dan akan dipertahankan lebih lama jika sumber daya terbatas. 

#### 4. Penggunaan:
QoS digunakan untuk menjamin kinerja aplikasi, mengelola sumber daya secara efisien, dan memastikan stabilitas sistem. 

#### 5. Pentingnya QoS:
Dalam lingkungan Kubernetes yang kompleks dengan banyak Pod dan beban kerja, QoS sangat penting untuk memastikan bahwa aplikasi dapat berjalan dengan baik dan sistem tetap stabil. 

---

![image](https://hackmd.io/_uploads/r1dEHXYgel.png)

1. Setup Mininet dan Ryu dengan topologi di atas dengan ketentuan:
    - Trafik dari Host1 ke Host3 (**VoIP**) → Diprioritaskan dengan queue berkecepatan tinggi.
    - Trafik dari Host2 ke Host4 (**HTTP**) → Diproses dengan queue berkecepatan lebih rendah.
    - Terapkan QoS dengan OVS Queue untuk memastikan VoIP mendapatkan bandwidth lebih besar dibanding HTTP.

2. Pembuktian QoS berjalan dengan benar
    - Gunakan **iperf** untuk melakukan uji trafik dan tunjukkan bahwa trafik prioritas tinggi mendapatkan bandwidth lebih besar dibanding trafik prioritas rendah.
    - Gunakan **Wireshark** untuk melihat bagaimana paket **diprioritaskan**.
    - **Bandingkan hasil pengujian dengan dan tanpa QoS.**
