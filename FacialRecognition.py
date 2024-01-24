from pathlib import Path
import cv2
import face_recognition as fr

class FacialRecognition:
    def __init__(self, folder_path):
        self.fotos_list = []
        self.locations = []
        self.cod_faces = []
        self.results = []
        self.cara_control = None  # Variable para almacenar la cara de control
        self.caras_folder = Path(folder_path)

    def cargar_imagenes(self):
        paths = [str(file) for file in self.caras_folder.glob('*.jpg')]
        self.fotos_list = [fr.load_image_file(path) for path in paths]

    def asignar_perfil_color(self):
        self.fotos_list = [cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in self.fotos_list]

    def localizar_cara(self):
        self.locations = [fr.face_locations(f)[0] for f in self.fotos_list]

    def get_cod_faces(self):
        self.cod_faces = [fr.face_encodings(f)[0] for f in self.fotos_list]

    def draw_rectangles(self):
        for (f, l) in zip(self.fotos_list, self.locations):
            cv2.rectangle(f,
                          (l[3], l[0]),
                          (l[1], l[2]),
                          (0, 255, 0), 2)

    def show_imgs(self):
        for index, f in enumerate(self.fotos_list):
            cv2.imshow(f'Foto {index}', f)

    def compare_all_with_control(self):
        results = []
        for i, fc in enumerate(self.cod_faces):
            if i > 0:
                diferencias = {'misma_cara': fr.compare_faces([self.cara_control], fc),
                               'distancia': fr.face_distance([self.cara_control], fc)}
            elif i == 0:
                diferencias = {'misma_cara': 'control',
                               'distancia': '0'}
            results.append(diferencias)

        self.results = results

    def show_results(self):
        for d, f in zip(self.results, self.fotos_list):
            resultado = d['misma_cara']
            distancia = d['distancia'][0]
            cv2.putText(f, f'{resultado} :::: {distancia}',
                        (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    def run(self):
        cap = cv2.VideoCapture(0)  # Iniciar la captura de video con la cámara del portátil
        ret, self.cara_control = cap.read()  # Capturar la cara de control desde la cámara
        cap.release()  # Liberar la cámara después de capturar la cara de control

        self.cargar_imagenes()
        self.asignar_perfil_color()
        self.localizar_cara()
        self.get_cod_faces()
        self.draw_rectangles()
        self.compare_all_with_control()  # Comparar con la cara de control
        self.show_results()
        self.show_imgs()
        cv2.waitKey(0)
