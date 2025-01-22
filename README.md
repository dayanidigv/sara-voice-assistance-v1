
# **Sara Voice Assistance v1**

Sara is a voice-activated assistant that can perform various tasks such as responding to queries, controlling system settings, web searches, telling jokes, and more. This project demonstrates the integration of voice recognition, text-to-speech, and automation tools.

---

## **Features**
- **Voice Recognition**: Uses speech-to-text capabilities to understand user commands.
- **Text-to-Speech**: Responds to user commands with a natural-sounding voice.
- **Web Search**: Searches Google or YouTube based on user input.
- **System Control**: Adjusts system brightness, volume, and schedules shutdowns.
- **File Operations**: Creates files and directories, and opens specific applications.
- **Fun Features**: Tells jokes, retrieves weather info (requires API key), and more.
- **Notification Support**: Displays notifications for non-critical events.
- **Error Handling**: Handles common errors like microphone or connectivity issues.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/dayanidigv/sara-voice-assistance-v1.git sara
cd sara
```

### **2. Install Dependencies**
Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required libraries:
```bash
pip install -r requirements.txt
```

### **3. Install `pyaudio` (if needed)**
On Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

---

## **Usage**

1. Run the script:
   ```bash
   python main.py
   ```
2. Say "Sara" to activate the assistant.
3. Use commands like:
   - **"What is the time?"**: Sara will tell you the current time.
   - **"Search YouTube for Python tutorials"**: Opens YouTube with the given search query.
   - **"Set system brightness level to 50%"**: Adjusts your system's brightness.
   - **"Tell me a joke"**: Sara will tell you a random joke.
   - **"Create file test.txt"**: Creates a text file named `test.txt`.

---

## **File Structure**
```
sara-voice-assistance/
│
├── main.py           # Main script
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
```

---

## **Technologies Used**
- **Python 3.10**: Core programming language.
- **SpeechRecognition**: For voice input.
- **pyttsx3**: For text-to-speech functionality.
- **Selenium**: For web automation.
- **PyAutoGUI**: For system control automation.
- **BeautifulSoup**: For web scraping.
- **Pillow**: For image processing.

---

## **Customizable Features**
- **API Integration**: Replace placeholders for weather or location APIs to enable real-time information retrieval.
- **Voice Commands**: Modify or add commands in the `data_model` dictionary.
- **GUI Improvements**: Enhance the existing tkinter-based interface.

---

## **Known Issues**
- **Microphone Compatibility**: Ensure your microphone is recognized and configured properly.
- **API Key Requirements**: For weather/location functionality, you need valid API keys.
- **System-Specific Limitations**: Some features are limited to Windows OS.

---

## **Contributing**
Feel free to contribute by:
- Adding new features.
- Fixing bugs or improving performance.
- Submitting suggestions or issues.

---

## **Acknowledgments**
- Inspired by personal assistants like Siri and Alexa.
- Built with Python's robust libraries for automation and voice processing.
