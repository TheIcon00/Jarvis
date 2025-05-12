import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests 
import openai
openai.api_key = "your openai api key"



recogniser = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "490421361a4c41a78bbbe7e30b69fef8"
def openai_query(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    c = c.lower()
    if c == "open youtube":
        webbrowser.open("https://www.youtube.com")
    elif c == "open google":
        webbrowser.open("https://www.google.com")
    elif c == "open facebook":
        webbrowser.open("https://www.facebook.com")
    elif c.startswith("play"):
        song = " ".join(c.split(" ")[1:])
        print(f"Parsed song name: {song}")
        if song in musiclibrary.music:
            webbrowser.open(musiclibrary.music[song])
        else:
            speak(f"Sorry, I could not find the song {song}")
    elif c == "open instagram":
        webbrowser.open("https://www.instagram.com")
    elif c == "open whatsapp":
        webbrowser.open("https://web.whatsapp.com")
    elif c == "open snapchat":
        webbrowser.open("https://www.snapchat.com")
    elif "news" in c:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            for i, article in enumerate(articles[:5]):  # limit to 5 articles
                title = article.get("title")
                if title:
                    print(f"{i+1}. {title}")
                    speak(title)
        else:
            print("Failed to fetch news:", response.status_code)
    elif c == "exit":
        speak("Goodbye")
        exit()
    else:
        try:
            response = openai_query(c)
            print("OpenAI response:", response)
            speak(response)
        except Exception as e:
            print("Error with OpenAI API:", e)
            speak("Sorry, I could not process your request.")

if __name__ == "__main__":
    speak("Hello, Boss")

    while True:
        print("Listening...")
        try:
            with sr.Microphone() as source:
                print("Recognising...")
                audio = recogniser.listen(source, timeout=3, phrase_time_limit=3)
                word = recogniser.recognize_google(audio, language="en-US")
                
                if word.lower() == "jarvis":
                    speak("Yes boss")
                    with sr.Microphone() as source:
                        print("Jarvis listening...")
                        audio = recogniser.listen(source, timeout=3, phrase_time_limit=3)
                        command = recogniser.recognize_google(audio, language="en-US")
                        processCommand(command)
        except Exception as e:
            print("Error:", e)
