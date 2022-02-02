import pyttsx3
import speech_recognition as sr
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


# j[]= {"library","exam controller office","ninfe","mfnen","fenfie","ofoem","fmefo"}
# k[]={"b2 lg 2.5", "b3 lg 2.8", " b1 lg 1.5", "b1 lg 3.4","b2 lg 5.6","b3 lg 2.2"}

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 5 <= hour < 12:
        speak("Good morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        +speak("Good Evening")
    speak("I am Tyson, how may i help you sir ?")


def takeCommand():
    # It takes microphone input from the user and returns string output
    """

    :return:
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognising..")
        query = r.recognize_google(audio, language='en-in')
        speak(f'User said: {query}\n')

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


path = 'imagesattendance'
images = []
classnames = []
mylist = os.listdir(path)

for cl in mylist:
    curimg = cv2.imread(f'{path}/{cl}')
    images.append(curimg)
    classnames.append(os.path.splitext(cl)[0])


def findencodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist


def markattendance(name):
    with open('attendance.csv', 'r+') as f:
        mydatalist = f.readlines()
        namelist = []
        for line in mydatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            # now = datetime.now()
            # dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}')
            speak(f'{name} your attendance has been recorded')


#encodelistknown = findencodings(images)

def facerecog():
    # encodelistknown = findencodings(images)
    speak('Wait for your attendance to be taken')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facescurframe = face_recognition.face_locations(imgS)
        encodescurframe = face_recognition.face_encodings(imgS, facescurframe)

        for encodeface, faceloc in zip(encodescurframe, facescurframe):
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            facedis = face_recognition.face_distance(encodelistknown, encodeface)

            matchindex = np.argmin(facedis)

            if matches[matchindex]:
                name = classnames[matchindex].upper()
                print(name)

                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
                markattendance(name)
                return 0

        cv2.imshow('webcam', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    encodelistknown = findencodings(images)
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'attendance' in query:
            facerecog()
            speak("Thank you Sir")


        elif 'thank you' in query:
            speak("You are welcome Sir")
            break
