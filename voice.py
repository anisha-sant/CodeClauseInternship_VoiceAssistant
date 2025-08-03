import tkinter as tk
from tkinter import ttk
import threading
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty('rate', 180) 

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_and_process():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Update the UI to show that the app is listening
        status_label.config(text="Listening...", foreground="red")
        transcript_label.config(text="You said: (listening...)")
        root.update()

        try:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            # Use Google's Speech Recognition to convert audio to text
            command = r.recognize_google(audio)
            transcript_label.config(text=f"You said: {command}")
            status_label.config(text="Processing...", foreground="blue")
            root.update()
            
            print(f"User command: {command}")
            response = process_command(command)
            
            assistant_response_label.config(text=f"Assistant: {response}")
        
            status_label.config(text="Speaking...", foreground="green")
            root.update()
            speak(response)
            
        except sr.UnknownValueError:
            error_message = "Sorry, I could not understand the audio."
            transcript_label.config(text=error_message)
            speak(error_message)
        except sr.RequestError as e:
            error_message = f"Could not request results from Google Speech Recognition service; {e}"
            transcript_label.config(text=error_message)
            speak(error_message)
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            transcript_label.config(text=error_message)
            speak(error_message)
        finally:
            status_label.config(text="Ready. Click the button to start.", foreground="black")
            root.update()

def process_command(command):
    """
    Simulates a response from a large language model based on the command.
    In a real application, this would be an API call.
    """
    command_lower = command.lower()
    if "hello" in command_lower:
        return "Hello there! How can I help you today?"
    elif "time" in command_lower:
        import datetime
        now = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {now}."
    elif "date" in command_lower:
        import datetime
        today = datetime.date.today().strftime("%B %d, %Y")
        return f"Today's date is {today}."
    elif "how are you" in command_lower:
        return "I am a computer program, but thank you for asking. I'm functioning optimally!"
    else:
        return f"I can't answer '{command}' right now, but a real assistant would give you a helpful response here."

def start_voice_assistant():
    """
    Starts the voice assistant functionality in a new thread to keep the GUI
    responsive.
    """
    thread = threading.Thread(target=listen_and_process)
    thread.daemon = True
    thread.start()

root = tk.Tk()
root.title("Python Voice Assistant")
root.geometry("600x400")
root.resizable(False, False)

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

title_label = ttk.Label(main_frame, text="Python Voice Assistant", font=("Helvetica", 20, "bold"))
title_label.pack(pady=(0, 20))

mic_button = ttk.Button(main_frame, text="Click to Speak", command=start_voice_assistant)
mic_button.pack(pady=10)

status_label = ttk.Label(main_frame, text="Ready. Click the button to start.", font=("Helvetica", 12))
status_label.pack(pady=(10, 20))

display_frame = ttk.Frame(main_frame, relief="sunken", borderwidth=2)
display_frame.pack(fill="both", expand=True, padx=10, pady=10)


transcript_label = ttk.Label(display_frame, text="You said:", font=("Helvetica", 12, "italic"), wraplength=500)
transcript_label.pack(pady=10, anchor="w", padx=10)

assistant_response_label = ttk.Label(display_frame, text="Assistant:", font=("Helvetica", 12), wraplength=500)
assistant_response_label.pack(pady=10, anchor="w", padx=10)

root.mainloop()