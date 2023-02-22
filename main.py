import face_recognition
import cv2

daniel = cv2.imread("Faces/Daniel.jpg")
samuel = cv2.imread("Faces/Samuel.jpg")
faces = [daniel, samuel]
names = ["Daniel", "Samuel"]

# felipe = cv2.imread("Faces/Felipe.jpg")
savedFaces = []
for i in faces:
    savedFaces.append(face_recognition.face_encodings(i, known_face_locations=[face_recognition.face_locations(i)[0]])[0])


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
            faceEnco = face_recognition.face_encodings(frame, known_face_locations=[eachFace])
            # Comparar el Frame con el rostro de la imagen
            myText = "Unknow"
            myColor = (0, 0, 255)
            for face in faceEnco:
                match = face_recognition.compare_faces(savedFaces, face)
                if True in match:
                    name = names[match.index(True)]
                    myText = name
                    myColor = (0, 255, 0)

            # cv2.rectangle(frame, (eachFace[3], eachFace[0]), (eachFace[1], eachFace[2] + 30), myColor, -1)
            # cv2.rectangle(frame, (eachFace[3], eachFace[0]), (eachFace[1], eachFace[2]), myColor, 2)
            cv2.putText(frame, myText, (eachFace[3],eachFace[2]+ 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2)


    cv2.imshow("a", frame)

    k = cv2.waitKey(1)
    if  k == 27 & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()