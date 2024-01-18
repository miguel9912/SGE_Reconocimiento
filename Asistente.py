import pyttsx3
import speech_recognition as sr

import webbrowser
import datetime
import wikipedia

from Persona import Persona


usuarios = list()

# Escuchar micro y devolver audio como texto
def audio_to_text():
    # Recognizer
    r = sr.Recognizer()

    # Configurar el micro
    with sr.Microphone() as origen:
        # Tiempo de espera desde que se activa el micro
        r.pause_threshold = 0.5

        # Informar que comenzó la grabación
        print('Puedes comenzar a hablar')
        # Guardar audio
        audio = r.listen(origen, )
        try:
            # Buscar en google lo escuchado
            text = r.recognize_google(audio, language='es-es')
            print(text)
            return text
        except sr.UnknownValueError:
            print('Ups, no entendí lo que dijiste')
            return 'Esperando'

        except sr.RequestError:
            print('Ups, sin servicio')
            return 'Esperando'

        except:
            print('Ups, algo ha salido mal')
            return 'Esperando'







def talk(msg):
    newVoiceRate = 160

    engine = pyttsx3.init()
    engine.setProperty('rate', newVoiceRate)
    engine.say(msg)
    engine.runAndWait()






def print_voices():
    engine = pyttsx3.init()
    for voz in engine.getProperty('voices'):
        print(voz.id, voz)





def saludo():

    hour = datetime.datetime.now()
    if hour.hour < 6 or hour.hour > 20:
        momento = 'Buenas noches.'
    elif 6 <= hour.hour < 13:
        momento = 'Buenos días.'
    else:
        momento = 'Buenas tardes.'

    talk(f'{momento} Soy el bicho, tu asistente personal.')






def registro():
    talk('Dime tu nombre cariño')
    name = audio_to_text().lower()
    print(name)
    usuarios.append(Persona(name, ""))
    mensaje  = f'{name} registrado exitosamente'
    talk(mensaje)
    return Persona(name, "")


def comprobarRegistro():
    talk('¿Que usuario deseas comprobar?')
    name = audio_to_text().lower()
    found = False
    for p in usuarios:
        if p.name == name:
            found = True
    return found

def mostrarUsuarios():
    for persona in usuarios:
        print(persona.name)


def requests():
    saludo()
    stop = False
    while not stop:
        talk('¿Qué deseas hacer?')
        request = audio_to_text().lower()
        print(request)
        if 'abrir youtube' in request:
            talk('Abriendo youtube')
            webbrowser.open('https://www.youtube.com')
        elif 'salir' in request:
            talk('Hasta luégo, bombón')
            exit()
        elif 'registrarse' in request:
            registro()
        elif 'comprobar registro' in request:
            if comprobarRegistro():
                talk('El usuario está registrado en el sistema')
            else:
                talk('El usuario no está registrado en el sistema')
        elif 'listar usuarios' in request:
            mostrarUsuarios()


