import os
import cv2
import pyttsx3
import speech_recognition as sr
import pywhatkit
import webbrowser
import datetime
import time
import json
from Persona import Persona

usuarios = list()


def audio_to_text(timeout=10):
    # Recognizer
    r = sr.Recognizer()

    # Configurar el micrófono
    with sr.Microphone() as origen:
        # Tiempo de espera desde que se activa el micrófono
        r.pause_threshold = 0.5

        # Informar que comenzó la grabación
        print('Puedes comenzar a hablar')
        start_time = time.time()

        # Guardar audio
        while time.time() - start_time < timeout:
            audio = r.listen(origen)
            try:
                # Buscar en Google lo escuchado
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


def guardar_datos_personas(personas):
    dict_instances = {}
    for persona in personas:
        dict_instances[persona.name] = persona.to_dict()

    result = {'Personas': dict_instances}

    with open('datos_personas.json', 'w') as json_file:
        json.dump(result, json_file, indent=2)
    talk('Datos de personas guardados exitosamente.')


def cargar_datos_personas():
    if not usuarios:  # Solo cargar si la lista de usuarios está vacía
        try:
            with open('datos_personas.json', 'r') as json_file:
                data = json.load(json_file)
                dict_instances = data.get('Personas', {})
                personas = []

                for name, persona_data in dict_instances.items():
                    nueva_persona = Persona(name, persona_data['image'])
                    personas.append(nueva_persona)

                return personas
        except FileNotFoundError:
            return []

    return usuarios


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
        return newUser
    else:
        talk('El registro no ha podido realizarse correctamente.')
        return None


def takePhoto(name):
    # Crear la carpeta "caras" si no existe
    if not os.path.exists("caras"):
        os.makedirs("caras")

    # Abre la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        talk("Error: No se pudo abrir la cámara.")
        return None, False

    # Intenta establecer una tasa de fotogramas más alta
    cap.set(cv2.CAP_PROP_FPS, 120)

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
        # Guarda la foto en la carpeta "caras"
        cv2.imwrite(os.path.join("caras", f"{name}.jpg"), frame)
        talk(f"Foto capturada y guardada como 'caras/{name}.jpg'")
        # Libera la cámara
        cap.release()
        return frame, True
    else:
        talk("Error al capturar la foto.")
        # Libera la cámara
        cap.release()
        return None, False


def comprobarRegistro():
    talk('¿Qué usuario deseas comprobar?')
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
    # Cargar los datos de los usuarios al inicio
    usuarios.extend(cargar_datos_personas())

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
            talk('SUUUUUUUU')
            talk('Hasta luego bombón')
            guardar_datos_personas(usuarios)
            exit()
        elif 'registrarse' in request:
            nueva_persona = registro()
            if nueva_persona:
                usuarios.append(nueva_persona)
                guardar_datos_personas(usuarios)
        elif 'comprobar registro' in request:
            if comprobarRegistro():
                talk('El usuario está registrado en el sistema')
            else:
                talk('El usuario no está registrado en el sistema')
        elif 'listar usuarios' in request:
            showUsers()
            talk('Estos son los usuarios registrados:')
            for persona in usuarios:
                talk(persona.name)





