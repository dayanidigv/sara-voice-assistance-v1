import os
import webbrowser
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime as dt
import pyttsx3
import speech_recognition as sr
import requests
import random
import wikipedia
import threading
import time as t
import subprocess
import socket
import platform
import pyautogui as py
import json
import plyer 
import win32api
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab
from tqdm import tqdm
import screen_brightness_control as sc
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyjokes
try:
    import winerror
except ImportError or ModuleNotFoundError:
    pass
import keyboard as key
from bs4 import BeautifulSoup

osname = platform.system()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Create a threading Event
stop_event = threading.Event()

# Define the voice assistant's name
assistant_name = "sara"

# Define Female Voice
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
engine.setProperty('volume', 2.7)
engine.setProperty('voice', voices[1].id)

# Create the GUI window
window = tk.Tk()
window.title("Sara")
window.geometry("400x100")

# Create progress bar and label
progress_bar = ttk.Progressbar(window, length=300, mode="determinate")
progress_bar.pack(pady=20)

progress_label = tk.Label(window, text="Scanning", font=("Arial", 12))
progress_label.pack()

# Define current time
current_time = dt.datetime.now()
h = current_time.hour
m = current_time.minute
s = current_time.second

# Set up Chrome options for running in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the Chrome webdriver using the headless options
driver = webdriver.Chrome(options=chrome_options)

# Set up for control System Volume 
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Data model for reply
data_model = {
            "hi": "Hello, How can I assist you today?",
            "hello": "Hi, How can I help you?",
            "thank you": "You're welcome!",
            "thanks": "You're welcome!",
            "good": "That's great to hear! How can I assist you further?",
            "good morning": "Good morning! How can I assist you?",
            "good night": "Good night! Sweet dreams!",
            "good afternoon": "Good afternoon! How can I assist you?",
            "how are you": "I'm doing well, thank you! How can I assist you?",
            "what's your name": "My name is Sara. How can I assist you?",
            "i like you": "Thank you! I'm here to help you.",
            "i love you": "Thank you for your kind words! I'm here to assist you.",
            "i am glad": "I'm glad to hear that! How can I assist you today?",
            "how can I help": "I'm here to assist you. How can I help you today?",
            "tell me more": "Sure! What specific information are you looking for?",
            "please assist me": "Of course! I'm here to assist you. What do you need help with?",
            "can you help me?": "Absolutely! I'm here to help. What do you need assistance with?",
            "what's your purpose?": "My purpose is to assist and provide information. How can I help you?",
            "what can you do?": "I can help answer questions, provide information, and assist with various tasks. How can I assist you today?",
            "how does it work?": "I work by analyzing and understanding your queries and providing relevant responses. How can I assist you?",
            "where are you from?": "I'm an AI language model developed by OpenAI. How can I assist you today?",
            "who created you?": "I was created by a team of engineers and researchers at OpenAI. How can I assist you?",
            "do you have any hobbies?": "As an AI, I don't have personal hobbies, but I enjoy assisting and providing information. How can I assist you today?",
            "what languages do you speak?": "I can communicate and assist in now only English. How can I assist you?",
            "how old are you?": "I'm an AI, so I don't have an age.",
            "what is your favorite color?": "As an AI, I don't have personal preferences.",
            "where can I find support?": "If you need support, you can reach out to our customer service team at dayanidiportfolio.github.io .",
            "what is the meaning of life?": "The meaning of life can vary for each person. It's a philosophical question that has different interpretations.",
            "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
            "what is the weather like today?": "I'm sorry, but I don't have access to real-time weather information.",
            "how do I reset my password?": "To reset your password, go to the login page and click on the 'Forgot Password' link. Follow the instructions to reset your password.",
            "can you recommend a good restaurant nearby?": "I'm sorry, but I don't have access to location-specific information. You can try using a local search engine or review website for restaurant recommendations.",
            "what is the capital of France?": "The capital of France is Paris.",
            "how do I delete my account?": "To delete your account, go to your account settings and look for the option to delete or deactivate your account. Follow the provided instructions.",
            "what is the latest news?": "I don't have real-time access to news updates. You can check news websites or apps for the latest news.",
            "what are your thoughts on artificial intelligence?": "As an AI, I don't have personal thoughts or opinions.",
            "can you play music?": "I'm sorry, but I don't have the capability to play music.",
            "how can I improve my programming skills?": "To improve your programming skills, you can practice regularly, work on projects, and explore online resources such as tutorials, courses, and forums.",
            "tell me a fun fact": "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
            "what is the meaning of happiness?": "The meaning of happiness can vary from person to person. It is often described as a state of well-being, contentment, or joy.",
            "how can I improve my productivity?": "To improve productivity, you can try strategies like setting goals, prioritizing tasks, minimizing distractions, and practicing time management techniques.",
            "what is the best way to learn a new language?": "The best way to learn a new language may vary for each individual. Some effective methods include immersion, taking classes, practicing with native speakers, and using language-learning apps or resources.",
            "how can I stay motivated?": "To stay motivated, you can set clear goals, break tasks into smaller steps, celebrate achievements, seek support from others, and find inspiration in things you enjoy.",
            "can you recommend a good book to read?": "Sure! What genre or topic are you interested in?",
            "how can I start a career in [specific field]?": "Starting a career in [specific field] typically involves gaining relevant education, acquiring practical experience, networking, and staying updated with industry trends and developments.",
            "what are some healthy eating tips?": "Some healthy eating tips include consuming a balanced diet with plenty of fruits, vegetables, whole grains, lean proteins, and healthy fats, staying hydrated, and moderating the intake of sugary and processed foods.",
            "how do I create a budget?": "To create a budget, you can start by tracking your income and expenses, categorizing your expenses, setting financial goals, and allocating your income accordingly. There are also various budgeting apps and tools available to assist you.",
            "what are the best practices for data security?": "Some best practices for data security include using strong and unique passwords, enabling two-factor authentication, keeping software and devices updated, being cautious of phishing attempts, and regularly backing up important data.",
            "what are some effective study techniques?": "Effective study techniques include breaking study sessions into manageable chunks, actively engaging with the material through summarizing or teaching it to someone else, utilizing mnemonic devices or visualization techniques, and practicing retrieval through self-quizzing.",
            "how do I overcome procrastination?": "To overcome procrastination, you can try strategies like breaking tasks into smaller, more manageable parts, setting deadlines and using a planner or to-do list, finding accountability partners, and recognizing and addressing underlying reasons for procrastination.",
        }

# Function to Send Notification
def notification(title,message):
     plyer.notification.notify(title=title,message=message , app_name='Sara', timeout=1)

# Function to Get Available Drives in System
def get_available_drives():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives

# Function to speak the assistant's response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
sayConnection = False
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
            audio = r.listen(source)  # Listen for input
        try:
            print("Recognizing...")
            return r.recognize_google(audio, language='en')
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
    except OSError as e:
        print(f"Microphone error: {e}")
        return None

    

def search_dir(dir_name):
    pass

# Function to Scan full System to get Files Location Information and store them in a JSON file
def scanSystem():
    if os.path.exists(os.path.join(os.getcwd(),"sysytemPath")) == False:
        os.mkdir(os.path.join(os.getcwd(),"systemPath"))
    def on_close():
        window.destroy()
    exefile = []
    imagefile = []
    videofile = []
    musicfile = []
    allDir = []
    available_drives = get_available_drives()
    if available_drives:
        progress_bar["maximum"] = len(available_drives)
        for idx, drive in enumerate(available_drives, start=1):
            progress_bar["value"] = idx
            progress_label["text"] = f"Scanning Drive {idx}/{len(available_drives)}"
            window.update()
            for path, dirs, files in tqdm(os.walk(drive), desc="Scanning"):
                for dir in dirs:
                    Path = os.path.join(path, dir)
                    allDir.append({"name": dir, "path": Path})
                for file in files:
                    if file.endswith(".exe"):
                        file_path = os.path.join(path, file)
                        exefile.append({"name": file.replace(".exe", ""), "path": file_path})
                    elif file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".tief", ".raw")):
                        file_path = os.path.join(path, file)
                        imagefile.append({"name": file, "path": path})
                    elif file.lower().endswith((".mp4", ".mov", ".wmv", "flv")):
                        file_path = os.path.join(path, file)
                        videofile.append({"name": file, "path": path})
                    elif file.lower().endswith((".mp3", ".ogg", ".aac", ".wav")):
                        file_path = os.path.join(path, file)
                        musicfile.append({"name": file, "path": path})

    if exefile:
        with open(os.path.join(os.getcwd(), "systemPath", "exefile_paths.json"), "w") as f:
            json.dump(exefile, f, indent=4)

    if imagefile:
        with open(os.path.join(os.getcwd(), "systemPath", "imagefile_paths.json"), "w") as f:
            json.dump(imagefile, f, indent=4)

    if videofile:
        with open(os.path.join(os.getcwd(), "systemPath", "videofile_paths.json"), "w") as f:
            json.dump(videofile, f, indent=4)

    if musicfile:
        with open(os.path.join(os.getcwd(), "systemPath", "musicfile_paths.json"), "w") as f:
            json.dump(musicfile, f, indent=4)

    progress_label["text"] = f"Scanning Completed"
    # Start the GUI event loop
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()

# Get All .exe Files Location Information json file
def readJsonFile(file):
    try:
        with open( os.path.join(os.getcwd(),"systemPath", file), "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        speak("Do you want to initiate scanning?")
        confirmation = py.confirm(text="Do you want to initiate a scan?", title="Sara - Scan Confirmation")
        if confirmation == "OK":
            speak("initiate scanning...Please wait")
            scanSystem()
            with open( os.path.join(os.getcwd(),"systemPath", file), "r") as f:
                data = json.load(f)
            return data
        else:
            speak("Permission denied")

#Gives Information on the Topic in wikipedia
def information(topic, lines = 5):
    data = wikipedia.summary(topic, sentences=lines)
    return data

# function to web scrapping to get information
def Question(user_query):
    URL = "https://www.google.co.in/search?q=" + user_query

    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        result = soup.find(class_='hgKElc').get_text()
    except:
        try:
            result = soup.find(class_='kno-rdesc').get_text()
        except:
            return False
    result =  remove_key(["Description", " Wikipedia"],result)
    return result

# Function to Gathering Information
def info(query):
    query = remove_key(["tell","me"], query )
    speak("Information gathering...")
    print((query))
    result = Question(query)
    if(result == False):
        result = get_wikipedia_summary(query)
    print(result)
    speak(result)

# Get  Information in Wikipedia 
def get_wikipedia_summary(title):
    try:
        page = wikipedia.page(title)
        summary = page.summary
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        # If the title is ambiguous, you can handle the exception here
        print("Title is ambiguous. Please provide a more specific title.")
    except wikipedia.exceptions.PageError as e:
        # If the page is not found, you can handle the exception here
        print("Page not found. Please check the title.")

# Function to Search in google
def search(topic: str) -> None:
    speak("Searching...")
    if "youtube" in topic:
        topic = remove_key(["youtube", "open", "search"], topic) 
        webbrowser.open(f"https://www.youtube.com/results?search_query={topic}")
    else:
        webbrowser.open(f"https://www.google.com/search?q={topic}")

# Function to check internet connection
def check_internet_connection():
    try:
        # Create a socket connection to Google DNS (8.8.8.8) on port 53
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# Function to Schedules a Shutdown after the Specified Time
def shutdown(time = 20):
    if "window" in osname.lower():
        cont = f"shutdown -s -t {time}"
        error_code = os.system(cont)
        if error_code in [winerror.ERROR_SHUTDOWN_IN_PROGRESS, 1115]:
            speak("A Shutdown Process has already been Scheduled!")
        else:
            speak(f"Your System will Shutdown in {time} Seconds!")
    else:
        speak(f"Available on Windows only, can't Execute on {osname}")

# Function to Cancels the Scheduled Shutdown
def cancel_shutdown():
    if "window" in osname.lower():
        error_code = os.system("shutdown /a")
        if error_code == winerror.ERROR_NO_SHUTDOWN_IN_PROGRESS:
            speak("Shutdown Cancellation process has been Aborted! [NO Shutdown Scheduled]")
        else:
           speak("Shutdown has been Cancelled!")
    else:
        speak(f"Available on Windows only, can't Execute on {osname}")

#Play a YouTube Video
def play_youtube(topic):
    url = f"https://www.youtube.com/results?q={topic}"
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == "WEB_PAGE_TYPE_WATCH":
            break
    if lst[count - 5] == "/results":
        raise Exception("No Video Found for this Topic!")
    webbrowser.open(f"https://www.youtube.com{lst[count - 5]}")

#Take Screenshot of Any Website Without Opening it
def web_screenshot():
    speak("Enter Website link")
    link = py.prompt(text="Enter Website link", title="Sara",)
    driver.get(f"https://{link}")
    current_time = int(t.time())
    filename = f"screenshot_{current_time}.png"
    driver.save_screenshot(filename)
    os.startfile(filename)
    driver.quit()

# Function to open a file or directory
def open_file(file_path):
    if os.path.exists(file_path):
        os.startfile(file_path)
    else:
        speak("Sorry, I couldn't find the specified file or directory.")

# Function to get the current time
def get_time():
    current_time = dt.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

# Function to create a file
def create_file(file_name):
    try:
        with open(file_name, 'w') as f:
            speak("File created successfully.")
    except Exception as e:
        speak("Sorry, I couldn't create the file.")

# Function to create a file in a specific path
def create_file_in_path(file_name, path):
    try:
        file_path = os.path.join(path, file_name)
        with open(file_path, 'w') as f:
            speak("File created successfully.")
    except Exception as e:
        speak("Sorry, I couldn't create the file.")

# Function to greet
def greet():
    if 0 <= h <= 11:
        speak("Good morning")
    elif 12 <= h <= 16:
        speak("Good Afternoon")
    elif 17 <= h <= 19:
        speak("Good Evening")
    else:
        speak("Welcome")
    speak("This is Sara, How can i help you.")

# Function to open a comment editor like Notepad
def open_comment(open_query):
    open_query = open_query.lower()
    try:
        if any(keyword in open_query for keyword in ["type", "write"]):
            open_query = open_query.replace(("type", "write"), "").strip()
            if "notepad" in open_query:
                subprocess.call(["notepad.exe"])
        else:
            file_name = None
            if "youtube" in open_query:
                if "play" in open_query:
                    search_query = remove_key(["play youtube", "open youtube", "youtube","play","open"], open_query)
                    play_youtube(search_query)
                else:
                    webbrowser.open(r"https://www.youtube.com/")
            elif "google" in open_query:
                webbrowser.open(r"https://google.com/")

            elif any(keyword in open_query for keyword in ["play youtube", "open youtube", "youtube"]):
                search_query = remove_key(["play youtube", "open youtube", "youtube"], open_query)
                play_youtube(search_query)

            elif "notepad" in open_query: file_name = "Notepad"

            elif "notepad++" in open_query or "notepad ++" in open_query: file_name = "notepad++"

            elif "wordpad" in open_query: file_name = "wordpad"

            elif "whatsapp" in open_query or "whats app" in open_query : file_name = "WhatsApp"

            elif "telegram" in open_query: file_name = "Telegram"

            elif "postman" in open_query: file_name = "Postman"

            elif "blender" in open_query: file_name = "blender"

            elif "eclipse" in open_query: file_name = "eclipse"

            elif "spotify" in open_query: file_name = "Spotify"

            elif "music player" in open_query or "media player" in open_query:  file_name = "MediaPlayer"

            elif "video player" in open_query or "vlc" in open_query: file_name = "vlc"

            elif "photos" in open_query or "gallery" in open_query: file_name = "PhotosApp"

            elif "cmd" in open_query or "command prompt" in open_query : file_name = "cmd"

            elif "firefox" in open_query or "fire fox" in open_query: file_name = "firefox"

            elif "calculator" in open_query or "calci" in open_query: file_name = "CalculatorApp"

            elif "file explorer" in open_query or "file" in open_query or "folder" in open_query: file_name = "FileExplorer"

            elif "snipping tool" in open_query: file_name = "SnippingTool"

            elif "sound record" in open_query or "voice record" in open_query: file_name = "SoundRec"

            elif "map" in open_query and "google" not in open_query:  file_name = "Maps"

            elif "codeblocks" in open_query or "code blocks" in open_query: file_name = "codeblocks"

            elif "code" in open_query: file_name = "Code"

            elif "github desktop" in open_query:  file_name = "GitHubDesktop"

            elif "camera" in open_query: file_name = "WindowsCamera"

            elif "time" in open_query or "clock" in open_query: file_name = "Time"

            else:
                speak(f"{open_query} is not availeable.")
                
            if file_name:
                file_paths = readJsonFile("exefile_paths.json")
                try:
                    for file_info in file_paths:
                        if file_name == file_info["name"]:
                            os.startfile(file_info["path"])
                            break
                except:
                    speak("not open")
            
    except OSError as error:
        print(error)
        speak("File or path was not found.")

# Function to Remove Words in Query
def remove_key(keys,string):
    for key in keys:
        string = string.replace(key, '')
    return string.strip()

#Take Screenshot of the Screen
def take_screenshot(file_name = "pywhatkit_screenshot", delay = 1):
    speak(f"Take ScreenShot in {delay} seconds")
    t.sleep(delay)
    screen = ImageGrab.grab()
    screen.show(title=file_name)
    screen.save(f"{file_name}.png")

#Take Photho
def take_photo():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        speak("Failed to open the camera")
        return
    ret, frame = camera.read()
    if not ret:
        speak("Failed to capture frame")
        return
    # Save the captured frame as an image
    cv2.imwrite("captured_image.jpg", frame)
    camera.release()
    speak("Image captured successfully!")

#Take countdoun
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print("\r",str(i), end=" ")
        speak(str(i))
        t.sleep(0.9)

# Get integer value in String
def string_to_get_value(string):
    words = string.split(" ")
    numeric_value = None
    for word in words:
        if word.isdigit():
            numeric_value = int(word)
            return numeric_value  

# Function to Set Brightness 
def set_brightness(string):
    numeric_value = string_to_get_value(string)
    if numeric_value is not None:
        sc.set_brightness(value=numeric_value) 
        speak(f"Set System brightness level is {sc.get_brightness()} percentage")
    else:
        speak("System brightness level is not set")

# Datasets for set System volume
percentage_values = [
    (100, 0.0),
    (95, -0.7782278060913086),
    (90, -1.5984597206115723),
    (85, -2.4654886722564697),
    (80, -3.384982109069824),
    (75, -4.363698959350586),
    (70, -5.409796714782715),
    (65, -6.5332441329956055),
    (60, -7.746397495269775),
    (55, -9.064839363098145),
    (50, -10.508596420288086),
    (45, -12.10401439666748),
    (40, -13.886737823486328),
    (35, -15.906672477722168),
    (30, -18.236774444580078),
    (25, -20.989887237548828),
    (20, -24.35443115234375),
    (15, -28.681884765625),
    (10, -34.75468063354492),
    (5, -45.02272033691406),
    (0, -96.0)
]

# Function to convert percentage to volume level value
def convert_percentage_to_value(percentage):
    if percentage % 5 == 0:     # Value for percentages divisible by 5 is -0.7782278060913086
        for percent, value in percentage_values:
            if percent == percentage:
                return value
    else:
        percentage = percentage + (5 - (percentage % 5))
        for percent, value in percentage_values:
            if percent == percentage:
                return value

# Function to convert  volume level value to percentage
def convert_value_to_percentage(value):
    for percent, val in percentage_values:
        if val <= value:
            if val == value:
                return percent
            else:
                return percent + 2

# Function to Set System Volume
def set_volume(percentage):
    percent =  string_to_get_value(percentage)
    if percent is not None:
        volume.SetMasterVolumeLevel(convert_percentage_to_value(percent),None)
        speak(f"Set System volume level is {percent} percentage")
    else:
        speak("System Volume level is not set")

# Function to get Jokes
def jokes():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)

# Function Get ip lovation
def get_ip_location():
    url = 'https://api.myip.com/'
    try:
        response = requests.get(url)
        data = response.json()
        ip = data['ip']
        country = data['country']
        cc = data['cc']
        data = {"ip": ip, "country": country, "cc": cc}
        encoded_data = json.dumps(data)
        speak(f"your country is {country}.your ip is {ip}")
        return encoded_data
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve IP location:", str(e))

# Function to get location
def get_location():
    data = get_ip_location()
    api_key = 'df242c94d66143af90f6c7111f968d28'
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={data[0]}'
    try:
        response = requests.get(url)
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as e:
        speak("Failed to retrieve location information:", str(e))

# Function to Sleep Sara wake up with "windows" key + "/"" key
def sleep():
    speak("Press the 'Windows' key and '/' key together to wake me up.")
    while True:
        if key.is_pressed('left windows'):
            if key.is_pressed('/'):
                greet()
                break

greet()
speak(f"Please use the name {assistant_name} to access me.")

# Main program loop
while True:
    query = listen()
    if query:
        query = query.lower()

        if assistant_name in query or "tara" in query:
            query = query.replace(assistant_name, "").replace("tara", "").strip()

            if "exit" in query:
                speak("Program has stopped.")
                exit(0)

            elif 'search'  in query:
                search_query = query.replace('search', '').strip()
                search(search_query)

            elif any(keyword in query for keyword in ["info", "information", "about"]):
                search_query = remove_key(["info", "information", "about"], query)
                info(search_query)

            elif 'open' in query:
                open_query = query.replace('open', '').strip()
                open_comment(open_query)

            elif any(keyword in query for keyword in ["time", "current time", "time now", "timenow"]):
                get_time()

            elif 'create file' in query:
                file_name = query.replace('create file', '').strip()
                create_file(file_name)

            elif 'create file in' in query:
                file_name, path = query.replace('create file in', '').strip().split(',')
                create_file_in_path(file_name.strip(), path.strip())

            elif any(keyword in query for keyword in ["play youtube", "open youtube", "youtube"]):
                search_query = remove_key(["play youtube", "open youtube", "youtube"], query)
                play_youtube(search_query)

            elif any(keyword in query for keyword in ["system screenshot", "take screenshot","takes screenshot"]):
                take_screenshot()

            elif any(keyword in query for keyword in ["take photo", "take picture","takes photos","takes image","take images"]):
                take_photo()

            elif any(keyword in query for keyword in ["web screenshot", "take web screenshot", "website screenshot", "take website screenshot"]):
                web_screenshot()

            elif any(keyword in query for keyword in ["shutdown", "system shutdown", "shutdown system"]):
                time = remove_key(["shutdown", "system shutdown", "shutdown system"], query)
                shutdown()

            elif any(keyword in query for keyword in ["cancel shutdown", "shutdown cancel"]):
                cancel_shutdown()

            elif any(keyword in query for keyword in ["countdown", "set countdown"]):
                seconds = remove_key(["countdown", "set countdown", "seconds"], query)
                countdown(int(seconds)) if seconds != "" else countdown(10)

            elif any(keyword in query for keyword in ["tell a joke", "joke"]):
                jokes()

            elif any(keyword in query for keyword in ["get my location", "my location","location"]):
                get_ip_location()
            
            elif any(keyword in query for keyword in ["set system brightness level", "set brightness level", "change system brightness level", "change brightness level"]):
                string = remove_key(["set system brightness level", "set brightness level", "change system brightness level", "change brightness level","percentage","in","%"], query)
                set_brightness(string)
            
            elif any(keyword in query for keyword in ["set system volume level", "set volume level", "change system volume level", "change volume level","set system volume level", "set sound level", "change system sound level", "change sound level"]):
                string = remove_key(["set system volume level", "set volume level", "change system volume level", "change volume level","set system volume level", "set sound level", "change system sound level", "change sound level","percentage","in","%"], query)
                set_volume(string)
            elif any(keyword in query for keyword in ["system brightness level", "brightness level", "get system brightness level", "get brightness level"]):
                speak(f"System brightness level is {sc.get_brightness()} percentage")

            # Add more keyword conditions here
            elif any(keyword in query for keyword in ["bye", "goodbye", "good bye"]):
                speak("Goodbye, Take care.")
                sleep()

            else:
                for data in data_model:
                    if query in data:
                        speak(data_model[data])
                        break
                else:
                    speak("Sorry, I didn't understand that.")
            

        else:
            notification(title="You Say",message=query)
