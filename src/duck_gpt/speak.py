from gtts import gTTS
import os
import playsound

def speak(text):
    # configura el idioma
    tts = gTTS(text=text, lang='es')
    # guarda el audio en un archivo
    filename = 'voice.mp3'
    # reproduce el audio
    tts.save(filename)
    # reproduce el audio
    playsound.playsound(filename)
    # elimina el archivo
    os.remove(filename)