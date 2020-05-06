# import PyTesseract for image-to-text analysis
# link to Tesseract installation: 
# https://github.com/UB-Mannheim/tesseract/wiki?fbclid=IwAR2aj_N_2qrLLyNFRYwULr_1NDaB20TPQa93h-beGDvIQv1akGsByEXYCOQ

# then add tesseract to the path
# pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import pytesseract as pt

# import python imaging library
from PIL import Image

# import speech recognition for getting the desired destination language for users
import speech_recognition as sr

# import opencv for accessing camera, possibly, to detect corners of an image, then capture it
# so that it's easier than to have pytesseract translate image to text with live video
import cv2 as cv

# import selenium for web scraping in order to automate the translation on Google Translate
import selenium
from selenium import webdriver
# import webdriverwait for wait time
from selenium.webdriver.support.ui import WebDriverWait
# import keys for any keyboard triggering
from selenium.webdriver.common.keys import Keys
# import time for prgramme sleep time
import time

# import GTTS for text-to-speech
# text-to-speech
from gtts import gTTS
import os

# import tkinter
import tkinter as tk
# print('Package Loaded')

# specifying languages to be used for image-to-text analysis
# vietnamese, english, korean, chinese simplified, french
langs_tesseract = 'vie+eng+kor+chi_sim+fra'

# specifying languages to be used for google engine (GTTS, Google Translate)
langs_gg = 'vi+en+ko+zh+fr'

# SPEECH RECOGNITION
# initialise recogniser
r = sr.Recognizer()


def chooseDestLanguage():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            global destL
            destL = r.recognize_google(audio)
            # make the destination lang lower case as it'll be searched up on google translate
            destL = destL.lower()
            if 'viet' in destL:
                destL = 'vi'
                print(destL)
            elif 'kor' in destL:
                destL = 'ko'
                print(destL)
            elif 'chi' in destL:
                destL = 'zh-CN'
                print(destL)
            # call the function to do web scraping on Google Translate
            googleTranslate()
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))


# initialise OPENCV live video webcam
cap = cv.VideoCapture(0)

def liveVideoCapture():
    while True:
        # loop through the img sequence and pass it to another variable
        _, frames = cap.read()
        gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
        cv.imshow('Live Webcam', frames)

        # end the loop if there is a key interrupts 
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        # toText = pt.image_to_string(gray, lang=langs_tesseract)
        # if toText == '' or toText == None:
        #     pass
        # else:
        #     print(toText)

# SELENIUM - WEB SCRAPING (GOOGLE TRANSLATE)
def googleTranslate():
    # set the path to the chrom driver executables file
    # link to download: https://sites.google.com/a/chromium.org/chromedriver/downloads
    PATH = 'C:\Program Files (x86)\chromedriver.exe'

    # opts = ChromeOptions()
    # opts.add_experimental_option("excludeSwitches", ['enable-automation'])
    # choose the web browser type to be driven
    driver = webdriver.Chrome(PATH)

    # specify the url to be driven, format it with the custom destL
    driver.get(f'https://translate.google.com/#view=home&op=translate&sl=auto&tl={destL}')

    # set input field
    inputField = 'source'

    # set output field
    outputField = "//div[@class='result tlid-copy-target']"

    # find input field
    input = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(inputField))

    # input = driver.find_element_by_xpath("//textarea[@id='source']")
    analyseImg()

    # wait for 3 secs for analysing text
    time.sleep(3)

    # input some keywords into the field
    input.send_keys(keywords)

    # wait for 3 secs
    time.sleep(3)

    # before finding out the output HTML element 
    # as it's hidden before the input field is filled with text
    output = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(outputField))

    print(output.text)
    time.sleep(3)

def analyseImg():
    # for prototyping
    # testing the accuracy in image-to-text analysis between grayscaled img and coloured img 
    img = cv.imread('media/img/vietnamese.png')
    # img = Image.open('media/img/korean.jpg')
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imshow('Gray', grey)
    # cv.imshow('Coloured', img)
    global keywords
    keywords = pt.image_to_string(grey, lang=langs_tesseract)
    cv.waitKey(0)
    print(keywords)

    
# TKINTER
root = tk.Tk()

canvas = tk.Canvas(root, bg='white')
canvas.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

webcamBtn = tk.Button(root, text='Open Live Webcam', padx=20, pady=10, fg='white', bg='black', command=liveVideoCapture)
webcamBtn.pack()

imageRecognitionBtn = tk.Button(root, text='PyTesseract', padx=20, pady=10, fg='white', bg='black', command=analyseImg)
imageRecognitionBtn.pack()

speakBtn = tk.Button(root, text='Speak Your Desired Destination Language', padx=20, pady=10, fg='white', bg='black', command=chooseDestLanguage)
speakBtn.pack()

root.mainloop()