import face_recognition
import cv2

from modules.PersistenceModule import Persistence
class FaceRecognition:
    def __init__(self, cap=None, source="", authNames=[]):
        self.cap = cap
        self.source = source
        self.authNames = authNames

    def start_authentication(self):
        ret, frame = self.cap.read()
        if ret == False: return IndexError
        frame = cv2.flip(frame, flipCode=1)
        faceCor = face_recognition.face_locations(frame)
        data = Persistence(path=self.source)
        data.save_info()
        self.authNames = data.names
        if faceCor != []:
            for eachFace in faceCor:
                faceEnco = face_recognition.face_encodings(frame, known_face_locations=[eachFace], model="large")
                for face in faceEnco:
                    match = face_recognition.compare_faces(data.savedFaces, face, tolerance=0.4)
                    if True in match:
                        # Acá es donde va a estar el espacio para la autenticación
                        self.myName = self.authNames[match.index(True)] 
                    else:
                        self.myName = ""