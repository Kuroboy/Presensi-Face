import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
import time
import datetime
import MySQLdb
import cv2, os
import IoU
import cekPin
import faceRec

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
db = MySQLdb.connect("localhost", "root","","presensi")
curs = db.cursor()
curs1 = db.cursor()
now = datetime.datetime.now()

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



class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Kehadiran Mahasiswa")
        self.resizable(False, False)
        self.geometry("500x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):
        self.destroy()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        render = PhotoImage(file='homepagepic.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=4, sticky="nsew")
        label = tk.Label(self, text="        Selamat Datang        ", font=self.controller.title_font, fg="#263942")
        label.grid(row=0, sticky="ew")
        button1 = tk.Button(self, text="   Kehadiran  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Daftar & Update data  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Exit", fg="#263942", bg="#ffffff", command=self.on_closing)
        button1.grid(row=1, column=0, ipady=3, ipadx=7)
        button2.grid(row=2, column=0, ipady=3, ipadx=2)
        button3.grid(row=3, column=0, ipady=3, ipadx=32)

    def on_closing(self):
        self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Masukan NPM", fg="#263942", font='Helvetica 10 bold').grid(row=0, column=0, pady=10, padx=5)
        self.id = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.id.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttoIn = tk.Button(self, text="Masuk", fg="#ffffff", bg="#263942", command=self.Masuk)
        self.buttoOut = tk.Button(self, text="Keluar", fg="#ffffff", bg="#263942", command=self.Keluar)
        self.buttoncanc.grid(row=1, column=2, pady=7, ipadx=5, ipady=4)
        self.buttoIn.grid(row=1, column=0, pady=7, ipadx=5, ipady=4)
        self.buttoOut.grid(row=1, column=1, pady=7, ipadx=5, ipady=4)

    def Masuk(self):
        try:
            if self.id.get() == "None":
                messagebox.showerror("Error", "NPM harus diisi")
                return
            elif len(self.id.get()) == 0:
                messagebox.showerror("Error", "NPM Harus diisi")
                return
            npm = self.id.get()
            (npmPin, namaPin) = cekPin.getPIN(npm)
            messagebox.showinfo("Info", "Tekan OK, Lalu Tunggu Kamera Menyala...")
            time.sleep(3)
            (npmFace, namaFace) = faceRec.getFace_info()
            messagebox.showinfo("Info", "Deteksi wajah selesai")
            day = now.strftime("%w")
            hari = satuMinggu(day)
            if (namaPin == namaFace and npmPin == npmFace):
                curs.execute("Insert into laporan (npm, nama) values(%s,%s)",(npmPin,namaPin))
                curs1.execute("Update laporan set tanggal = CURDATE(), hari = '" + hari + "' , jamMasuk = CURTIME() where npm = "+npmPin+" order by no desc limit 1")
                db.commit()
            else:
                messagebox.showinfo("ERROR", "NPM dan Wajah Tidak Sesuai")
        except TypeError:
            messagebox.showerror("ERROR", "Data Tidak ditemukan \nSilahkan Daftarkan Data anda")
        self.controller.show_frame("StartPage")

    def Keluar(self):
       try:
           if self.id.get() == "None":
               messagebox.showerror("Error", "NPM harus diisi")
               return
           elif len(self.id.get()) == 0:
               messagebox.showerror("Error", "NPM Harus diisi")
               return
           day = now.strftime("%w")
           hari = satuMinggu(day)
           npm = self.id.get()
           (npmPin, namaPin) = cekPin.getPIN(npm)
           curs.execute("SELECT *FROM laporan WHERE jamKeluar is NULL and jamMasuk is NOT NULL  and Hari = '" + hari + "' order by no desc limit 1")
           status = 0
           for row in curs:
               status = 1
           if status == 1:
               messagebox.showinfo("Info", "Tekan OK, Lalu Tunggu Kamera Menyala...")
               time.sleep(3)
               (npmFace, namaFace) = faceRec.getFace_info()
               if (namaPin == namaFace and npmPin == npmFace):
                   curs.execute("update laporan set jamKeluar = CURTIME() Where jamKeluar is NULL and jamMAsuk is NOT NULL and hari = '" + hari + "' order by no desc limit 1")
                   db.commit()
                   messagebox.showinfo("Info", "Proses selesai")
           else:
               messagebox.showinfo("ERROR", "Anda Belum Masuk")
           sql = "select nama, tanggal, hari, jamMasuk, jamKeluar from laporan"
           curs.execute(sql)
           result = curs.fetchall()
           tk.Label(self, text="Nama", fg="#263942", font='Helvetica 7 bold').grid(row=4, column=0, pady=5,padx=3)
           tk.Label(self, text="Tanggal", fg="#263942", font='Helvetica 7 bold').grid(row=5, column=0, pady=5,padx=3)
           tk.Label(self, text="Hari", fg="#263942", font='Helvetica 7 bold').grid(row=6, column=0, pady=5,padx=3)
           tk.Label(self, text="JamMasuk", fg="#263942", font='Helvetica 7 bold').grid(row=7, column=0, pady=5,padx=3)
           tk.Label(self, text="JamKeluar", fg="#263942", font='Helvetica 7 bold').grid(row=8, column=0, pady=5,padx=3)
           for row in result:
               name = row[0]
               tgl = str(row[1])
               hari = str(row[2])
               masuk = str(row[3])
               keluar = str(row[4])
           tk.Label(self, text=name, fg="#263942", font='Helvetica 7 bold').grid(row=4, column=1, pady=5, padx=3)
           tk.Label(self, text=tgl, fg="#263942", font='Helvetica 7 bold').grid(row=5, column=1, pady=5, padx=3)
           tk.Label(self, text=hari, fg="#263942", font='Helvetica 7 bold').grid(row=6, column=1, pady=5, padx=3)
           tk.Label(self, text=masuk, fg="#263942", font='Helvetica 7 bold').grid(row=7, column=1, pady=5, padx=3)
           tk.Label(self, text=keluar, fg="#263942", font='Helvetica 7 bold').grid(row=8, column=1, pady=5, padx=3)
       except TypeError:
           messagebox.showerror("ERROR", "Data Tidak ditemukan \n Silahkan Daftarkan Data Anda")
       self.controller.show_frame("PageOne")


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Masukan NPM", fg="#263942", font='Helvetica 10 bold').grid(row=0, column=0, pady=10,padx=5)
        self.npm = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.npm.grid(row=0, column=1, pady=10, padx=10)
        tk.Label(self, text="Masukan Nama", fg="#263942", font='Helvetica 10 bold').grid(row=1, column=0, pady=10, padx=5)
        self.name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.name.grid(row=1, column=1, pady=10, padx=10)
        tk.Label(self, text="Masukan Kelas", fg="#263942", font='Helvetica 10 bold').grid(row=2, column=0, pady=10,padx=5)
        self.kelas = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.kelas.grid(row=2, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Kembali", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttoIn = tk.Button(self, text="Daftar", fg="#ffffff", bg="#263942", command=self.iou)
        self.buttoncanc.grid(row=4, column=2, pady=7, ipadx=5, ipady=4)
        self.buttoIn.grid(row=4, column=1, pady=7, ipadx=5, ipady=4)

    def iou(self):
        try:
            if self.npm.get() == "None":
                messagebox.showerror("Error", "NPM harus diisi")
                return
            elif len(self.npm.get()) == 0:
                messagebox.showerror("Error", "NPM Harus diisi")
                return
            elif self.name.get() == "None":
                messagebox.showerror("Error", "Nama harus diisi")
                return
            elif len(self.name.get()) == 0:
                messagebox.showerror("Error", "Nama Harus diisi")
                return
            elif self.kelas.get() == "None":
                messagebox.showerror("Error", "Kelas harus diis")
                return
            elif len(self.kelas.get()) == 0:
                messagebox.showerror("Error", "Kelas Harus diisi")
                return
            id = self.npm.get()
            nama = self.name.get()
            kelas = self.kelas.get()
            messagebox.showinfo("Info", "Tekan OK, Lalu Tunggu Kamera Menyala \nUntuk mengambil Data Wajah...")
            IoU.face_insertOrUpdate(id, nama, kelas)
            IoU.PIN_insertOrUpdate(nama, id, kelas)
            sampleNum = 0
            cam = cv2.VideoCapture(0)
            time.sleep(5)
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    sampleNum = sampleNum + 1
                    cv2.imwrite("dataSet/user." + str(id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow('img', img)
                cv2.waitKey(50)
                if sampleNum > 50:
                    os.system("del dataTrain\\train.yml /s /q")
                    os.system("python3 Training.py")
                    os.mkdir("absensi\\" + id)
                    break
            messagebox.showinfo("Info", "Proses Selesai..")
            cam.release()
            cv2.destroyAllWindows()
        except FileExistsError:
            messagebox.showinfo("Info", 'Npm anda sudah terdaftar \ndata anda akan diupdate')
        cam.release()
        cv2.destroyAllWindows()
        self.controller.show_frame("StartPage")

app = MainUI()
#app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()