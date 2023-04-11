# Implementasi Algoritma UCS dan A\* untuk Menentukan Linstasan Terpendek

## Deskripsi Persoalan
UCS dan A* adalah dua algoritma pencarian rute yang umum diketahui. UCS mencari jalur dengan mengambil simpul yang jaraknya dari titik mulai paling kecil sampai ditemukan simpul tujuan. Sedangkan A* menggunakan heuristik tambahan yang admissible (tidak pernah memperkirakan nilai yang lebih besar dari sebenarnya) dan mengambil simpul dengan jarak dari akar dan jarak titik tujuan (berdasarkan heuristik) yang minimum lebih dulu.

Pada tugas kali ini kami diminta untuk membuat program pencarian rute berdasarkan google map di sekitar kota Bandung. Pencarian rute dilakukan menggunakan algoritma UCS dan A*. Peta direpresentasikan dengan graf yang dibuat dalam bentuk matriks ketetanggan. Program bisa menerima simpul asal dan tujuan, lalu menentukan jalur terpendek antara kedua simpul tersebut. Jalur kemudian ditunjukkan di peta/graf. Nilai heuristik yang digunakan adalah jarak garis lurus.

## Library yang diperlukan
Versi Python yang digunakan : 3.10.6 dan ...
* OSMNX
* NetworkX
* Tkinter dan CustomTkinter
* TkinterMapView
* Matplotlib
* Scikit
* Numpy

## Cara Menjalankan Program
Buka file main.py dan langsung jalankan. Akan muncul tampilan sebagai berikut :
![image](https://user-images.githubusercontent.com/110515021/231219600-8c7b4fb5-6d22-4dc4-807a-a902d7ae8346.png)
Tampilan di sebelah kiri berfungsi untuk visualisasi sebagai graf matplotlib biasa, sedangkan di sebelah kanan untuk pencarian jalur pada peta. Untuk visualisasi graf biasa, klik tombol "Upload Graph" di sebelah kiri dan pilih file yang berisi matriks ketetanggaan yang diinginkan. Akan muncul graf hasil visualisasi dari matriks tersebut. Berikutnya, pilih simpul awal dan akhir pada bagian "Start Node" dan "End Node". Untuk mencari jalur di antara kedua simpul tersebut, pilih algoritma pencarian yang diinginkan lalu klik tombol "Search" di sebelah kiri.

Pada tampilan peta, untuk memilih titik mulai dan akhir, klik kanan pada lokasi yang diinginkan. Akan muncul pilihan "Add start point" dan "Add end point". Pilih salah satu opsi tersebut. Setelah memilih titik mulai dan tujuan, pilih algoritma yang diingkan lalu klik tombol "Search Path". Program akan mendownload data graf dari OpenStreetMap dan menunjukkan jalur hasil setelah pemrosesan selesai.

Pada tampilan peta juga bisa dilakukan visualisasi matriks ketatanggan dari file. Pilih file yang diinginkan dengan mengklik tombol "Upload Map". Peta akan berpindah lokasi dan menunjukkan hasil visualisasi graf pada peta. Cara memilih titik awal dan akhir masih sama. Pastikan titik yang dipilih paling dekat dengan simpul yang diinginkan dan tidak ada di luar bounding box yang dibentuk graf. Untuk mencari jalur, pilih algoritma yang diinginkan dan klik tombol "Search Path".

Apabila ingin berpindah lokasi dengan cepat pada peta, ketikkan nama lokasi di kotak yang tersedia dan klik tombol "Search Location".

Contoh tampilan peta dan graf :
![image](https://user-images.githubusercontent.com/110515021/231222331-4f96c475-793f-4980-8d61-b749fd0fdc47.png)

