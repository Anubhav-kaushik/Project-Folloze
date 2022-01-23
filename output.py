from win32com.client import Dispatch

def speak(text):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(text)


