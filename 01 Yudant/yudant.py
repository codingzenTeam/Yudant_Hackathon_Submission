from bardapi import Bard

import pyttsx3

import speech_recognition as sr

import datetime

import subprocess

import webbrowser




def initialize_speech_engine():

    engine = pyttsx3.init()

    engine.setProperty('rate', 180)

    return engine




def listen_for_speech():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        audio = recognizer.listen(source)

    try:

        print("Recognizing...")

        text = recognizer.recognize_sphinx(audio)

        print("You said:", text)

        return text

    except sr.UnknownValueError:

        print("Unable to recognize speech")

        return ""

    except sr.RequestError as e:

        print("Error:", str(e))

        return ""




def get_bard_response(token, text):

    bard = Bard(token=token)

    response = bard.get_answer(text)['content']

    return response




def speak_response(engine, response):

    print("robot -> " + response)

    engine.say(response)

    engine.runAndWait()

    engine.stop()




def greet():

    current_time = datetime.datetime.now().time()

    if current_time < datetime.time(12):

        greeting = "Good morning!"

    elif current_time < datetime.time(17):

        greeting = "Good afternoon!"

    else:

        greeting = "Good evening!"

    return greeting




def open_application(application_name):

    subprocess.call(["open", "-a", application_name])




def open_website(website, browser=None):

    url = f"https://www.{website}.com"

    if browser:

        webbrowser.get(browser).open(url)

    else:

        webbrowser.open(url)




def run_voice_assistant():

    token = 'WQj3v6PlhIPeIdlOP3thF367Cz4ETfd4r6wuYIiCKtmHenWigaiUymhUo24WqZATtsMXSw.'

    engine = initialize_speech_engine()




    greeting = greet()

    

    speak_response(engine, greeting)




    while True:

        use_speech_recognition = input("Do you want to use speech recognition? (y/n): ")

        

        if use_speech_recognition.lower() == 'y':

            text = listen_for_speech()

        else:

            text = input("Enter your command: ")

        

        if text:

            print("human -> " + text)

            if text.startswith("open website"):

                command = text[12:].strip()

                if "on" in command:

                    website, browser = command.split("on")

                    website = website.strip()

                    browser = browser.strip()

                    open_website(website, browser)

                    response = f"Opening {website} on {browser}"

                else:

                    open_website(command)

                    response = f"Opening {command}"

            elif text.startswith("open"):

                application_name = text[5:].strip()

                open_application(application_name)

                response = f"Opening {application_name}"

            else:

                response = get_bard_response(token, text)

            speak_response(engine, response)

            

        if engine._inLoop:

            engine._endLoop




run_voice_assistant()
