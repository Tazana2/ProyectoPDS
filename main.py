import face_recognition
import cv2
import os

# Se "procesan" las imágenes que estén en el directorio y se le guarda su nombre (nombre_archivo)
path = ".\\Faces"
faces = [cv2.imread(os.path.join(path, image)) for image in os.listdir(path)]
names = [name[:name.index('.')] for name in os.listdir(path)]

savedFaces = []
for i in faces:
    savedFaces.append(face_recognition.face_encodings(i, known_face_locations=[face_recognition.face_locations(i)[0]], model="small")[0])


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Ingresar los frames de la cámara principal del dispositivo
    ret, frame = cap.read()
    if ret == False: break
    frame = cv2.flip(frame, flipCode=1)

    # Encontrar las coordenadas de todos los rostros presentes
    faceCor = face_recognition.face_locations(frame)

    # A cada rostro encontrado se le toman sus caracteristicas y se le hace un rectangulo en donde se encuentre
    if faceCor != []:
        for eachFace in faceCor:
            faceEnco = face_recognition.face_encodings(frame, known_face_locations=[eachFace], model="small")
            # Comparar el Frame con el rostro de la imagen
            myText = "Unknow"
            myColor = (0, 0, 255)
            for face in faceEnco:
                match = face_recognition.compare_faces(savedFaces, face)
                if True in match:
                    # Acá es donde va a estar el espacio para la autenticación
                    name = names[match.index(True)]
                    myText = name
                    myColor = (0, 255, 0)
            cv2.putText(frame, myText, (eachFace[3],eachFace[2]+ 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2)


    cv2.imshow("Authentication", frame)

    k = cv2.waitKey(1)
    if  k == 27 & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()