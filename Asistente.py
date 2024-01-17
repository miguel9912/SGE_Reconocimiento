import cv2
import speech_recognition as sr
import os

class Asistente:
    def __init__(self):
        self.usuarios_registrados = {}

    def reconocer_usuario_con_camara(self):
        # Inicializar el clasificador facial de OpenCV
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Inicializar la cámara
        cap = cv2.VideoCapture(0)

        while True:
            # Capturar el fotograma
            ret, frame = cap.read()

            # Convertir a escala de grises para el reconocimiento facial
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detectar rostros en el fotograma
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Dibujar un rectángulo alrededor del rostro detectado
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Recortar la región del rostro
                roi_gray = gray[y:y+h, x:x+w]

                # Devolver el nombre del usuario si es reconocido
                nombre_usuario = self.reconocer_usuario_en_imagen(roi_gray)
                if nombre_usuario:
                    cap.release()
                    cv2.destroyAllWindows()
                    return nombre_usuario

            # Mostrar el fotograma con el rectángulo alrededor del rostro
            cv2.imshow('Reconocimiento Facial', frame)

            # Si no hay usuarios registrados, tomar una foto y cerrar la cámara
            if not self.usuarios_registrados:
                print("Usuario no registrado. Tomando foto y cerrando la cámara...")
                ruta_imagen = self.tomar_foto_y_cerrar_camara()
                nombre_usuario = self.reconocer_voz()

                # Registrar al usuario
                self.usuarios_registrados[nombre_usuario] = {
                    'foto': ruta_imagen
                }
                print(f"Usuario {nombre_usuario} registrado con éxito en {ruta_imagen}.")
                return nombre_usuario

            # Salir si se presiona la tecla 'Esc'
            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyAllWindows()
                return None

    def mostrar_camara(self):
        # Inicializar la cámara
        cap = cv2.VideoCapture(0)

        while True:
            # Capturar el fotograma
            ret, frame = cap.read()

            # Mostrar el fotograma en una ventana
            cv2.imshow('Vista de la Cámara', frame)

            # Salir si se presiona la tecla 'Esc'
            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyAllWindows()
                break

    def tomar_foto_y_cerrar_camara(self):
        cap = cv2.VideoCapture(0)

        # Capturar el fotograma
        ret, frame = cap.read()

        # Guardar la imagen en un archivo
        ruta_imagen = self.reconstruir_nombre_imagen("temp_user")
        cv2.imwrite(ruta_imagen, frame)

        cap.release()
        cv2.destroyAllWindows()

        return ruta_imagen

    def reconocer_usuario_en_imagen(self, imagen):
        for nombre_usuario, datos_usuario in self.usuarios_registrados.items():
            foto_registrada = cv2.imread(datos_usuario['foto'], cv2.IMREAD_GRAYSCALE)
            # Aquí puedes utilizar algún método de comparación de características, como la correlación
            correlacion = cv2.matchTemplate(imagen, foto_registrada, cv2.TM_CCOEFF_NORMED)
            # if correlacion > umbral_de_correlacion:
            if correlacion > 0.6:
                return nombre_usuario
        return None

    def capturar_imagen(self, nombre_usuario):
        # Inicializar la cámara
        cap = cv2.VideoCapture(0)

        # Capturar el fotograma
        ret, frame = cap.read()

        # Guardar la imagen en un archivo
        ruta_imagen = self.reconstruir_nombre_imagen(nombre_usuario)
        cv2.imwrite(ruta_imagen, frame)

        cap.release()
        cv2.destroyAllWindows()

        return ruta_imagen

    def reconstruir_nombre_imagen(self, nombre_usuario):
        return f"{nombre_usuario.replace(' ', '_')}.jpg"

    def reconocer_voz(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Escuchando... Di tu nombre:")
            audio = recognizer.listen(source)

        try:
            nombre_usuario = recognizer.recognize_google(audio, language="es-ES").lower()
            print(f"Nombre reconocido por voz: {nombre_usuario}")  # Mensaje de depuración
            return nombre_usuario
        except sr.UnknownValueError:
            print("No se pudo entender el nombre")
            return "No se pudo entender el nombre"
        except sr.RequestError as e:
            print(f"Error en la solicitud de reconocimiento de voz: {e}")
            return f"Error en la solicitud de reconocimiento de voz: {e}"

    def controlar_asistencia(self):
        orden = self.reconocer_voz()
        print(f"Orden reconocida: {orden}")

        if "iniciar reconocimiento" in orden:
            print("Iniciando reconocimiento facial...")
            self.mostrar_camara()
            nombre_usuario = self.reconocer_usuario_con_camara()

            if nombre_usuario:
                print(f"Bienvenido, {nombre_usuario}.")
            else:
                print("Usuario no reconocido. ¿Desea registrarse?")

    def registrar_usuario(self):
        orden = self.reconocer_voz()

        if "registrar usuario" in orden:
            nombre_usuario = self.reconocer_voz()

            # Verificar si el directorio "caras" existe, si no, crearlo
            if not os.path.exists("caras"):
                os.makedirs("caras")

            # Capturar la imagen con la webcam
            ruta_imagen = os.path.join("caras", f"{nombre_usuario.replace(' ', '_')}.jpg")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cv2.imwrite(ruta_imagen, frame)
            cap.release()
            cv2.destroyAllWindows()

            # Registrar al usuario
            self.usuarios_registrados[nombre_usuario] = {
                'foto': ruta_imagen
            }
            print(f"Usuario {nombre_usuario} registrado con éxito en {ruta_imagen}.")

    def salir_aplicacion(self):
        orden = self.reconocer_voz()

        if "salir de la aplicación" in orden:
            print("Hasta luego. Gracias por usar la aplicación de reconocimiento facial.")
            exit()
