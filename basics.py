import cv2
import numpy as np
import face_recognition

imgjlaw = face_recognition.load_image_file('Imagebasic/jlaw.jpg')
imgjlaw = cv2.cvtColor(imgjlaw,cv2.COLOR_BGR2RGB)
imgtest = face_recognition.load_image_file('Imagebasic/jlaw test.jpg')
imgtest = cv2.cvtColor(imgtest,cv2.COLOR_BGR2RGB)

faceloc = face_recognition.face_locations(imgjlaw)[0]
encodejlaw = face_recognition.face_encodings(imgjlaw)[0]
cv2.rectangle(imgjlaw,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)

faceloctest = face_recognition.face_locations(imgtest)[0]
encodetest = face_recognition.face_encodings(imgtest)[0]
cv2.rectangle(imgtest,(faceloctest[3],faceloctest[0]),(faceloctest[1],faceloctest[2]),(255,0,255),2)

results = face_recognition.compare_faces([encodejlaw],encodetest)
facedis = face_recognition.face_distance([encodejlaw],encodetest)
print(results,facedis)
cv2.imshow('Jennifer', imgjlaw)
cv2.imshow('Jennifer test', imgtest)
cv2.waitKey(0)