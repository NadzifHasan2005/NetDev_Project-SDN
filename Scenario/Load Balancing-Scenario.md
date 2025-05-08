# Load Balancing
Load balancing merupakan suatu jaringan komputer yang menggunakan metode untuk mendistribusikan beban kerjaan pada dua atau lebih dari suatu koneksi jaringan secara seimbang agar pekerjaan dapat berjalan optimal.

Load Balancing dapat menggunakan dengan beberapa algoritma, antara lain:
- Agen Based
- Flow Based
- Round Robin

### Agen Based
Load Balancing dengan algoritma least connection menggunakan agen yang berfungsi mendistribusikan jumlah koneksi pada server.

### Flow Based
Load Balancing dengan algoritma least connection menggunakan flow yang tersimpan dijadikan sebagai parameter jumlah koneksi pada server.

### Round Robin
Load Balancing dengan algoritma round robin sebagai metode pemilihan server pada load balancing.

### Multipath Load Balancing
Sebuah metode pengaturan traffic dengan mendistribusi dan membagi muatan secara adil di antara banyak rute dari sumber ke tujuan.

---

![image](https://hackmd.io/_uploads/Sy40a8uxgg.png)

1. Setup Mininet dan Ryu dengan topologi di atas dengan ketentuan:
    - Dalam skenario khusus ini, jika Host1 ingin mengirimkan paket ke Host2, maka akan dilakukan load balancing, **70%** dari traffic S1 akan diarahkan ke port 1 dan sisa **30%** akan diarahkan ke port 2. Begitu juga sebaliknya ketika Host2 ke Host1.
    - Lalu jika Host3 ingin mengirimkan paket ke Host4, maka akan dilakukan load balancing juga, **50%** dari traffic Switch3 akan diarahkan ke port 1 dan sisa **50%** akan diarahkan ke port 2. Begi juga sebaliknya ketika Host2 ke Host1.

2. Pembuktian
    - Lakukan test iperf **Host1** ke **Host2** untuk melakukan dump paket.
    - Lakukan test iperf **Host3** ke **Host4** untuk melakukan dump paket.
    - Lakukan cek stats menggunakan **ovs-ofctl**.
