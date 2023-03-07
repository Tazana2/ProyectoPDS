from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from customtkinter import *
import cv2


from FaceRecognitionModule import FaceRecognition


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recoginition Project")
        self.geometry("600x600")
        self.bind('<Escape>', lambda e: self.quit())
        self.vid = None

        self.frame = CTkFrame(self)
        self.frame.pack(pady=40, padx=50, fill="both", expand=True)

        self.main_title = CTkLabel(self.frame, text="¡Bienvenido!", font=("Monocraft", 28)).pack(pady=20)

        self.container_register = CTkFrame(self.frame)
        self.container_register.pack(pady=15, padx=20, fill="both", expand=True)

        self.container_login = CTkFrame(self.frame)
        self.container_login.pack(pady=15, padx=20, fill="both", expand=True)


        self.label1 = CTkLabel(self.container_register, text="Registrate", font=("Monocraft", 20))
        self.label1.pack(pady=25)

        self.nameText = Variable()
        self.entry_name = CTkEntry(
            self.container_register, 
            textvariable=self.nameText, 
            placeholder_text="Escribe tu nombre", 
            font=("Monocraft", 12)
        )
        self.entry_name.pack(padx=100, fill="x")

        self.button_register = CTkButton(
            self.container_register,
            text="Registrate",
            font=("Monocraft", 12),
            command=self.checkNameEntry
        )
        self.button_register.pack(pady=10)


        self.label2 = CTkLabel(self.container_login, text="Iniciar Sesión", font=("Monocraft", 20))
        self.label2.pack(pady=30)

        self.button_login = CTkButton(self.container_login, text="Ingresar", font=("Monocraft", 12), command=self.bruh)
        self.button_login.pack()


    def createTopLevel(self, whatIsfor=""):
        self.nwWindow = CTkToplevel(self)
        self.nwWindow.title("Authentication")
        self.nwWindow.geometry("550x550")
        if whatIsfor == "Register":
            self.registerWin()
        elif whatIsfor == "Login":
            self.loginWin()

    def closeTopLevel(self):
        self.entry_name.delete(0, END)
        self.nwWindow.destroy()
        self.nwWindow.update()
        if self.vid:
            self.vid.release()

    def openCamera(self):
        cv_image = cv2.flip(cv2.cvtColor(self.vid.read()[1], cv2.COLOR_BGR2RGBA), 1)
        captured_image = Image.fromarray(cv_image)
        photo_image = ImageTk.PhotoImage(image=captured_image)

        self.cam_widget.photo_image = photo_image
        self.cam_widget.configure(image=photo_image)
        self.cam_widget.after(10, self.openCamera)


    def take_photo_register(self):
        try:
            cv2.imwrite(f".\Faces\{self.nameText.get()}.jpg", cv2.flip(self.vid.read()[1], 1))
            self.closeTopLevel()
            messagebox.showinfo(
                message="¡Te has registrado con éxito!",
                title="Registro completado"
            )
        except:
            self.closeTopLevel()
            messagebox.showerror(
                message="Ha ocurrido al registrarte. Revisa tu cámara o el campo del nombre (Recuerda que no puede tener caracteres especiales) y vuelve a intentar." ,
                title="Error:"
            )

    def registerWin(self):
        try:
            self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
            self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        except:
            self.closeTopLevel()
            messagebox.showerror(
                message="Ha ocurrido un error al detectar tu dispositivo de video. Revísalo y vuelve a intentar.",
                title="Error:"
            )

        self.cam_widget = Label(self.nwWindow)
        self.cam_widget.pack(pady=20, padx=20)

        capBtn = CTkButton(self.nwWindow, text="Tomar Foto", command=self.take_photo_register, font=("Monocraft", 12))
        capBtn.pack(pady=10)

        clBtn = CTkButton(self.nwWindow, text="Salir", command=self.closeTopLevel, font=("Monocraft", 12))
        clBtn.pack()
        self.openCamera()

    def loginWin(self):
        try:
            self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
            self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        except:
            self.closeTopLevel()
            messagebox.showerror(
                message="Ha ocurrido un error al detectar tu dispositivo de video. Revísalo y vuelve a intentar.",
                title="Error:"
            )

        self.cam_widget = Label(self.nwWindow)
        self.cam_widget.pack(pady=20, padx=20)

        label_recomendation = CTkLabel(self.nwWindow, text="Recuerda:\n\nEs mejor si estás en un lugar iluminado \ny con nadie más que tú en la cámara.", font=("Monocraft", 14))
        label_recomendation.pack(pady=10)

        capBtn = CTkButton(self.nwWindow, text="Iniciar Reconocimiento", command=self.startAuthentication, font=("Monocraft", 12))
        capBtn.pack(pady=10)

        clBtn = CTkButton(self.nwWindow, text="Salir", command=self.closeTopLevel, font=("Monocraft", 12))
        clBtn.pack()

        self.openCamera()

    def checkNameEntry(self):
        if self.nameText.get() != "": self.createTopLevel(whatIsfor="Register")
        else:
            messagebox.showerror(
                message="Tienes que ingresar toda la información para registrarte.",
                title="Error:"
            )

    def startAuthentication(self):
        try:
            m = FaceRecognition(path=".\\Faces", cap=self.vid)
            m.save_info()
            name = m.start_recognition()
            if name in m.names:
                self.closeTopLevel()
                messagebox.showinfo(
                    message=f"Bienvenido {name}",
                    title="Inicio de sesión exitoso"
                )
            else:
                self.closeTopLevel()
                messagebox.showerror(
                    message="Usted no está registrado o no se le pudo reconocer.",
                    title="Error:"
                )
        except:
            self.closeTopLevel()
            messagebox.showerror(
                message="Ha ocurrido un error al realizar la autenticación.",
                title="Error:"
            )

    def bruh(self):
        self.createTopLevel(whatIsfor="Login")