#created on May 11 2021 by Ethan Santos

from tkinter.constants import CENTER, YES
import speech_recognition as sr
import webbrowser
import time
import pyautogui
import playsound
import os
import random
import requests
import urllib.request
import urllib.parse
import urllib
import re
import json
import randfacts
import wolframalpha
import tkinter
from urllib.request import urlopen
from lxml import etree
from pynput import keyboard
from pynput.keyboard import Key, Listener
from bs4 import BeautifulSoup
from gtts import gTTS
from time import ctime

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.winfo_toplevel().title("Jarvis Voice Assistant")
        self.listen_button = tkinter.Button(self)
        self.listen_button["text"] = "Listen"
        self.listen_button["command"] = self.say_hi
        self.listen_button.pack(side="top", expand=YES)

    def listen(self):
        print('Listening')
        replies = ['Yes sir?', 'I am listening sir.', 'What do you need sir?', 'What would you like me to do sir?', 'At your service.']
        reply = replies[random.randint(0,len(replies)-1)]
        jarvis_speak(reply)
        self.listen_button["text"] = "Listen"
        voice_data = record_audio()
        print(voice_data)
        #if there_exists(['hey Jarvis', 'Jarvis']):
        respond(voice_data)
        #root.after(10, self.listen)

    def say_hi(self):
        root.after(10, self.listen)
        self.listen_button["text"] = "Listening"

app_id = "28UXLL-P79R54QWWH"
client = wolframalpha.Client(app_id)

r = sr.Recognizer()

def there_exists(terms, voice_data):
    for term in terms:
        if term in voice_data:
            return True

def jarvis_speak(audio_string):
    tts = gTTS(text=audio_string, lang = 'en', tld = 'co.uk')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) +'.mp3'
    tts.save(audio_file)
    print(audio_string)
    playsound.playsound(audio_file)
    os.remove(audio_file)

def record_audio(ask = False): 
    with sr.Microphone() as source:
        #r.adjust_for_ambient_noise(source)
        if ask:
            jarvis_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            jarvis_speak('Sorry, I do not understand what you are saying.')
        except sr.RequestError:
            jarvis_speak('Sorry, my speech service is down.')
        return voice_data

def news():
    query_params = {
      "source": "google-news",
      "sortBy": "top",
      "apiKey": "d4e3901e3c10405e987df6bbec9ecaf6"
    }
    main_url = " https://newsapi.org/v1/articles"
 
    # fetching data in json format
    res = requests.get(main_url, params=query_params)
    open_news_page = res.json()
 
    # getting all articles in a string article
    article = open_news_page["articles"]
 
    # empty list which will
    # contain all trending news
    results = []
     
    for ar in article:
        results.append(ar["title"])
         
    for i in range(5):
         
        # printing all trending news
        jarvis_speak(results[i])

def respond(voice_data):
    if there_exists(['hey','hi','hello'], voice_data):
        greetings = ['Greetings. How may I help you?', 'Hello! What can I do for you?']
        greet = greetings[random.randint(0,len(greetings)-1)]
        jarvis_speak(greet)
    elif there_exists(['what is your name', "what's your name", 'what can I call you', 'do you have a name'], voice_data):
        jarvis_speak('My name is Jarvis.')
    elif there_exists(['what are you'], voice_data):
        jarvis_speak('I am Jarvis, a voice assistant created by Ethan.')
    elif there_exists(['time'], voice_data):
        jarvis_speak(ctime())
    elif there_exists(['search', 'Google',], voice_data):
        #search = record_audio('What would you like to search sir?')
        if there_exists(['search',], voice_data):
            search = search = voice_data.split("search", 1)[1] 
        elif there_exists(['Google'], voice_data):
            search = search = voice_data.split("Google", 1)[1] 
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        jarvis_speak('Here is what I found for ' + search)
    elif there_exists(['location'], voice_data):
        location = record_audio('What do you want me to find sir?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        jarvis_speak('Here is the location of ' + location)
    elif there_exists(['weather'], voice_data):
        location = record_audio('Which location would you like to check the weather for?')
        url = 'https://google.com/search?q='+'weather '+ location
        webbrowser.get().open(url)
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        jarvis_speak('Here is the weather for ' + location)
        jarvis_speak(temp)
    elif there_exists(['open Roblox'], voice_data):
        url = 'https://www.roblox.com/home'
        webbrowser.get().open(url)
        jarvis_speak('Opening roblox.')
    elif there_exists(['close Chrome'], voice_data):
        os.system("taskkill /im chrome.exe /f")
        jarvis_speak('Closing all chrome tabs.')
    elif there_exists(['news'], voice_data):
        news()
    elif there_exists(['play music', 'play a song'], voice_data):
        
        song = record_audio('What song would you like to play sir?')
        replaced_song = song.replace(" ", "+")
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + replaced_song)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        webbrowser.get().open(url)
        params = {"format": "json", "url": url}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            jarvis_speak('Currently playing ' + data['title'])
    elif there_exists(['play', 'pause'], voice_data) and 'music' not in voice_data:
        pyautogui.typewrite(['space'])
    elif there_exists(['volume up', 'turn up the volume'], voice_data):
        pyautogui.typewrite(['volumeup'])
    elif there_exists(['volume down', 'turn down the volume'], voice_data):
        pyautogui.typewrite(['volumedown'], voice_data)
    elif there_exists(['mute', 'unmute'], voice_data):    
        pyautogui.typewrite(['volumemute'], voice_data)
    elif there_exists(['what', 'how', 'when', 'why', 'who'], voice_data) and 'you' not in voice_data and 'your' not in voice_data and 'weather' not in voice_data and 'time' not in voice_data and 'Google' not in voice_data and 'news' not in voice_data and 'search' not in voice_data:
        res = client.query(voice_data)
        try:
            answer = next(res.results).text
        except StopIteration:
            answer = "I do not have an answer."
        jarvis_speak(answer)
    elif there_exists(['fact'], voice_data):
        jarvis_speak(randfacts.getFact())
    elif there_exists(['send Discord message'], voice_data):
        message = record_audio('What message would you like to send sir?')
        pyautogui.write(message)
        pyautogui.hotkey('enter')
    elif there_exists(['goodbye', 'exit', 'turn off', 'close', 'shutdown'], voice_data) and 'Chrome' not in voice_data:
        jarvis_speak('Goodbye sir. Turning off.')
        exit()
    else:
        jarvis_speak('Sorry. I do not know what you want me to do.')

jarvis_speak("Hello sir. How may I help you?")

def wake_command():
    print('Listening for wake command')
    voice_data = record_audio()
    if there_exists(['hey Jarvis', 'Jarvis'], voice_data):
        replies = ['Yes sir?', 'I am listening sir.', 'What do you need sir?', 'What would you like me to do sir?', 'At your service.']
        reply = replies[random.randint(0,len(replies)-1)]
        jarvis_speak(reply)
        voice_data = record_audio()
        respond(voice_data)
    root.after(10, wake_command)

root = tkinter.Tk()
app = Application(master=root)
#root.after(10, wake_command)
root.mainloop()