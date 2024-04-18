# Program Restaurant menggunakan Service Layer Pattern  


Petunjuk menjalankan program:
1. Buka command prompt(windows) atau terminal(mac)
2. Buka file sampai berada di file service-layered-pattern-elreda yaitu cd nama_file
3. Lalu jalankan perintah  python -m elreda -dbinit=True -dburl="elreda.db"
4. Untuk menjalankan pytest dengan perintah pytest tests
Contoh di command prompt:
C:\Users\gilbe\Desktop\UAS_OOP\service-layered-pattern-elreda>python -m elreda -dbinit=True -dburl="elreda.db"


Fitur yang ada:
1. Jika ada >5 order di Kitchentab, maka ada tulisan Kitchen is Busy (remind guest!!)
2. Jika ada order baru, maka ada pop up email dan print text
3. Jika sebuah menu makanan diorder >= 20, maka akan ada print membeli bahan makanan.

Versi 2
4. Jika ada order baru, maka ada print "TinggTongg... Ada pesanan masuk!"


Disclaimer:
Perintah juga dapat dengan perintah "python -m elreda"
dbInit belum dapat melakukan dummy dan pengahapusan semua data
dburl, dbUrl juga belum dapat memasukan database dan filedatabase
