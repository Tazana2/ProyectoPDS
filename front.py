from tkinter import *
from customtkinter import *

from tkinter import messagebox
import cv2

# from main import FaceRecognition

from PIL import Image, ImageTk


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recoginition Project")
        self.geometry("600x600")
        self.bind('<Escape>', lambda e: self.quit())

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

        self.button_login = CTkButton(self.container_login, text="Ingresar", font=("Monocraft", 12), command=self.createTopLevel)
        self.button_login.pack()


    def createTopLevel(self):
        self.nwWindow = CTkToplevel(root)
        self.nwWindow.title("Authentication")
        self.nwWindow.geometry("500x500")
        if self.nameTop == "Register":
            self.registerWin()

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
                message="Te has registrado con éxito! :D",
                title="Registro completado"
            )
        except:
            self.closeTopLevel()
            messagebox.showerror(
                message="Ha ocurrido al registrate. Revisa tu cámara o el campo del nombre (Recuerda que no puede tener cáracteres especiales) y vuelve a intentar D:" ,
                title="Error:"
            )

    def registerWin(self):
        try:
            self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
            self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        except:
            self.closeTopLevel()
            messagebox.showerror(
                message="Ha ocurrido un error al detectar tu dispositivo de video. Revisalo y vuelve a intentar.",
                title="Error:"
            )

        self.cam_widget = Label(self.nwWindow)
        self.cam_widget.pack(pady=20, padx=20)

        capBtn = CTkButton(self.nwWindow, text="Tomar Foto", command=self.take_photo_register)
        capBtn.pack(pady=10)

        clBtn = CTkButton(self.nwWindow, text="Salir", command=self.closeTopLevel)
        clBtn.pack()
        self.openCamera()

    def checkNameEntry(self):
        self.nameTop = "Register"
        if self.nameText.get() != "": self.createTopLevel()
        else:
            messagebox.showerror(
                message="Tienes que ingresar toda la información para registrarte",
                title="Error:"
            )



if __name__ == "__main__":
    root = App()
    root.mainloop()