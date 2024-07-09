import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclib
import requests
from openai import OpenAI

recognizer=sr.Recognizer()
engine = pyttsx3.init()
api_key = '07ae76edad4f4950b91d5eeaf2047d4f' #news apikey
url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
def speak(text):
   engine.say(text)
   engine.runAndWait()

def aiprocess(command):
    client = OpenAI( api_key="apikey",
    )
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like alexa"},
    {"role": "user", "content": command}
    ]
   )
    return completion.choices[0].message.content

def processcommand(command):
    if "open google" in command.lower():
       webbrowser.open("https://google.com")    
    elif "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com/")
    elif command.lower().startswith("play"):
        song=command.lower().split(" ")[1]
        link=musiclib.music[song]
        webbrowser.open(link)    
    elif "news" in command.lower():
        req=requests.get(url)
        if req.status_code == 200:
          headlines = req.json()
          for article in headlines['articles']:
            speak(article['title'])
    else:
       answer=aiprocess(command)
       speak(answer)

if __name__ == "__main__": 
   speak("Initializing jarvis")
 
while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Say Jarvis...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower()=="jarvis":
                speak("Yes sir")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processcommand(command)
            else:
                speak("Sorry i can't understand")


        except Exception as e:
               print("Error; {0}".format(e))