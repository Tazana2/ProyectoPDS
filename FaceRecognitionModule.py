import face_recognition
import cv2
import os

class FaceRecognition:
    def __init__(self, path="", names=[], savedFaces=[], cap=None):
        self.names = names
        self.path = path
        self.savedFaces = savedFaces
        self.cap = cap

    def save_info(self):
        self.names = [name[:name.index('.')] for name in os.listdir(self.path)]
        faces = [cv2.imread(os.path.join(self.path, image)) for image in os.listdir(self.path)]
        self.savedFaces = [face_recognition.face_encodings(i, known_face_locations=[face_recognition.face_locations(i)[0]], model="small")[0] for i in faces]

    def start_recognition(self):
        # Ingresar los frames de la cámara principal del dispositivo
        ret, frame = self.cap.read()
        if ret == False: return IndexError
        frame = cv2.flip(frame, flipCode=1)
        # Encontrar las coordenadas de todos los rostros presentes
        faceCor = face_recognition.face_locations(frame)
        # A cada rostro encontrado se le toman sus caracteristicas y se le hace un rectangulo en donde se encuentre
        if faceCor != []:
            for eachFace in faceCor:
                faceEnco = face_recognition.face_encodings(frame, known_face_locations=[eachFace], model="small")
                for face in faceEnco:
                    match = face_recognition.compare_faces(self.savedFaces, face)
                    if True in match:
                        # Acá es donde va a estar el espacio para la autenticación
                        myText = self.names[match.index(True)]
                        return myText