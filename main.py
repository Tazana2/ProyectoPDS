import face_recognition
import cv2


# Abrir la imagen y encontrar las cordenadas de un solo rostro
myImage = cv2.imread("Faces/Daniel.jpg")
faceCor = face_recognition.face_locations(myImage)[0]

# Tomar las caracteristicas del rostro dentro de la carpeta en un Array
faceEncoImg = face_recognition.face_encodings(myImage, known_face_locations=[faceCor])[0]


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
            faceEnco = face_recognition.face_encodings(frame, known_face_locations=[eachFace])[0]
            # Comparar el Frame con el rostro de la imagen
            match = face_recognition.compare_faces([faceEnco], faceEncoImg)
            # print(f"El rostro es el mismo que el de la imagen?: {match}")

            if match[0] == True:
                myText = "Daniel"
                myColor = (0, 255, 0)
            else:
                myText = "Unknown"
                myColor = (0, 0, 255)

            # cv2.rectangle(frame, (eachFace[3], eachFace[0]), (eachFace[1], eachFace[2] + 30), myColor, -1)
            cv2.rectangle(frame, (eachFace[3], eachFace[0]), (eachFace[1], eachFace[2]), myColor, 2)
            cv2.putText(frame, myText, (eachFace[3],eachFace[2]+ 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)


    cv2.imshow("a", frame)

    k = cv2.waitKey(1)
    if  k == 27 & 0xFF:
        break

cap.release()
cv2.destroyAllWindows()