import speech_recognition as sr
from gtts import gTTS
import datetime
import webbrowser
import os
import pywhatkit
import random
import pygame
import tempfile
import pyautogui
import subprocess 
pygame.mixer.init()


applications = {
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": r"C:\Windows\system32\notepad.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "spotify": r"C:\Users\TonNomUtilisateur\AppData\Roaming\Spotify\Spotify.exe",
    "discord": r"C:\Users\HP\AppData\Local\Discord\Update.exe --processStart Discord.exe"
}

def parler(texte):
    """Fait parler l'IA avec voix humaine gTTS"""
    print(f"🗣️ IA: {texte}")
    tts = gTTS(text=texte, lang="fr")
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        chemin_audio = fp.name + ".mp3"
        tts.save(chemin_audio)
        pygame.mixer.music.load(chemin_audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass  

def ecoute():
    """Écoute la voix de l'utilisateur et retourne le texte"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 J'écoute...")
        r.pause_threshold = 0.7
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="fr-FR")
        print(f"✅ Tu as dit : {text}")
        return text.lower()
    except sr.UnknownValueError:
        parler(random.choice([
            "Pardon ? J’ai pas compris.",
            "Désolé, tu peux répéter ?",
            "Hmm, ça m’a échappé."
        ]))
        return ""
    except sr.RequestError:
        parler("Il y a un souci avec la connexion internet.")
        return ""

def ouvrir_application(cmd):
    """Ouvre une application ou propose des options si ambiguë"""
    trouvé = False
    for app in applications:
        if app in cmd:
            parler(f"Je lance {app} pour toi.")
            chemin = applications[app]
            # Si l'application contient des arguments (ex: Discord)
            if "discord" in app:
                subprocess.Popen(chemin)
            else:
                os.startfile(chemin)
            trouvé = True
            break
    if not trouvé:
        parler("Je peux ouvrir ces applications : " + ", ".join(applications.keys()))

def commande(cmd):
    """Analyse et exécute la commande"""
    if "heure" in cmd:
        heure = datetime.datetime.now().strftime("%H:%M")
        parler(random.choice([
            f"Il est exactement {heure}.",
            f"On est à {heure} pile.",
            f"Actuellement, il est {heure}."
        ]))

    elif "date" in cmd:
        date = datetime.datetime.now().strftime("%d %B %Y")
        parler(random.choice([
            f"Aujourd'hui, on est le {date}.",
            f"On est le {date}.",
            f"{date}, c’est la date du jour."
        ]))

    elif "ouvre google" in cmd:
        parler(random.choice([
            "C’est parti, ouverture de Google.",
            "J’ouvre Google pour toi.",
            "Un instant, Google arrive."
        ]))
        webbrowser.open("https://www.google.com")
    

    elif "cherche" in cmd:
        recherche = cmd.replace("cherche", "").strip()
        parler(f"Je cherche {recherche} sur Google.")
        pywhatkit.search(recherche)

    elif "joue" in cmd:
        musique = cmd.replace("joue", "").strip()
        parler(random.choice([
            f"Ok, je mets {musique} sur YouTube.",
            f"Je lance {musique}, profite bien.",
            f"Voici {musique} sur YouTube."
        ]))
        pywhatkit.playonyt(musique)

    elif "ouvre" in cmd:
        ouvrir_application(cmd)

    elif " éteins l'ordinateur" in cmd:
        parler(random.choice([
            "Ok, je vais l’éteindre.",
            "C’est parti, l’ordinateur va se fermer.",
            "Je te laisse, l’ordinateur va se fermer."
        ]))
        os.system("shutdown /s /t 0")

    elif "redemarer l'ordinateur" in cmd:
        parler(random.choice([
            "Ok, je vais redémarrer.",
            "C’est parti, l’ordinateur va se redémarrer.",
            "Je te laisse, l’ordinateur va se redémarrer."
        ]))
        os.system("shutdown /r /t 1")

    elif "stop" in cmd or "au revoir" in cmd:
        parler(random.choice([
            "À plus tard, prends soin de toi.",
            "D’accord, je me déconnecte. Bye !",
            "À bientôt !"
        ]))
        exit()

    else:
        parler(random.choice([
            "Hmm… ça, je ne sais pas encore le faire.",
            "Désolé, je ne connais pas cette commande.",
            "Je ne suis pas sûr de comprendre."
        ]))

if __name__ == "__main__":
    parler(random.choice([
        "Salut ! Prêt à discuter ?",
        "Bonjour, comment ça va aujourd’hui ?",
        "Hey ! C’est parti pour te filer un coup de main."
    ]))
    while True:
        texte = ecoute()
        if texte:
            commande(texte)
