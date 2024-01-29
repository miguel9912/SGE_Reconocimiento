from pathlib import Path
import cv2
import face_recognition as fr
import unidecode

class FacialRecognition:
    def __init__(self, folder_path):
        self.caras_folder = Path(folder_path)
        self.cod_faces = []
        self.names = []


    def cargar_imagenes(self):
        self.cod_faces = []
        self.names = []

        for path in self.caras_folder.glob('*.jpg'):
            encoding = fr.face_encodings(fr.load_image_file(path))

            if encoding:
                self.cod_faces.append(encoding[0])
                self.names.append(path.stem)
            else:
                print(f"No se pudo detectar ninguna cara en la imagen {path}")

    def tomar_foto(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        return frame

    def reconocer_persona(self, foto):
        foto_cod = fr.face_encodings(foto)
        if foto_cod:
            for i, cod in enumerate(self.cod_faces):
                results = fr.compare_faces([cod], foto_cod[0])
                if all(results):
                    # Asegura que el nombre no tenga tildes, esté en minúsculas y no tenga espacios
                    nombre_encontrado = unidecode.unidecode(self.names[i].lower().replace(" ", ""))
                    return True, nombre_encontrado
        return False, None

    def run(self):
        cara_control = self.tomar_foto()
        self.cargar_imagenes()

        reconocido, nombre_encontrado = self.reconocer_persona(cara_control)

        if reconocido:
            return(f"Bienvenido {nombre_encontrado}!")
        else:
            return ("No se encontró ninguna coincidencia con los usuarios registrados.")