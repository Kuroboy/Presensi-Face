import signal
import MySQLdb
import getpass
import tkinter as tk
from tkinter import messagebox
import sys

db = MySQLdb.connect("localhost", "root","","presensi")
cur = db.cursor()

def signal_handler(signal,frame):
    global lanjut
    print("\nCTRL+C capture, ending read")
    sys.exit(0)
    lanjut = False

def getPIN(npm):
        try:
            passKey = npm
            sql = "select *from passkey where pkey = %s" %passKey
            cur.execute(sql)
            result = cur.fetchall()
            for row in result:
                npm = row[3]
                nama = row[2]
                kelas = row[4]
            print ("\nNama : %s \nNPM : %s \nKelas : %s" %(nama, npm, kelas))
            return npm, nama

            curs.close()
        except UnboundLocalError as e:
            print("\nData Tidak ditemukan")
