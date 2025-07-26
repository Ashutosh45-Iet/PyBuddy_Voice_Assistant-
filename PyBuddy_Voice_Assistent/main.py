import warnings
warnings.filterwarnings("ignore")                  # Suppress unnecessary warning messages

import pyttsx3  # type: ignore                      # Text-to-speech engine
import os
import speech_recognition as sr  # type: ignore      # Speech recognition (Google API)
import random                                         # For random song selection
import webbrowser                                   # To open URLs in browser
import datetime
from plyer import notification # type: ignore
import pyautogui # type: ignore
import wikipedia # type: ignore
import pywhatkit as pwk # type: ignore
import user_config
import smtplib,ssl
import requests
from bs4 import BeautifulSoup



#print(user_config.gmail_password)

#exit()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)               # Use default voice (male); use voices[1].id for female
engine.setProperty('rate', 160)                         # Set speaking rate

# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    

# Function to recognize and return user voice input
def command():
    content = " "
    while content == " ":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎧 Listening to your question...")  
            r.pause_threshold=1
            r.energy_threshold=300
            audio = r.listen(source,0,4)

        try:
            print("Understanding.....")
            content = r.recognize_google(audio, language='en-in')
            print("You said: " + content)
        except Exception as e:
            print("Please try again...")

    return content


# Main function to process and respond to user commands
def main_process():
    Pybuddy_chat = []  # ✅ Declare the variable at the very start
    while True:
        request = command().lower()
        
        # Greet the user   
        if 'hello' in request:
            speak("Welcome, how can I help you?")

        # 1.Play random music from YouTube
        elif 'play music' in request:
            speak('Playing music')
            song = random.randint(1, 5)
            if song == 1:
                webbrowser.open("https://www.youtube.com/watch?v=iUqPfGlg9GQ")
            elif song == 2:
                webbrowser.open("https://www.youtube.com/watch?v=lFdSi01tpYM")
            elif song == 3:
                webbrowser.open("https://www.youtube.com/watch?v=XWKazQwFFdY")
            elif song == 4:
                webbrowser.open("https://www.youtube.com/watch?v=kUhpQL87z3c")
            elif song == 5:
                webbrowser.open("https://www.youtube.com/watch?v=FMyziKCVFQ4")
                
        # 2.Report current time
        elif 'say time' in request:
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is " + str(now_time))

        #3. Report current date
        elif 'say date' in request:
            now_date = datetime.datetime.now().strftime("%d:%m:%Y")
            speak("Current date is " + str(now_date))

        # 4.Add a new task to TODO list
        elif 'new task' in request:
            task = request.replace("new task", "").strip()
            if task != "":
                speak("Adding task: " + task)
                with open("todo.txt", "a") as file:
                    file.write(task + "\n")

        #5.Speak out the saved tasks
        elif 'speak task' in request:
            with open("todo.txt", "r") as file:
                speak("Work we have to do today is: " + file.read())

        #6. Show a desktop notification of tasks
        elif 'show work' in request:
            with open("todo.txt", "r") as file:
                task = file.read()
                notification.notify(
                    title="Today's work",
                    message=task
                )
        
        elif 'open youtube' in request:
            webbrowser.open("https://www.youtube.com/")         

        # 7.Open an application using its name form desktop search bar
        elif 'open' in request:
            query = request.replace("open", "").strip()
            pyautogui.press("super")  # Press Windows key
            pyautogui.typewrite(query)  # Type the app name
            pyautogui.sleep(2)
            pyautogui.press("enter")  # Launch the app
        
        # Take a screenshot and save it with a timestamp
        elif 'take screenshot' in request:
            speak("Taking screenshot...")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            speak(f"Screenshot saved as {filename}")
               
            
        # If the user request contains 'wikipedia'
        elif 'wikipedia' in request:
            request = request.replace("PyBuddy", "")                    
            request = request.replace("search wikipedia", "")          # Remove "search wikipedia" phrase
            result = wikipedia.summary(request, sentences=2)           # Get a 2-sentence summary from Wikipedia
            print(result)                                             
            speak(result)                                             

        # If the user wants to search on Google
        elif 'search google' in request:
            request = request.replace("PyBuddy", "")                    # Clean the request
            request = request.replace("search google", "")             # Remove "search google" phrase
            webbrowser.open("https://www.google.com/search?q=" + request)  # Open Google search with query
            
        # If the user wants to send a WhatsApp message
        elif 'send whatsapp' in request:
            now = datetime.datetime.now()                            
            hour = now.hour
            minute = now.minute + 1                                   
            if minute >= 60:                                 # Handle case when minutes overflow
                hour += 1
                minute -= 60
            pwk.sendwhatmsg("+919721121463", "Hi, How are you", hour, minute)  # Send WhatsApp message using pywhatkit

        # If the user wants to send an email (SMTP approach)
        elif 'send email' in request:
            s = smtplib.SMTP('smtp.gmail.com', 587)                   
            s.starttls()                                               
            s.login("ashutosh.upsidc@gmail.com", user_config.gmail_password)  # Login using sender's email and password
            message = """
            this is message for fee submission of your college

            Thank you for your response
            """
            s.sendmail("ashutosh.upsidc@gmail.com", "yadavaryan1280@gmail.com", message) 
            s.quit()                                                
            speak("email sent successfully")                        

        # If the user asks for image generation
        elif "image" in request:
            request = request.replace("PyBuddy ", "")                  
            image_generation.generate_image(request)                   # type: ignore # Generate image based on request

        # If the user wants to chat with AI
        elif "ask ai" in request:
            Pybuddy_chat = []                                          
            request = request.replace("PyBuddy ", "")                 
            request = request.replace("ask ai ", "")                  
            Pybuddy_chat.append({"role": "user", "content": request})   # Add user query to chat history
            response = ai.send_request(Pybuddy_chat)                    # type: ignore # Send query to AI model
            speak(response)

        # If the user wants to clear the chat history
        elif "clear chat" in request:
            _chat = []                                           
            speak("Chat Cleared")                                    

        # Default fallback: send user query to AI
        else:
            request = request.replace("PyBuddy ", "")                 
            Pybuddy_chat.append({"role": "user", "content": request})  
            response = ai.send_request(Pybuddy_chat)                    # type: ignore # Get AI response
            Pybuddy_chat.append({"role": "assistant", "content": response})  # Save assistant response
            speak(response)                                            # Speak out the AI's response


 # Start the voice assistant
if __name__ == "__main__":
    main_process()     
        
        

    
               
