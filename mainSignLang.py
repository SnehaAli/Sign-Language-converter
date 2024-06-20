import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import cv2
from easygui import *
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string


from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import math


# import selecting
# obtain audio from the microphone
#AUDIO TO TEXT TO SIGN
def func():
    r = sr.Recognizer()
    asl_gif = ['are you okay', 'are you alright', 'applause', 'all night', 'animals', 'anyone', ' april', 'awesome',
               'belt', 'bird', 'black', 'blog', 'blue', 'bow', 'brave', 'breakup', 'broken hearted', 'baby', 'birth',
               'balloon', 'brown', 'bull',
               'can i borrow that', 'cartoon', 'championship', 'cheetah', 'childish', 'clever', 'child', 'cool', 'color',
               'costume', 'calm down',
               'dancer', 'dancing', 'dak red', 'day', 'december', 'deer', 'delete', 'disconnect', 'drum', 'duck',
               'empy', 'entertainment', 'everyday', 'excited', 'excuse me',
               'facebook', 'fall in love', 'fashion show', 'father', 'family',  'fox', 'friday', 'fish', 'foosball',
               'february',
               'game', 'goat', 'gold', 'good afternoon', 'good evening', 'golf', 'good night', 'gray', 'green',
               'good morning', 'girlfriend',
               'hair style', 'hashtag', 'hello', 'honored', 'how are you', 'he', 'happy','happy new year',
               'how are you doing', 'heart', 'her', 'hy', 'hi', 'hey',
               'i am impressed', 'i dont know', 'i dont like it', 'i dont understand', 'itself', 'it',  'i love you',
               'i enjoy this', 'i impress you', 'i know', 'i like it', 'i understand', 'i want', 'ice', 'ill help',
               'i am fine', 'impress', 'impressed', 'inspired', 'instagram', 'internet', 'is it cold in here',
               'is it warm in here', 'its clear', 'its not clear', 'its really hard', 'is it far', 'i am lost',
               'january', 'joke', 'july',
               'kick', 'kids', 'knock it off',
               'late night', 'laugh heartily', 'light purple', 'like', 'lion', 'lipstick',
               'maybe', 'me', 'medium couch', 'monday', 'monster', 'monthly', 'mouse', 'movie', 'mother', 'march',
               'merry christmas',
               'november', 'nice to meet you', 'not my problem',
               'orange', 'olympics',
               'parade', 'parents', 'peace', 'peaceful', 'penguin', 'pink', 'please repeat', 'point', 'pool', 'proud',
               'please', 'please help me', 'practice',
               'quaterback',
               'red', 'relieved', 'remorseful', 'rolling on the floor laughing', 'rose',
               'saturday', 'seriously', 'shark', 'sheep', 'shocked', 'shy', 'signing vlog', 'silver', 'social media',
               'soon', 'sports', 'spring', 'steal', 'stunned', 'summer', 'sunday', 'sunrise', 'sailing', 'sorry',
               'standing ovation', 'someone',
               'thank you so much', 'theatre', 'thursday', 'tickle', 'tiger', 'time', 'today', 'tomorrow', 'touched',
               'tuesday', 'twitter', 'tease', 'tennis', 'tie', 'thank you', 'three of us', 'thirsty', 'ticket',
               'us', 'usher', 'understand', 'us',
               'volleyball', 'vlog',
               'what are you doing','what is the weather link', 'whats for lunch', 'whats the weather like for today',
               'whats wrong', 'which building', 'white', 'world series', 'wrestling', 'waste time', 'weekend', 'whale',
               'wonderful', 'wheres the classroom', 'wheres the bathroom', 'win',
               'yellow', 'you are beautiful', 'young']

    arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
    with sr.Microphone() as source:

        r.adjust_for_ambient_noise(source)
        i = 0
        while True:
            print("Speak Now")
            audio = r.listen(source)
            # recognize speech using Sphinx
            try:
                a = r.recognize_google(audio)
                a = a.lower()
                print('You Said: ' + a.lower())

                for c in string.punctuation:
                    a = a.replace(c, "")

                if (a.lower() == 'goodbye' or a.lower() == 'good bye' or a.lower() == 'bye'):
                    print("oops!Time To say good bye")
                    break

                elif (a.lower() in asl_gif):

                    class ImageLabel(tk.Label):
                        """a label that displays images, and plays them if they are gifs"""

                        def load(self, im):
                            if isinstance(im, str):
                                im = Image.open(im)
                            self.loc = 0
                            self.frames = []

                            try:
                                for i in count(1):
                                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                                    im.seek(i)
                            except EOFError:
                                pass

                            try:
                                self.delay = im.info['duration']
                            except:
                                self.delay = 100

                            if len(self.frames) == 1:
                                self.config(image=self.frames[0])
                            else:
                                self.next_frame()

                        def unload(self):
                            self.config(image=None)
                            self.frames = None

                        def next_frame(self):
                            if self.frames:
                                self.loc += 1
                                self.loc %= len(self.frames)
                                self.config(image=self.frames[self.loc])
                                self.after(self.delay, self.next_frame)

                    root = tk.Tk()
                    lbl = ImageLabel(root)
                    lbl.pack()
                    lbl.load(r'ASL_Gifs/{0}.gif'.format(a.lower()))
                    root.mainloop()
                else:
                    for i in range(len(a)):
                        if (a[i] in arr):

                            ImageAddress = 'letters/' + a[i] + '.jpg'
                            ImageItself = Image.open(ImageAddress)
                            ImageNumpyFormat = np.asarray(ImageItself)
                            plt.imshow(ImageNumpyFormat)
                            plt.draw()
                            plt.pause(1)
                        else:
                            continue

            except:
                print(" ")
            plt.close()


#SIGN TO TEXT
def func1():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

    imgSize = 300
    offset = 20



    labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z"]

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgOutput = img.copy()
        hands, img = detector.findHands(img)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]

            imgCropShape = imgCrop.shape


            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                print(prediction, index)

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)

            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                          (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y - 27), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (255, 0, 255), 4)

           # cv2.imshow("ImageCrop", imgCrop)
            #cv2.imshow("ImageWhite", imgWhite)

        cv2.imshow("Image", imgOutput)
        key = cv2.waitKey(1)

def chart():
    img = cv2.imread("letters/ASLlang.jpg")
    cv2.imshow("American Sign Language CHART", img)
    cv2.waitKey(0)


while 1:
    image = "signLanguage/ASL2.png"
    msg = "AMERICAN SIGN LANGUAGE"
    choices = ["Audio to Sign", "Sign To Text ", "American Sign Language Chart", "QUIT!"]
    reply = buttonbox(msg, image=image, choices=choices)
    if reply == choices[0]:
        func()
    if reply == choices[1]:
        func1()
    if reply == choices[2]:
        chart()
    if reply == choices[3]:
        quit()