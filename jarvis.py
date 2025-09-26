import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import requests
import datetime
import webbrowser
import os

# For ChatGPT integration
import openai

# Set your OpenAI API key here (hardcoded for immediate use)
OPENAI_API_KEY = "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"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set to male voice (e.g., Microsoft David)
engine.setProperty('rate', 150)  # Speed of speech

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for voice commands and convert to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=30)
        except sr.WaitTimeoutError:
            speak("Listening timed out. Please try again.")
            return ""
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-in').lower()
            print(f"You said: {command}")
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Please repeat.")
            return ""
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return ""
        return command

def process_command(command):
    # Support 'open [ai tool] and search [query]' command
    import re
    open_search_match = re.match(r"open ([\w .-]+) and search (.+)", command)
    if open_search_match:
        tool = open_search_match.group(1).strip().lower()
        query = open_search_match.group(2).strip()
        ai_tool_urls = {
            "gemini": "https://gemini.google.com/",
            "google gemini": "https://gemini.google.com/",
            "claude": "https://claude.ai/",
            "claude ai": "https://claude.ai/",
            "perplexity": "https://www.perplexity.ai/",
            "perplexity ai": "https://www.perplexity.ai/",
            "copilot": "https://github.com/features/copilot",
            "github copilot": "https://github.com/features/copilot",
            "poe": "https://poe.com/",
            "poe ai": "https://poe.com/",
            "hugging face": "https://huggingface.co/",
            "huggingface": "https://huggingface.co/",
            "deepl": "https://www.deepl.com/",
            "deep l": "https://www.deepl.com/",
            "you.com": "https://you.com/",
            "you ai": "https://you.com/",
            "blackbox ai": "https://www.blackbox.ai/",
            "chatgpt": "https://chat.openai.com/",
            "openai": "https://openai.com/",
            "google": "https://www.google.com/",
            "youtube": "https://www.youtube.com/"
        }
        search_urls = {
            "google": f"https://www.google.com/search?q={query.replace(' ', '+')}",
            "perplexity": f"https://www.perplexity.ai/search?q={query.replace(' ', '+')}",
            "you.com": f"https://you.com/search?q={query.replace(' ', '+')}",
            "youtube": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        }
        url = ai_tool_urls.get(tool)
        search_url = search_urls.get(tool)
        if url:
            speak(f"Opening {tool.title()} home page")
            webbrowser.open(url)
        if search_url:
            speak(f"Searching {tool.title()} for {query}.")
            webbrowser.open_new_tab(search_url)
            return f"Opened {tool.title()} and searched for '{query}'."
        elif url:
            return f"Opened {tool.title()} home page, but search is not supported."
        else:
            speak(f"Sorry, I don't know the homepage for {tool}.")
            return f"Sorry, I don't know the homepage for {tool}."
    # Generic: open any AI tool by name
    import re
    open_match = re.match(r"open ([\w .-]+)", command)
    if open_match:
        tool = open_match.group(1).strip().lower()
        ai_tool_urls = {
            "gemini": "https://gemini.google.com/",
            "google gemini": "https://gemini.google.com/",
            "claude": "https://claude.ai/",
            "claude ai": "https://claude.ai/",
            "perplexity": "https://www.perplexity.ai/",
            "perplexity ai": "https://www.perplexity.ai/",
            "copilot": "https://github.com/features/copilot",
            "github copilot": "https://github.com/features/copilot",
            "poe": "https://poe.com/",
            "poe ai": "https://poe.com/",
            "hugging face": "https://huggingface.co/",
            "huggingface": "https://huggingface.co/",
            "deepl": "https://www.deepl.com/",
            "deep l": "https://www.deepl.com/",
            "you.com": "https://you.com/",
            "you ai": "https://you.com/",
            "blackbox ai": "https://www.blackbox.ai/",
            "chatgpt": "https://chat.openai.com/",
            "openai": "https://openai.com/",
            "google": "https://www.google.com/",
            "youtube": "https://www.youtube.com/"
        }
        url = ai_tool_urls.get(tool)
        if url:
            speak(f"Opening {tool.title()} home page")
            webbrowser.open(url)
            return f"Opening {tool.title()} home page."
        else:
            speak(f"Sorry, I don't know the homepage for {tool}.")
            return f"Sorry, I don't know the homepage for {tool}."

    # Generic: search in any AI tool (where possible)
    search_match = re.match(r"search (.+) in ([\w .-]+)", command)
    if search_match:
        query = search_match.group(1).strip()
        tool = search_match.group(2).strip().lower()
        # Only support Google, Perplexity, You.com, and YouTube for direct search
        search_urls = {
            "google": f"https://www.google.com/search?q={query.replace(' ', '+')}",
            "perplexity": f"https://www.perplexity.ai/search?q={query.replace(' ', '+')}",
            "you.com": f"https://you.com/search?q={query.replace(' ', '+')}",
            "youtube": f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        }
        url = search_urls.get(tool)
        if url:
            speak(f"Searching {tool.title()} for {query}.")
            webbrowser.open_new_tab(url)
            return f"Searching {tool.title()} for {query}."
        else:
            speak(f"Sorry, I can't search in {tool} automatically.")
            return f"Sorry, I can't search in {tool} automatically."
    # Open Gemini AI home page
    if 'open gemini' in command or 'open google gemini' in command:
        speak("Opening Google Gemini home page")
        webbrowser.open("https://gemini.google.com/")
        return "Opening Google Gemini home page."

    # Open Claude AI home page
    elif 'open claude' in command or 'open claude ai' in command:
        speak("Opening Claude AI home page")
        webbrowser.open("https://claude.ai/")
        return "Opening Claude AI home page."

    # Open Perplexity AI home page
    elif 'open perplexity' in command or 'open perplexity ai' in command:
        speak("Opening Perplexity AI home page")
        webbrowser.open("https://www.perplexity.ai/")
        return "Opening Perplexity AI home page."

    # Open GitHub Copilot home page
    elif 'open copilot' in command or 'open github copilot' in command:
        speak("Opening GitHub Copilot home page")
        webbrowser.open("https://github.com/features/copilot")
        return "Opening GitHub Copilot home page."

    # Open Poe AI home page
    elif 'open poe' in command or 'open poe ai' in command:
        speak("Opening Poe AI home page")
        webbrowser.open("https://poe.com/")
        return "Opening Poe AI home page."

    # Open Hugging Face home page
    elif 'open hugging face' in command or 'open huggingface' in command:
        speak("Opening Hugging Face home page")
        webbrowser.open("https://huggingface.co/")
        return "Opening Hugging Face home page."

    # Open DeepL home page
    elif 'open deepl' in command or 'open deep l' in command:
        speak("Opening DeepL home page")
        webbrowser.open("https://www.deepl.com/")
        return "Opening DeepL home page."

    # Open You.com home page
    elif 'open you.com' in command or 'open you ai' in command:
        speak("Opening You.com AI home page")
        webbrowser.open("https://you.com/")
        return "Opening You.com AI home page."

    # Open Blackbox AI home page
    elif 'open black box ai' in command:
        speak("Opening Blackbox AI home page")
        webbrowser.open("https://www.blackbox.ai/")
        return "Opening Blackbox AI home page."
    # Remove 'jarvis' from command if present
    command = command.replace('jarvis', '').strip()

    # Explain how AI works
    if command.strip() in ["how does ai work", "how ai work", "how to ai work", "explain ai"]:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Explain how artificial intelligence works in simple terms."}]
            )
            answer = response.choices[0].message.content.strip()
            speak(answer)
            return answer
        except Exception as e:
            speak("Sorry, I couldn't get a response from ChatGPT.")
            return f"Error: {e}"

    # Explain how any AI type works
    elif command.startswith("how does") and "work" in command:
        ai_type = command.replace("how does", "").replace("work", "").strip()
        if not ai_type:
            speak("Please specify the AI type you want to know about.")
            return "Please specify the AI type you want to know about."
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Explain how {ai_type} works in simple terms."}]
            )
            answer = response.choices[0].message.content.strip()
            speak(answer)
            return answer
        except Exception as e:
            speak("Sorry, I couldn't get a response from ChatGPT.")
            return f"Error: {e}"
    # Search and play song on YouTube
    elif command.startswith('search this song') or command.startswith('search song'):
        song = command.replace('search this song', '', 1).replace('search song', '', 1).strip()
        if not song:
            speak("Please specify the song name to play.")
            return "Please specify the song name to play."
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube."
    # Close the current browser tab (Windows only)
    elif 'close the tab' in command or 'close tab' in command:
        try:
            import pyautogui
            pyautogui.hotkey('ctrl', 'w')
            speak("Closing the current tab.")
            return "Closing the current tab."
        except ImportError:
            speak("pyautogui is not installed. Please install it to enable tab closing.")
            return "pyautogui is not installed. Please install it to enable tab closing."
        except Exception as e:
            speak(f"Failed to close the tab: {e}")
            return f"Failed to close the tab: {e}"
    # Remove 'jarvis' from command if present
    command = command.replace('jarvis', '').strip()

    # Search command: open a new tab and answer using ChatGPT
    if command.startswith('search ') or command.startswith('search this '):
        query = command.replace('search', '', 1).strip()
        if not query:
            speak("Please specify what you want to search for.")
            return "Please specify what you want to search for."
        # Open Google search in a new tab
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open_new_tab(url)
        speak(f"Searching Google for {query}.")
        # Get a short answer from ChatGPT as well
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Answer this as briefly as possible: {query}"}]
            )
            answer = response.choices[0].message.content.strip()
            speak(answer)
            return f"Google search opened for '{query}'. AI answer: {answer}"
        except Exception as e:
            return f"Google search opened for '{query}', but AI answer failed: {e}"

    # Open ChatGPT home page
    if 'open chatgpt' in command or 'open chat gpt' in command:
        speak("Opening ChatGPT home page")
        webbrowser.open("https://chat.openai.com/")
        return "Opening ChatGPT home page."

    # Open Google Gemini home page
    elif 'open gemini' in command or 'open google gemini' in command:
        speak("Opening Google Gemini home page")
        webbrowser.open("https://gemini.google.com/")
        return "Opening Google Gemini home page."

    # Open Claude AI home page
    elif 'open claude' in command or 'open claude ai' in command:
        speak("Opening Claude AI home page")
        webbrowser.open("https://claude.ai/")
        return "Opening Claude AI home page."

    # Open Perplexity AI home page
    elif 'open perplexity' in command or 'open perplexity ai' in command:
        speak("Opening Perplexity AI home page")
        webbrowser.open("https://www.perplexity.ai/")
        return "Opening Perplexity AI home page."

    # Open Wikipedia home page
    elif 'open wikipedia' in command:
        speak("Opening Wikipedia home page")
        webbrowser.open("https://www.wikipedia.org/")
        return "Opening Wikipedia home page."

    # Tell the time
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        return f"The current time is {current_time}"

    # Wikipedia summary
    elif 'wikipedia' in command:
        query = command.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia, {result}")
            return f"According to Wikipedia, {result}"
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find that on Wikipedia.")
            return "Sorry, I couldn't find that on Wikipedia."

    # Open Blackbox AI
    elif 'open black box ai' in command:
        speak("Opening Blackbox AI home page")
        webbrowser.open("https://www.blackbox.ai/")
        return "Opening Blackbox AI home page."

    # Open Google
    elif 'open google' in command:
        speak("Opening Google home page")
        webbrowser.open("https://www.google.com")
        return "Opening Google home page."

    # Open YouTube
    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    # Play song on YouTube
    elif 'play' in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
        return f"Playing {song} on YouTube."

    # Weather info
    elif 'weather' in command:
        api_key = "YOUR_OPENWEATHERMAP_API_KEY"
        city = "London"  # Replace with desired city or extract from command
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if response.get("cod") == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            speak(f"The weather in {city} is {temp} degrees Celsius with {desc}.")
            return f"The weather in {city} is {temp} degrees Celsius with {desc}."
        else:
            speak("Sorry, I couldn't fetch the weather data.")
            return "Sorry, I couldn't fetch the weather data."

    # ChatGPT direct prompt
    elif 'chatgpt' in command:
        prompt = command.replace('chatgpt', '').strip()
        if not prompt:
            speak("Please provide a prompt for ChatGPT.")
            return "Please provide a prompt for ChatGPT."
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content.strip()
            speak(answer)
            return answer
        except Exception as e:
            speak("Sorry, I couldn't get a response from ChatGPT.")
            return f"Error: {e}"

    # Shutdown commands
    elif (
        'exit' in command
        or 'turn off jarvis' in command
        or 'turn off' in command
        or 'shutdown' in command
    ):
        speak("Goodbye, sir. Turning off now.")
        return False

    # Fallback: ChatGPT for any other question
    else:
        if not command.strip():
            speak("Please ask a question or give a command.")
            return "Please ask a question or give a command."
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": command}]
            )
            answer = response.choices[0].message.content.strip()
            speak(answer)
            return answer
        except Exception as e:
            speak("Sorry, I couldn't get a response from ChatGPT.")
            return f"Error: {e}"

def run_jarvis():
    """Main loop to run JARVIS."""
    speak("JARVIS online. How may I assist you?")
    while True:
        command = take_command()
        if command:
            response = process_command(command)
            if response is False:
                break
            if response:
                print(f"Jarvis: {response}")

if __name__ == "__main__":
    run_jarvis()