import cv2
import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import datetime
import time

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




def takePhoto():
    # Abre la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        talk("Error: No se pudo abrir la cámara.")
        return

    # Muestra la vista previa de la cámara
    talk("Preparándose para tomar la foto. Por favor, sonríe.")
    for i in range(3, 0, -1):
        talk(str(i))
        #time.sleep(250)

    # Captura un solo fotograma
    ret, frame = cap.read()
    if ret:
        # Guarda la foto
        cv2.imwrite("foto_capturada.jpg", frame)
        talk("Foto capturada y guardada como 'foto_capturada.jpg'")
    else:
        talk("Error al capturar la foto.")

    # Libera la cámara
    cap.release()

# Resto del código...


def comprobarRegistro():
    talk('¿Que usuario deseas comprobar?')
    name = audio_to_text().lower()
    found = False
    for p in usuarios:
        if p.name == name:
            found = True
    return found

def showUsers():
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
            showUsers()
        elif 'tomar foto' in request:
            takePhoto()



