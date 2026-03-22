import speech_recognition as sr
import webbrowser
import musicLibrary
import time
import requests
import wikipedia
from gtts import gTTS
from playsound import playsound
import os

recognizer = sr.Recognizer()
newsapi = "8ef77753cb554e28b1181d8b4a33291b"


# ✅ SPEAK FUNCTION (gTTS - stable)
def speak(text):
    try:
        print("Jarvis:", text)

        tts = gTTS(text="  " + text, lang='en')  # silence padding
        filename = "voice.mp3"
        tts.save(filename)

        time.sleep(0.3)
        playsound(filename)
        time.sleep(0.2)

        os.remove(filename)

    except Exception as e:
        print("Speech Error:", e)


def processCommand(c):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song)

        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak("Song not found")

    # 🔥 NEWS FEATURE (same output style)
    elif any(word in c for word in ["news", "headlines", "update", "updates"]):
        print("Fetching latest news")
        speak("Fetching latest news")

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        response = requests.get(url)

        print("Status Code:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                speak("No news found")
                return

            speak("Here are the top headlines")
            time.sleep(1)

            for article in articles[:2]:
                title = article["title"]
                print("Speaking:", title)
                speak(title)
                time.sleep(1)

            print("Finished speaking news")

        else:
            speak("Sorry, I could not fetch news")

        # 🔥 KNOWLEDGE / QUESTION ANSWER FEATURE
    elif any(q in c for q in ["what is", "who is", "who was", "tell me about"]):
        try:
            print("Searching Wikipedia...")
            speak("Searching Wikipedia")

            query = c
            for word in ["what is", "who is", "who was", "tell me about"]:
                query = query.replace(word, "")

            query = query.strip()

            # 🔥 DIRECT TRY FIRST
            try:
                result = wikipedia.summary(query, sentences=2)

            except wikipedia.exceptions.DisambiguationError as e:
                print("Disambiguation, choosing first result...")
                result = wikipedia.summary(e.options[0], sentences=2)

            print("Answer:", result)
            speak(result)

        except Exception as e:
            print("Error:", e)
            speak("Sorry, I could not find information")
if __name__ == "__main__":
    print("Initializing Jarvis...")
    speak("Initializing Jarvis")
    time.sleep(1)

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source)

            word = recognizer.recognize_google(audio)
            print("Heard:", word)

            if "jarvis" in word.lower():
                print("Wake word detected")
                speak("Yes")

                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                processCommand(command)

        except Exception as e:
            print("Error:", e)

