import face_recognition
import cv2
import os

class Persistence:
    def __init__(self, path="", names=[], savedFaces=[]):
        self.names = names
        self.path = path
        self.savedFaces = savedFaces

    def save_info(self):
        self.names = [name[:name.index('.')] for name in os.listdir(self.path)]
        faces = [cv2.imread(os.path.join(self.path, image)) for image in os.listdir(self.path)]
        self.savedFaces = [face_recognition.face_encodings(i, known_face_locations=[face_recognition.face_locations(i)[0]], num_jitters=2,model="large")[0] for i in faces]
        # Res is not used yet
        self.res = dict(zip(self.names, self.savedFaces))
        
        print(self.res)
