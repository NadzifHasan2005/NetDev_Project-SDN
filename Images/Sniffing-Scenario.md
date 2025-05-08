# Sniffing
Sniffing adalah metode penyadapan lalu lintas data pada suatu jaringan komputer. Aktivitas ini biasanya disalahgunakan oleh orang-orang yang tidak bertanggung jawab, seperti Hacker.

---

![image](https://hackmd.io/_uploads/HJMBZTYexe.png)

1. Setup Mininet dan Ryu dengan topologi di atas dengan ketentuan:
    - Dalam skenario kali ini, jika Host2 ingin mengirimkan paket ke Host1, ketika paket sampai Switch2, Switch2 akan menduplikasi paket tersebut dan melakukan forwarding ke port 3 (Hacker3).
    - Lalu jika Host1 ingin mengirim paket ke Host2, ketika paket sampai di Switch1, Switch1 akan menduplikasi paket tersebut dan melakukan forwarding ke port 3 (Hacker1) dan port 4 (Hacker2).

2. Pembuktian
    - Lakukan tes **iperf Host1 ke Host2** untuk melakukan dump paket.
    - Lakukan cek stat menggunakan **ovs-ofctl**.

