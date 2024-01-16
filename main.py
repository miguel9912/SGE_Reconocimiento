import cv2
import os
import speech_recognition as sr

class AsistenteScrum:
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

            # Salir si se presiona la tecla 'Esc'
            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyAllWindows()
                return None

def reconocer_usuario_en_imagen(self, imagen):
    for nombre_usuario, datos_usuario in self.usuarios_registrados.items():
        foto_registrada = cv2.imread(datos_usuario['foto'], cv2.IMREAD_GRAYSCALE)
        # Aquí puedes utilizar algún método de comparación de características, como la 		correlación
        correlacion = cv2.matchTemplate(imagen, foto_registrada, cv2.TM_CCOEFF_NORMED)
        if correlacion > umbral_de_correlacion:
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
            print("Escuchando... Di una orden:")
            audio = recognizer.listen(source)

        try:
            orden = recognizer.recognize_google(audio, language="es-ES").lower()
            return orden
        except sr.UnknownValueError:
            return "No se pudo entender la orden"
        except sr.RequestError as e:
            return f"Error en la solicitud de reconocimiento de voz: {e}"

    def controlar_asistencia(self):
        orden = self.reconocer_voz()

        if "controlar asistencia" in orden:
            nombre_usuario = self.reconocer_usuario_con_camara()

            if nombre_usuario:
                print(f"Bienvenido, {nombre_usuario}.")
            else:
                print("Usuario no reconocido. ¿Desea registrarse?")

    def registrar_usuario(self):
        orden = self.reconocer_voz()

        if "registrar usuario" in orden:
            nombre_usuario = input("Dime tu nombre: ")
            datos_personales = input("Dime tus datos personales: ")

            ruta_imagen = self.capturar_imagen(nombre_usuario)

            self.usuarios_registrados[nombre_usuario] = {
                'datos_personales': datos_personales,
                'foto': ruta_imagen
            }
            print(f"Usuario {nombre_usuario} registrado con éxito.")

    def salir_aplicacion(self):
        orden = self.reconocer_voz()

        if "salir de la aplicación" in orden:
            print("Hasta luego. Gracias por usar la aplicación.")
            exit()

# Ejemplo de uso
asistente = AsistenteScrum()

while True:
    asistente.controlar_asistencia()
    asistente.registrar_usuario()
    asistente.salir_aplicacion()