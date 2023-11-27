import getpass
import signal
import MySQLdb
import cv2, os
import time
import datetime
from pathlib import Path


detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
db = MySQLdb.connect("localhost","root","","presensi")
db1 = MySQLdb.connect("localhost","root","","laporan")
lanjut = False

def signal_handler(signal,frame):
    global lanjut
    print("\nCTRL+C capture, ending read")
    sys.exit(0)
    lanjut = False

def face_insertOrUpdate(id,nama,kelas):
    curs = db.cursor()
    curs1 = db1.cursor()
    curs.execute("select *from facebase where npm=" +str(id))
    statData = 0
    for row in curs:
        statData = 1
    if (statData == 1):
        curs.execute("UPDATE facebase SET nama=%s, kelas=%s WHERE npm=%s",(nama,kelas,str(id)))
        db.commit()
        curs.close()
    else:
        curs.execute("INSERT INTO facebase(npm,nama,kelas)values(%s,%s,%s)",(id,nama,kelas))
        curs1.execute("""CREATE TABLE if not exists t_"""+str(id)+"""
        (nomor INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        nama varchar(30) default '"""+str(nama)+"""',
        kelas varchar(8) default '"""+str(kelas)+"""',
        tanggal date NOT NULL,
        hari varchar(10),
        jamMasuk time        NOT NULL,
        jamKeluar time)""")
    db.commit()
    db1.commit()
    curs.close()

def PIN_insertOrUpdate(nama,id,kelas):
    global lanjut
    while (True):
        passKey = id
        if passKey and len(passKey) == 8:
            curs = db.cursor()
            curs2 = db.cursor()
            curs3 = db1.cursor()
            curs.execute("""SELECT *FROM
            passkey WHERE pkey=%s""", [passKey])
            curs2.execute("""SELECT *FROM
            passkey WHERE npm="""+id)
            curs3.execute("SELECT *FROM t_"+id)
            statusData = 0
            for row in curs2 :
                statusData = 1
            if (statusData == 1):
                curs3.execute("UPDATE t_"+id+" SET nama=%s, kelas=%s",(nama,kelas))
                curs2.execute("""UPDATE passkey SET 
                nama=%s, kelas=%s, pkey=%s WHERE npm=%s""",(nama,kelas,passKey,id))
                db.commit()
                db1.commit()
                curs.close()
                curs2.close()
                curs3.close()
            else:
                curs.execute("""INSERT INTO passkey
                (pkey,npm,nama,kelas)
                values(%s,%s,%s,%s)""",(str(passKey),id,nama,kelas))
                db.commit()
                curs.close()
            break
        else:
            print("\nPIN yang dimasukan salah")
            continue
