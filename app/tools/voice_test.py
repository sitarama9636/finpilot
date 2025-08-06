from app.tools.voice_tool import recognize_voice, speak_text

if __name__ == "__main__":
    print("🎙️ Say something...")

    # Step 1: Capture voice and convert to text
    query = recognize_voice()

    # Step 2: Confirm back to user
    if query:
        print(f"✅ Recognized: {query}")
        speak_text(f"You said: {query}")
    else:
        print("⚠️ No valid voice input captured.")
