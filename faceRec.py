import datetime
import time
import MySQLdb
import cv2, os

cascadePath = ("haarcascade_frontalface_default.xml")
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('dataTrain/train.yml')
now = datetime.datetime.now()


def getProfile(id):
    db = MySQLdb.connect("localhost", "root", "", "presensi")
    curs = db.cursor()
    cmd = "select *from facebase where npm="+str(id)
    curs.execute(cmd)
    profile = None
    rows = curs.fetchall()
    for row in rows:
        profile = row
    curs.close()
    return profile


def getFace_info():
    cam = cv2.VideoCapture(0)
    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            profile = getProfile(id)
            print(str(id) + str(conf))
            if (conf < 40):
                if (profile != None):
                    cv2.imwrite("absensi/" + profile[1] + "/" + now.strftime("%Y-%m-%d %H-%M") + "[1]" + ".jpg", img)
                    cv2.imwrite("absensi/" + profile[2] + "/" + now.strftime("%Y-%m-%d &H-&M") + "[2]" + ".jpg", img)
                    time.sleep(3)
                    return profile[1], profile[2]
                    break
                else:
                    cam.release()
                    cv2.destroyAllWindows()
            cv2.imshow('img', img)
        if cv2.waitKey(10) & 0xff == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()