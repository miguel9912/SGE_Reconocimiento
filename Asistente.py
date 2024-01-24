import datetime
import json
import os
import time
import webbrowser
import numpy as np
import cap
import cv2
import pyttsx3
import speech_recognition as sr

from FacialRecognition import FacialRecognition
from Persona import Persona

usuarios = list()




def talk(msg):
    newVoiceRate = 160

    engine = pyttsx3.init()
    engine.setProperty('rate', newVoiceRate)
    engine.say(msg)
    engine.runAndWait()

def audio_to_text(timeout=10):
    # Recognizer
    r = sr.Recognizer()

    # Configurar el micro
    with sr.Microphone() as origen:
        # Tiempo de espera desde que se activa el micro
        r.pause_threshold = 0.5

        # Informar que comenzó la grabación
        print('Puedes comenzar a hablar')
        start_time = time.time()

        # Guardar audio
        while time.time() - start_time < timeout:
            audio = r.listen(origen)
            try:
                # Buscar en google lo escuchado
                text = r.recognize_google(audio, language='es-es')
                print(text)
                return text.lower()
            except sr.UnknownValueError:
                print('Ups, no entendí lo que dijiste')
                return 'Esperando'
            except sr.RequestError:
                print('Ups, sin servicio')
                return 'Esperando'
            except Exception as e:
                print(f'Ups, algo ha salido mal: {e}')
                return 'Esperando'

        print('Tiempo de espera agotado')
        return 'Esperando'


def cargar_imagenes_cara(carpeta_caras):
    imagenes = []
    nombres = []

    for nombre_archivo in os.listdir(carpeta_caras):
        ruta_completa = os.path.join(carpeta_caras, nombre_archivo)
        if os.path.isfile(ruta_completa) and nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            imagenes.append(cv2.imread(ruta_completa, cv2.IMREAD_GRAYSCALE))
            nombres.append(os.path.splitext(nombre_archivo)[0])  # Elimina la extensión (.jpg, .png, etc.)

    return imagenes, nombres




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



def guardar_datos_personas(personas):
    dict_instances = {}
    for persona in personas:
        dict_instances[persona.name] = persona.to_dict()
        dict_instances[persona.image] = persona.to_dict()

    result = {'Persona': dict_instances}

    with open('datos_personas.json', 'w') as json_file:
        json.dump(result, json_file, indent=2)
    talk('Datos de personas guardados exitosamente.')

def cargar_datos_personas():
    try:
        with open('datos_personas.json', 'r') as json_file:
            data = json.load(json_file)
            dict_instances = data.get('Persona', {})  # Utilizar la clave 'Persona'
            personas = []

            for name, persona_data in dict_instances.items():
                nueva_persona = Persona(name, persona_data['image'])
                personas.append(nueva_persona)

            return personas
    except FileNotFoundError:
        return []

def registro():
    talk('Dime tu nombre, por favor.')

    # Establecer un límite de tiempo para la entrada del nombre (10 segundos en este caso)
    name = audio_to_text(timeout=10).lower()

    if name == 'esperando':
        talk('No se ha podido capturar correctamente tu nombre. Por favor, intenta nuevamente.')
        return None

    print(name)
    ruta_imagen, result = takePhoto(name)

    if result:
        newUser = Persona(name, ruta_imagen)
        usuarios.append(newUser)
        mensaje = f'{name} registrado exitosamente.'
        talk(mensaje)
        return newUser  # Devolver la nueva persona creada
    else:
        talk('El registro no ha podido realizarse correctamente.')
        return None



def takePhoto(name):
    # Abre la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        talk("Error: No se pudo abrir la cámara.")
        return None, False

    # Intenta establecer una tasa de fotogramas más alta
    cap.set(cv2.CAP_PROP_FPS, 120)  # Ajusta a 30 FPS, puedes experimentar con otros valores

    # Muestra la vista previa de la cámara
    talk("Preparándose para tomar la foto. Por favor, sonríe.")

    # Crea una ventana para mostrar la vista previa
    cv2.namedWindow('Reconocimiento Facial', cv2.WINDOW_NORMAL)

    # Inicia un bucle para mostrar la transmisión en tiempo real durante la cuenta atrás
    for i in range(4, 0, -1):
        # Captura un fotograma
        ret, frame = cap.read()
        if not ret:
            talk("Error al capturar la foto.")
            break

        # Muestra la imagen actualizada en la ventana
        cv2.imshow('Reconocimiento Facial', frame)

        # Espera 1 segundo entre cada cuenta regresiva
        time.sleep(1)
        talk(str(i))

    # Cierra la ventana de vista previa
    cv2.destroyWindow('Reconocimiento Facial')

    # Captura un solo fotograma después de la cuenta atrás
    ret, frame = cap.read()
    if ret:
        # Guarda la foto
        cv2.imwrite(f"{name}.jpg", frame)
        talk(f"Foto capturada y guardada como '{name}.jpg'")
        # Libera la cámara
        cap.release()
        return frame, True
    else:
        talk("Error al capturar la foto.")
        # Libera la cámara
        cap.release()
        return None, False

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
            talk('Hasta luego bombón')
            # Guardar la información antes de salir
            guardar_datos_personas(usuarios)
            exit()
        elif 'registrarse' in request:
            nueva_persona = registro()
            if nueva_persona:
                usuarios.append(nueva_persona)
                # Guardar la información después de registrar
                guardar_datos_personas(usuarios)
        elif 'comprobar registro' in request:
            if comprobarRegistro():
                talk('El usuario está registrado en el sistema')
            else:
                talk('El usuario no está registrado en el sistema')
        elif 'iniciar sesión' in request:
            folder_path = 'C:\\Users\\Alumno\\Desktop\\SGE_Reconocimiento\\caras'
            facial_recognition = FacialRecognition()
            reconocido, nombre_encontrado = facial_recognition.run(folder_path)
            if reconocido:
                talk(f"Bienvenido, {nombre_encontrado}!")
            else:
                talk("No se encontró ninguna coincidencia con los usuarios registrados.")
        elif 'listar usuarios' in request:
            showUsers()
            talk('Estos son los usuarios registrados:')
            for persona in usuarios:
                talk(persona.name)




