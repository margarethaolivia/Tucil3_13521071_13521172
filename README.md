# Implementasi Algoritma UCS dan A\* untuk Menentukan Linstasan Terpendek

## Deskripsi Persoalan
UCS dan A* adalah dua algoritma pencarian rute yang umum diketahui. UCS mencari jalur dengan mengambil simpul yang jaraknya dari titik mulai paling kecil sampai ditemukan simpul tujuan. Sedangkan A* menggunakan heuristik tambahan yang admissible (tidak pernah memperkirakan nilai yang lebih besar dari sebenarnya) dan mengambil simpul dengan jarak dari akar dan jarak titik tujuan (berdasarkan heuristik) yang minimum lebih dulu.

Pada tugas kali ini kami diminta untuk membuat program pencarian rute berdasarkan google map di sekitar kota Bandung. Pencarian rute dilakukan menggunakan algoritma UCS dan A*. Peta direpresentasikan dengan graf yang dibuat dalam bentuk matriks ketetanggan. Program bisa menerima simpul asal dan tujuan, lalu menentukan jalur terpendek antara kedua simpul tersebut. Jalur kemudian ditunjukkan di peta/graf. Nilai heuristik yang digunakan adalah jarak garis lurus.

## Library
Versi Python yang digunakan : 3.10.6
* OSMNX
* NetworkX
* Tkinter dan CustomTkinter
* TkinterMapView
* Matplotlib
* Scikit
* Numpy

## Usage
Buka dan jalankan file main.py. Akan muncul tampilan sebagai berikut :
![image](https://user-images.githubusercontent.com/110515021/231219600-8c7b4fb5-6d22-4dc4-807a-a902d7ae8346.png)
Tampilan di sebelah kiri berfungsi untuk visualisasi sebagai graf matplotlib biasa, sedangkan di sebelah kanan untuk pencarian jalur pada peta. Untuk visualisasi graf biasa : 
1. Klik tombol "Upload Graph" di sebelah kiri dan pilih file yang berisi matriks ketetanggaan yang diinginkan. Akan muncul graf hasil visualisasi dari matriks tersebut. 
2. Pilih simpul awal dan akhir pada bagian "Start Node" dan "End Node". 
3. Pilih algoritma pencarian yang diinginkan. 
4. Klik tombol "Search" di sebelah kiri.

Untuk mencari jalur di antara 2 titik sembarang pada peta :
1. Klik kanan pada lokasi yang diinginkan.
2. Akan muncul pilihan "Add start point" dan "Add end point". Pilih salah satu opsi tersebut.
3. Pilih algoritma yang diingkan.
4. Klik tombol "Search Path". 
5. Program akan mendownload data graf dari OpenStreetMap dan menunjukkan jalur hasil setelah pemrosesan selesai.

Untuk melakukan visualisasi matriks ketatanggan dari file : 
1. Pilih file yang diinginkan dengan klik tombol "Upload Map". 
2. Peta akan berpindah lokasi dan menunjukkan hasil visualisasi graf pada peta.
3. Pilih titik awal dan akhir dengan klik kanan (sama seperti saat mencari jalur sembarang). Pastikan titik yang dipilih paling dekat dengan simpul yang diinginkan dan tidak ada di luar bounding box yang dibentuk graf. 
4. Pilih algoritma yang diinginkan.
5. Klik tombol "Search Path".

Apabila ingin berpindah lokasi dengan cepat pada peta, ketikkan nama lokasi di kotak yang tersedia dan klik tombol "Search Location".

Contoh tampilan peta dan graf :
![image](https://user-images.githubusercontent.com/110515021/231222331-4f96c475-793f-4980-8d61-b749fd0fdc47.png)

## Author
Margaretha Olivia Haryona / 13521071

Nathan Tenka              / 13521172

