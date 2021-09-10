import csv
from tkinter import *
from tkinter import messagebox as mb
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import pickle
import time
import cv2
import os

root = Tk()
root.geometry('400x400')
root.title("INFO")
root.configure(background='#262523')


def msg():
    if e1.index("end") == 0 :
        mb.showwarning('Missing details', 'enter your UID')
    else:
        Images()


def finalMsg():
    mb.showinfo("Take Images", "Images Saved Successfully")
    root.destroy()


def checkPassword():
    logIn = False

    csvfile = open('Students Details/Student_details.csv')
    reader = csv.reader(csvfile)
    UID = (e1.get()).upper()
    password = e2.get()

    for row in reader:
        if row[1] == UID:
            if row[2] == password:
                logIn = True

    if not logIn:
        mb.showinfo('Failed', 'Wrong Password!')
        root.e2.clear_text()
    else:
        msg()


def assure_path_exists(path):
    dir = os.path.dirname(path)
    dir = os.path.join(dir, (e1.get()).upper())
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("directory made")


def Images():
    # load our serialized face detector from disk
    print("[INFO] loading face detector...")
    protoPath = os.path.sep.join(["face_detection_model", "deploy.prototxt"])
    modelPath = os.path.sep.join(["face_detection_model", "res10_300x300_ssd_iter_140000.caffemodel"])
    detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

    # load our serialized face embedding model from disk
    print("[INFO] loading face recognizer...")
    embedder = cv2.dnn.readNetFromTorch("openface_nn4.small2.v1.t7")

    # load the actual face recognition model along with the label encoder
    recognizer = pickle.loads(open("output/recognizer.pickle", "rb").read())
    le = pickle.loads(open("output/label.pickle", "rb").read())

    z = 0

    path = "dataset/"

    assure_path_exists(path)

    # initialize the video stream, then allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    rows = 480
    cols = 640

    # start the FPS throughput estimator
    fps = FPS().start()

    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream
        frame = vs.read()

        # resize the frame to have a width of 600 pixels (while
        # maintaining the aspect ratio), and then grab the image
        # dimensions
        frame = imutils.resize(frame, width=640)
        (h, w) = frame.shape[:2]

        # construct a blob from the image
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        detector.setInput(imageBlob)
        detections = detector.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections
            if confidence > 0.5:
                # compute the (x, y)-coordinates of the bounding box for
                # the face
                box = detections[0, 0, i, 3 :7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # extract the face ROI
                face = frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                # construct a blob for the face ROI, then pass the blob
                # through our face embedding model to obtain the 128-d
                # quantification of the face
                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
                embedder.setInput(faceBlob)
                vec = embedder.forward()

                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                filename = "dataset/{}/image{}.jpg".format(e1.get(), z)
                cv2.imwrite(filename, frame)
                z += 1

        fps.update()
        # show the output frame
        cv2.imshow("Frame", frame)
        i = 1

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif z >= 300:
            break

    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()
    finalMsg()


l2 = Label(root, text="Enter UID", width=12, font=("Roboto", 12, "bold"), anchor="w", bg='#262523', fg='white')
l2.place(x=50, y=100)
e1 = Entry(root, width=30, bd=5)
e1.place(x=190, y=100)

l3 = Label(root, text="Enter Password", width=12, font=("Roboto", 12, "bold"), anchor="w", bg='#262523', fg='white')
l3.place(x=50, y=130)
e2 = Entry(root, width=30, bd=5)
e2.place(x=190, y=130)


b1 = Button(root, text='OK', command=checkPassword, width=10, bg='green', fg='white', font=("Roboto", 12, "bold"))
b1.place(x=150, y=190)

root.mainloop()
