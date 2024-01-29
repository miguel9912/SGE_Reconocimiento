import os
import cv2
import pyttsx3
import speech_recognition as sr
import datetime
import time
import json
from FacialRecognition import FacialRecognition
from Persona import Persona

usuarios = list()

######################################################################
######## TRANSFORMAMOS A TEXTO LA INFO RECIBIDA POR MICRÓFONO ########
######################################################################
def audio_to_text(timeout=10):
    r = sr.Recognizer()

    with sr.Microphone() as origen:
        r.pause_threshold = 0.5

        print('Puedes comenzar a hablar')
        start_time = time.time()

        while time.time() - start_time < timeout:
            audio = r.listen(origen)
            try:
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
######################################################################

##################################################################
######## MUESTRA EN AUDIO EL TEXTO RECIBIDO POR PARÁMETRO ########
##################################################################
def talk(msg):
    newVoiceRate = 160

    engine = pyttsx3.init()
    engine.setProperty('rate', newVoiceRate)
    engine.say(msg)
    engine.runAndWait()
##################################################################


#######################################################
######## SALUDO EN FUNCIÓN DEL MOMENTO DEL DÍA ########
#######################################################
def saludo():
    hour = datetime.datetime.now()
    if hour.hour < 6 or hour.hour > 20:
        momento = 'Buenas noches.'
    elif 6 <= hour.hour < 13:
        momento = 'Buenos días.'
    else:
        momento = 'Buenas tardes.'

    talk(f'{momento}.')
#######################################################

####################################################
######## GUARDAR DATOS RECOGIDOS EN EL JSON ########
####################################################
def guardar_datos_personas(personas):
    dict_instances = {}
    for persona in personas:
        dict_instances[persona.name] = persona.to_dict()

    result = {'Personas': dict_instances}

    with open('datos_personas.json', 'w') as json_file:
        json.dump(result, json_file, indent=2)
    print('Datos de personas guardados exitosamente.')
####################################################

####################################################
######## MOSTRAR DATOS RECOGIDOS EN EL JSON ########
####################################################
def cargar_datos_personas():
    if not usuarios:  # Solo cargar si la lista de usuarios está vacía
        try:
            with open('datos_personas.json', 'r') as json_file:
                data = json.load(json_file)
                dict_instances = data.get('Personas', {})
                personas = []

                for name, persona_data in dict_instances.items():
                    nueva_persona = Persona(name, persona_data['image'], persona_data['phone'])
                    personas.append(nueva_persona)

                return personas
        except FileNotFoundError:
            return []

    return usuarios
####################################################


###########################################################
######## RECOGIDA DE INFORMACIÓN DEL NUEVO USUARIO ########
###########################################################
def registro():
    talk('Dime tu nombre por favor.')
    name = audio_to_text(timeout=10).lower()

    while name == 'esperando':
        talk('No se ha podido capturar correctamente tu nombre. Por favor, intenta nuevamente.')
        name = audio_to_text(timeout=10).lower()
    talk('A continuación te tomaremos una foto')
    ruta_imagen, result = takePhoto(name)

    talk('Por último indica tu número de teléfono por favor.')
    phone = audio_to_text(timeout=10).lower()
    phone = phone.replace(" ","")
    while phone == 'esperando' or not phone.isdigit():
        if phone == 'esperando':
            talk('No se ha podido capturar correctamente tu teléfono. Por favor, intenta nuevamente.')
        elif not phone.isdigit():
            talk('El teéfono solo puede contener números')
        phone = audio_to_text(timeout=10).lower()
        phone = phone.replace(" ", "")

    if result:
        newUser = Persona(name, ruta_imagen, phone)
        usuarios.append(newUser)
        mensaje = f'{name} registrado exitosamente.'
        talk(mensaje)
        return newUser
    else:
        talk('El registro no ha podido realizarse correctamente.')
        return None
###########################################################


################################
######## TOMAMOS IMAGEN ########
################################
def takePhoto(name):
    # Crear la carpeta "caras" si no existe
    if not os.path.exists("caras"):
        os.makedirs("caras")

    # Abre la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return None, False

    # Intenta establecer una tasa de fotogramas más alta
    cap.set(cv2.CAP_PROP_FPS, 120)

    talk("Preparándose para tomar la foto. Por favor, sonríe.")

    cv2.namedWindow('Reconocimiento Facial', cv2.WINDOW_NORMAL)

    ret, frame = cap.read()
    cv2.imshow('Reconocimiento Facial', frame)

    if not ret:
        print("Error al capturar la foto.")
        cap.release()
        cv2.destroyAllWindows()
        return None, False

    for i in range(3, 0, -1):
        time.sleep(0.250)  # Ajusta el tiempo de espera según tus necesidades
        talk(str(i))

    # Cierra la ventana de vista previa
    cv2.destroyWindow('Reconocimiento Facial')

    ret, frame = cap.read()
    if ret:
        # Guarda la foto en la carpeta "caras"
        cv2.imwrite(os.path.join("caras", f"{name}.jpg"), frame)
        talk(f"Foto capturada y guardada como 'caras/{name}.jpg'")
        # Libera la cámara
        cap.release()
        cv2.destroyAllWindows()
        return frame, True
    else:
        print("Error al capturar la foto.")
        # Libera la cámara
        cap.release()
        cv2.destroyAllWindows()
        return None, False
##############################

#################################################
######## COMPROBAR USUARIO EN EL SISTEMA ########
#################################################
def comprobarRegistro():
    talk('¿Qué usuario deseas comprobar?')
    name = audio_to_text().lower()
    found = False
    for p in usuarios:
        if p.name == name:
            found = True
    return found
#################################################

##################################
######## MOSTRAR USUARIOS ########
##################################
def showUsers():
    for persona in usuarios:
        print(persona.name)
##################################


##################################
######## MÉTODO PRINCIPAL ########
##################################
def requests():
    # Cargar los datos de los usuarios al inicio
    usuarios.extend(cargar_datos_personas())
    logged = False
    saludo()
    stop = False
    while not stop:

        if not logged:
            talk('¿Qué deseas hacer?')
            talk('¿Deseas iniciar sesión, registrarte o salir ?')
            request = audio_to_text().lower()
            if 'salir' in request:
                talk('Hasta luego bombón')
                guardar_datos_personas(usuarios)
                stop = True

            elif ('registrarse' or 'registrarme') in request:
                nueva_persona = registro()
                if nueva_persona:
                    usuarios.append(nueva_persona)
                    guardar_datos_personas(usuarios)
                    logged = True

            elif 'iniciar sesión' in request:
                folder_path = 'caras'
                facial_recognition = FacialRecognition(folder_path)
                talk('Mira a la cámara por favor')
                code = facial_recognition.run()
                talk(code)
                if 'Bienvenido' in code:
                    logged = True
                else:
                    logged = False

            elif ('repetir' or 'repite') in request:
                pass


        else:
            talk('¿Qué deseas hacer?')
            talk('¿Deseas comprobar algún regístro en concreto, listar usuarios, cerrar sesión o salir?')
            request = audio_to_text().lower()

            if 'comprobar registro' in request:
                if comprobarRegistro():
                    talk('El usuario está registrado en el sistema')
                else:
                    talk('El usuario no está registrado en el sistema')

            elif ('listar usuarios' or 'lista los usuarios' or 'listar los usuarios') in request:
                showUsers()
                talk('Estos son los usuarios registrados:')
                for persona in usuarios:
                    talk(persona.name)
            elif 'cerrar sesión' in request:
                talk('Hasta la próxima')
                logged = False

            elif 'salir' in request:
                talk('Hasta luego bombón')
                guardar_datos_personas(usuarios)
                stop = True

            elif ('repetir' or 'repite') in request:
                pass

##################################