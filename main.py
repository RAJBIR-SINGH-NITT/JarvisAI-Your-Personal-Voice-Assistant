import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
import os
from gtts import gTTS
import pygame


 
# pip install pocketsphinx

# pyright: ignore[reportMissingImports]
recogniser = sr.Recognizer()
newsapi = "e3c8856d4cec4205832ef4576ece2666"


def speak_old(text):
    engine = pyttsx3.init()
    # newsapi = "e3c8856d4cec4205832ef4576ece2666"
    engine.say(text)
    # pyttsx3.speak(text)
    engine.runAndWait()
    engine.stop()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load your MP3 file
    pygame.mixer.music.load('temp.mp3')  # replace with your file name

    # Play the music
    pygame.mixer.music.play()

    # Keep the program running so the music can play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    

def aiProcess(command):
    client = OpenAI(
    api_key="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",
    )
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant. give short responses"},
        {"role": "user", "content": command}
    ]
    )
     
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com") 
    elif "open youtube" in c.lower()  :
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        print(link)
        webbrowser.open(link)

    elif "news" in c.lower():
        # r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        r = requests.get(f"https://newsapi.org/v2/everything?q=India&sortBy=publishedAt&language=en&apiKey={newsapi}")
        if r.status_code == 200:
            # parse the JSON response 
            data = r.json()

            # extract the articles 
            articles = data.get('articles', [])

            # print the headlines
            for article in articles:
                speak(article['title'])
    
    else:
        # let openai handle the request
        output = aiProcess(c)
        speak(output)


                            

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    # engine.stop()
    # pyttsx3.speak("Initializing Jarvis....")
    while True: 
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
        

        # recognize speech using Sphinx
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
            word = r.recognize_google(audio)
            # print(word, word.lower())
            if (word.lower() == "jarvis"):
                print("Ya Boss")

                # pyttsx3.speak("Ya")
                speak("Ya Boss")
                # engine1 = pyttsx3.init()
                # engine1.say("Ya")
                # engine1.runAndWait()
                # engine.runAndWait()
                # speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    
                    processCommand(command)
            
                 
            
        except Exception as e:
            print("Error; {0}".format(e))
                

            
          

