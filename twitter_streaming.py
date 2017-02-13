
import tweepy
from tweetListener import TweetListener

import cv2
import numpy as np

from kivy.loader import Loader
import urllib

try:
    import thread
except ImportError:
    import _thread as thread


from kivy.uix.image import Image
from kivy.uix.label import Label

import math
from time import time
from kivy.app import App
from kivy.clock import Clock

#twitter keys
access_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxxxxxxxxxx"
consumer_key = "xxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

class imageInformation(Image):

    posHintX = 0.0
    posHintY = 0.4
    IMGsize = 0.2

    def initPos(self, i, extraSize, xposdiff, yposdiff):
        FirstPicExtraSize = extraSize

        self.allow_stretch = True
        self.keep_ratio = False

        self.size_hint = (self.IMGsize + FirstPicExtraSize, self.IMGsize + FirstPicExtraSize)

        ImagesPerRow = 5
        ydisp = math.floor(i / ImagesPerRow)
        calcposHintY = self.posHintY - (ydisp * self.IMGsize)
        calcposHintX = self.posHintX + (self.IMGsize * (i%ImagesPerRow))

        self.posHintX = calcposHintX + xposdiff
        self.posHintY = calcposHintY + yposdiff
        self.pos_hint = {'x': self.posHintX, 'y': self.posHintY}

    def moveOneStepOver(self, destImgPosHintX, destImgPosHintY):
        self.size_hint = (self.IMGsize, self.IMGsize)
        self.posHintX = destImgPosHintX
        self.posHintY = destImgPosHintY
        self.pos_hint = {'x': destImgPosHintX, 'y': destImgPosHintY}

    def setTexture(self, inTexture):
        self.texture = inTexture

class StdOutListener(tweepy.StreamListener):

    imageURLArray = []
    notDoneReading = True

    #this number resets as i create a new listener for every new twitter thread.
    nrOfTweets = 0

    def on_error(self, status):
        print(status)

    def on_status(self, status):
        self.nrOfTweets += 1
        if 'media' in status.entities:
            #print('Tweet text: ' + status.text)

            #Takes the images and puts them in the list
            for image in status.entities['media']:
                mediaUrl = image['media_url']
                self.imageURLArray.append(mediaUrl)

        #returns NotDoneReading is set to false to kill the thread
        return self.notDoneReading

class ShowcaseApp(App):
    TPHLabel = None
    tweetThrad = None

    currentFacesString = "Number of faces found in active picture: "
    twitterSearchTagString = "Searching twitter by tag: "
    tweetsperhourString = "Number of tweets per hour: "

    imageList = []
    nrOfImages = 10

    mainImageSizeDif = 0.2
    mainImagePosXDif = 0.0
    mainImagePosYDif = 0.2

    startTime = time()

    totalTweetsPerHour = 0

    def build(self):

        root = self.root

        #Null image
        filename = 'data/none.png'
        try:

            for i in range(0, self.nrOfImages):
                self.image = imageInformation(source=filename)

                #cosmetic. to make the first picture larger.
                if i == 0:
                    self.image.initPos(0, self.mainImageSizeDif, self.mainImagePosXDif, self.mainImagePosYDif)
                else:
                    self.image.initPos(i, 0, 0, 0)

                self.imageList.append(self.image)
                root.add_widget(self.image)

        except Exception as e:
            print(e)

        self.title = 'tweet reader'
        Clock.schedule_interval(self._update_clock, 1 / 60.)


        self.ListenerInstance = StdOutListener()
        self.TL = TweetListener()

        # starts the thread that listens for tweets.
        tag = "selfie"
        thread.start_new_thread(self.TL.TweetCollectorThreadFunc, (tag, self.ListenerInstance))

        #creates the text that shows the desired data from the tweets / imgaes.
        #I would rather have made this in the .kv file but could not get access to them correctly from there
        #I probably missed something but no time to fix this now.
        self.TPHLabel = Label(text=self.tweetsperhourString + self.ListenerInstance.nrOfTweets.__str__(), size_hint= (1.6, 1.9))

        self.TSTLabel = Label(text=self.twitterSearchTagString + tag, size_hint=(1.6, 1.8))

        self.CFLabel = Label(text=self.currentFacesString, size_hint=(1.4, 1.5))

        root.add_widget(self.TPHLabel)

        root.add_widget(self.TSTLabel)

        root.add_widget(self.CFLabel)

    def findFace(self, url):

        cascPath = "C:/Users/Mattias/PycharmProjects/untitled/haarcascade_frontalface_default.xml"
        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(cascPath)
        # Read the image
        req = urllib.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        image = img
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return len(faces)


    def on_enter(self, value):
        #by making the listener return false the tweet listener finishes.
        #create a new listener in case the old one is busy for too long after being killed
        #as it only returns false when it gets the next messsage it might get locked for ever.
        #but this way fixes that.
        self.ListenerInstance.notDoneReading = False
        self.ListenerInstance = StdOutListener()

        #sets the string to correct tag
        self.TSTLabel.text = self.twitterSearchTagString + value

        # starts the thread that listens for tweets.
        #very unoptimal solution.
        #would be better if I didnt have to auth every time I create a new thread
        #or even better, I used the same thread just paused the stream to change tag
        #could not get it to work so this will have to do.
        thread.start_new_thread(self.TL.TweetCollectorThreadFunc, (value, self.ListenerInstance))


    def image_loaded(self, inImage):
        #when an image is loaded. create a new imageinformation and put it at the start of the line of pics.
        #then move every picture one step to the right.

        root = self.root

        self.image = imageInformation(texture=inImage.image.texture)
        self.image.initPos(0, self.mainImageSizeDif, self.mainImagePosXDif, self.mainImagePosYDif)

        for i in range(0,self.nrOfImages-1):
            self.imageList[i].moveOneStepOver(self.imageList[i+1].posHintX, self.imageList[i+1].posHintY)

        #removes the last image widet in the list
        root.remove_widget(self.imageList[self.nrOfImages-1])

        #puts the first picture first in the lsit
        self.imageList = [self.image] + self.imageList

        #removes the last elemet in the list
        self.imageList.pop()

        root.add_widget(self.image)

    def _update_clock(self, dt):
        self.HandleTweet()

        self.updateTweetsPerHour()

    def updateTweetsPerHour(self):
        appRunningTime = time() - self.startTime

        #tweets per second
        tweetsperhour = self.ListenerInstance.nrOfTweets / appRunningTime

        #tweets per hour
        tweetsperhour *= 3600

        self.TPHLabel.text = self.tweetsperhourString + tweetsperhour.__str__()

    def HandleTweet(self):
        #Gets the Image URLs from the list and starts to load them.
        TempTweetArray = self.ListenerInstance.imageURLArray
        self.ListenerInstance.imageURLArray = []

        for url in TempTweetArray:

            proxxyimage = Loader.image(url)

            proxxyimage.bind(on_load=self.image_loaded)

            #really bad emergency solution. this makes the program download the image from the url twice.
            #I could not get it to convert from kivy image to a numpy array so that I could use the aldready downloaded image.
            #makes the program laggy. should be threaded to prevent blockage.
            #This number should be put in the ImageInformation class so every picture keeps the number of faces.
            #But since the convertion did not work the whole design goes away and this is the best I could figure out for now.
            #Since the convertion didnt work I probably have to rework some stuf or look further into the conversion.
            tempNumber = self.findFace(url); #comment out this line to remove face-rec and make program run alot faster
            self.CFLabel.text = self.currentFacesString + tempNumber.__str__()


if __name__ == '__main__':
    ShowcaseApp().run()

