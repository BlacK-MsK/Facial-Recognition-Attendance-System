import csv
from csv import writer
from imutils.video import VideoStream
from imutils.video import FPS
import dataframe_image as dfi
from datetime import datetime, date
import pandas as pd
import numpy as np
import imutils
import pickle
import time
from tkinter import messagebox as mb
import cv2
import os

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

now = datetime.now()
today_date = date.today()
d1 = today_date.strftime("%d/%m/%Y")
Same_Student_name_time = 0

csv_name = (str(d1)+".csv")


def append_list_as_row(file_name, list_of_elem):
    writerCsv = True

    with open(file_name, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader :
            if row[0] == row_contents[0] :
                writerCsv = True
            else:
                writerCsv = False

    if not writerCsv:
        with open(file_name, 'a+', newline='') as write_obj :
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)

    
    mb.showinfo("Info", "Attendance marked")
    Attendance_dataframe = pd.read_csv("Attendance CSV/Attendance {}.csv".format(today_date))
    dfi.export(Attendance_dataframe, "Attendance Dataframes/Attendance File_{}.png".format(today_date))
    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()
    exit()
            



# initialize the video stream, then allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
rows = 480
cols = 640

# start the FPS throughput estimator
fps = FPS().start()

Student_name = "None"
face = []
UID = "123"
run_once = 0
z = 0


# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream
    frame = vs.read()
    result = True

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
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
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

            # perform classification to recognize the face
            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]

            # draw the bounding box of the face along with the
            # associated probability
            if name == "Unknown":
                text = "ID: {}".format(name)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
            else:
                text = "ID: {}".format(name)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

                UID = name


                Same_Student_name_time = 0
                i += 1
                if run_once == 0:
                    current_time = now.strftime("%H:%M:%S")
                    row_contents = [UID, current_time, d1, "Present"]
                    result = append_list_as_row("Attendance CSV/Attendance {}.csv".format(today_date), row_contents)
                    run_once = 1

    fps.update()
    # show the output frame
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    # elif not result == 1:
    #     mb.showinfo("Info!", "Attendance already marked!")
    #     break

# stop the timer and display FPS information

Attendance_dataframe = pd.read_csv("Attendance CSV/Attendance {}.csv".format(today_date))
dfi.export(Attendance_dataframe, "Attendance Dataframes/Attendance File_{}.png".format(today_date))

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

