import pyttsx3
import datetime
import webbrowser
import os
import wikipedia
import speech_recognition as sr
import warnings

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak('good morning!')
    elif 12 <= hour < 18:
        speak('good afternoon!')
    else:
        speak('good evening!')
    speak("I am NILA, your natural interactive live assistant. Please tell me how can I help you.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print('Can you please say that again...')
        return "None"
    return query

if __name__ == '__main__':
    # Suppress BeautifulSoup warning
    warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")
    
    wishMe()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.DisambiguationError as e:
                options = e.options
                speak("The term 'when' is ambiguous. Please specify a more specific topic:")
                for i, option in enumerate(options):
                    speak(f"{i + 1}: {option}")
                try:
                    choice = int(takeCommand())
                    if 1 <= choice <= len(options):
                        new_query = options[choice - 1]
                        results = wikipedia.summary(new_query, sentences=2)
                        speak("According to Wikipedia")
                        print(results)
                        speak(results)
                    else:
                        speak("Invalid choice. Please try again.")
                except ValueError:
                    speak("Invalid input. Please provide a valid choice.")
                except Exception as ex:
                    speak("An error occurred. Please try again.")
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("https://www.stackoverflow.com")
        elif 'play music' in query:
            music_dir = 'D:\\songs\\Favorite'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'stop' in query:
            speak("Goodbye!")
            break