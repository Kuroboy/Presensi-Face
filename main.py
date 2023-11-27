import IoU
import report
import cekPin
import faceRec
import time
import datetime
import signal
import sys
import MySQLdb

db = MySQLdb.connect("localhost","root","","laporan")
curs = db.cursor()
now = datetime.datetime.now()

def getMode():
    print("\nPilih Mode yang ingin dilakukan")
    print(""""Mode :
    absen
    daftar/update
    (input lowcase)\n""")
    mode = str(input("Mode : "))
    if mode == "absen" :
        mode = str(input("""Absen(Masuk/Keluar) : """))
        if mode == 'masuk' or mode == 'keluar':
            return mode
        else:
            return 'salah'
    elif mode == 'daftar' or mode == 'update':
        return mode
    else:
        return "salah"

def satuMinggu(day):
    if day == '0':
        return 'Minggu'
    elif day == '1':
        return 'Senin'
    elif day == '2':
        return 'Selasa'
    elif day == '3':
        return 'Rabu'
    elif day == '4':
        return 'Kamis'
    elif day == '5':
        return 'Jumat'
    else:
        return 'Sabtu'

def signal_handler(signal,frame):
    global lanjut
    print("\nCTRL+C capture, ending read")
    sys.exit(0)
    lanjut = False

print ("Selamat Datang")
time.sleep(2)
signal.signal(signal.SIGINT, signal_handler)
while(True):
    mode = getMode()
    if mode == "daftar" or mode == "update":
        IoU.action()
        mode == "Salah"
    elif mode == "masuk":
        try:
            (npmPin, namaPin) = cekPin.getPIN()
            print("""Tunggu Kamera menyala...
            \nDeteksi wajah Dalam 3 detk""")
            time.sleep(3)
            print("\nHarap Tunggu....")
            (npmFace, namaFace) = faceRec.getFace_info()
            day = now.strftime("%w")
            hari = satuMinggu(day)
            if(namaPin == namaFace and npmPin == npmFace):
                curs.execute("insert into T_"+npmPin+"(tanggal,Hari,jamMasuk) values (CURDATE(), '"+hari+"',CURTIME())")
                db.commit()
            else:
                print("Wajah dan Data Anda tidak ditemukan, coba lagi")
        except TypeError:
            print("\nData Tidak ditemukan")
    elif mode == "keluar":
            day = now.strftime("%w")
            hari = satuMinggu(day)
            (npmPin, namaPin) = cekPin.getPIN()
            curs.execute("SELECT *FROM T_"+npmPin+" WHERE jamKeluar is NULL and jamMasuk is NOT NULL and keterangan is NULL and Hari = '"+hari+"' order by nomor desc limit 1")
            status = 0
            for row in curs:
                status = 1
            if status == 1:
                print("Mendeteksi wajah dalam 3 detik")
                time.sleep(3)
                (npmFace, namaFace) = faceRec.getFace_info()
                print("\nSedang Memproses...")
                if (namaPin == namaFace and npmPin == npmFace):
                    curs.execute("update T_"+npmPin+" set jamKeluar = CURTIME() Where jamKeluar is NULL and jamMAsuk is NOT NULL and hari = '"+hari+"' order by nomor desc limit 1")
                    db.commit()
                    print("\n selesai \n")
            else:
                print("\nAnda blm masuk\n")
            sql = "select nama, kelas, tanggal, hari, jamMasuk, jamKeluar, keterangan from t_"+npmPin
            curs.execute(sql)
            result = curs.fetchall()
            print("""==================================================================================================
            \nNama :       Kelas:      Tanggal:        Hari:       Jam Masuk:      Jam Keluar      Keterangan: """)
            for row in result:
                name = row[0]
                kelas = str(row[1])
                tgl = str(row[2])
                hari = str(row[3])
                masuk = str(row[4])
                keluar = str(row[5])
                ket = str(row[6])
                print(name + "    " + kelas + "     " + tgl + "     " + hari + "     " + masuk + "      " + keluar + "      " + ket)
            print('\n==================================================================================================')

    elif mode == "salah":
        print("\nMode salah, silahkan diulang")