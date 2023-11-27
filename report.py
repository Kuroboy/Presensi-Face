import MySQLdb

db = MySQLdb.connect("localhost","root","","laporan")
curs = db.cursor()

def Lapor():
    try:
        rpt = str(input("Masukan NPM:"))
        sql = "select nama, kelas, tanggal, hari, jamMasuk, jamKeluar, keterangan from t+"+rpt
        curs.execute(sql)
        result = curs.fetchall()
        print("Nama :       Kelas:      Tanggal:        Hari:       Jam Masuk:      Jam Keluar      Keterangan: ")
        for row in result:
            name = row[0]
            kelas = str(row[1])
            tgl = str(row[2])
            hari = str(row[3])
            masuk = str(row[4])
            keluar = str(row[5])
            ket = str(row[6])
            print (name+"    "+kelas+"     "+tgl+"     "+hari+"     "+masuk+"      "+keluar+"      "+ket)
    except MySQLdb.Error as e:
        print("\nPengguna belum terdaftar")