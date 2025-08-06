from langchain_core.tools import tool
import speech_recognition as sr
import pyttsx3

@tool
def recognize_voice() -> str:
    """Use the microphone to convert user speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError:
        print("❌ Speech Recognition service error.")
        return ""

@tool
def speak_text(text: str):
    """Convert the given text into spoken audio."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return "🔊 Spoken successfully."
