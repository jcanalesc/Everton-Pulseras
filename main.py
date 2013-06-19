# -*- coding: utf-8 -*-
from Tkinter import *
import tkFileDialog, tkSimpleDialog, tkMessageBox
import webbrowser
import winctrlc

class LoginWindow(Toplevel):
    def inicializa(self):
        Label(self, text="Usuario").grid(row=0, sticky=W, pady=5)
        Label(self, text=u"Contraseña").grid(row=1, sticky=W, pady=5)
        self.usuario = Entry(self)
        self.contrasena = Entry(self)
        self.conectar = Button(self, text="Conectar")
        self.usuario.grid(row=0, column=1, pady=5)
        self.contrasena.grid(row=1, column=1, pady=5)
        self.conectar.grid(row=2, columnspan=2, pady=5)

class MainWindow(Tk):
    def inicializa(self):
        Label(self, text="Seleccionar evento").grid(row=0, columnspan=5, sticky=W)
        self.selector_archivo = Button(self, text="Clic para buscar archivo...", command=self.get_archivo)
        self.selector_archivo.grid(row=1, columnspan=4)
        self.last_file = None
        self.webprocess = None
        self.wm_protocol("WM_DELETE_WINDOW", self.close_handler)
        self.wLogin = LoginWindow()
        self.wLogin.inicializa()
        self.wLogin.withdraw()

    def get_archivo(self):
        fn = tkFileDialog.askopenfilename(parent=self, title="Elija archivo", filetypes=[("Archivos de eventos", "*.json")], initialdir="static\\saves\\")
        if fn != None and len(fn) > 0:
            tkMessageBox.showinfo("Archivo seleccionado", "Usted ha seleccionado el archivo \"%s\"" % fn)
            self.last_file = fn

    def close_handler(self):
        if self.webprocess != None:
            self.webprocess.send_ctrl_c()
        self.destroy()
        self.quit()

    def start_web_server(self):
        self.webprocess = winctrlc.Popen("python web_everton\\app.py", "log.log")



app = MainWindow()
app.inicializa()
app.mainloop()