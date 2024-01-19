import cv2
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import time

from Persona import Persona


usuarios = list()

#########################################################
################ CONVERTIR AUDIO A TEXTO ################
#########################################################
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
#########################################################










########################################
################ HABLAR ################
########################################
def talk(msg):
    newVoiceRate = 160

    engine = pyttsx3.init()
    engine.setProperty('rate', newVoiceRate)
    engine.say(msg)
    engine.runAndWait()
########################################





########################################
################ SALUDO ################
########################################
def saludo():

    hour = datetime.datetime.now()
    if hour.hour < 6 or hour.hour > 20:
        momento = 'Buenas noches.'
    elif 6 <= hour.hour < 13:
        momento = 'Buenos días.'
    else:
        momento = 'Buenas tardes.'

    talk(f'{momento} Soy el bicho, tu asistente personal.')
########################################








#############################################
################ REGISTRARSE ################
#############################################
def registro():
    talk('Dime tu nombre, por favor.')

    # Establecer un límite de tiempo para la entrada del nombre (10 segundos en este caso)
    name = audio_to_text(timeout=10).lower()

    if name == 'esperando':
        talk('No se ha podido capturar correctamente tu nombre. Por favor, intenta nuevamente.')
        return None

    print(name)
    talk('Ahora vamos a tomarte una foto no te muevas por favor.')
    photo, result = takePhoto(name)

    if result:
        newUser = Persona(name, photo)
        usuarios.append(newUser)
        mensaje = f'{name} registrado exitosamente.'
        talk(mensaje)
        return newUser
    else:
        talk('El registro no ha podido realizarse correctamente.')
#############################################









############################################
################ TOMAR FOTO ################
############################################
def takePhoto(name):
    # Abre la cámara
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        talk("Error: No se pudo abrir la cámara.")
        return None, False

    # Intenta establecer una tasa de fotogramas más alta
    cap.set(cv2.CAP_PROP_FPS, 30)  # Ajusta a 30 FPS, puedes experimentar con otros valores

    # Muestra la vista previa de la cámara
    talk("Preparándose para tomar la foto. Por favor, sonríe.")

    # Crea una ventana para mostrar la vista previa
    cv2.namedWindow('Reconocimiento Facial', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Reconocimiento Facial', 640, 480)

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
        time.sleep(250)
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
############################################









######################################################
################ COMPROBAR REGISTRARO ################
######################################################
def comprobarRegistro():
    talk('¿Que usuario deseas comprobar?')
    name = audio_to_text().lower()
    found = False
    for p in usuarios:
        if p.name == name:
            found = True
    return found
######################################################






##################################################
################ MOSTRAR USUARIOS ################
##################################################
def showUsers():
    for persona in usuarios:
        print(persona.name)
##################################################




############################################
################ PETICIONES ################
############################################
def requests():
    saludo()
    stop = False
    while not stop:
        talk('¿Qué deseas hacer?')
        request = audio_to_text().lower()
        print(request)
        if 'registrarse' in request:
            registro()
        elif 'comprobar registro' in request:
            if comprobarRegistro():
                talk('El usuario está registrado en el sistema')
            else:
                talk('El usuario no está registrado en el sistema')
        elif 'listar usuarios' in request:
            showUsers()
        elif 'salir' in request:
            talk('Hasta luégo bombón')
            exit()
############################################


