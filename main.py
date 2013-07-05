# -*- coding: utf-8 -*-
from Tkinter import *
from ttk import *
import tkFileDialog, tkSimpleDialog, tkMessageBox
import webbrowser
import winctrlc
import httplib, urllib
import json
import os

AUTH_HOST = "localhost"
AUTH_PORT = 5000
SKIP_LOGIN = True

class LoginWindow(Toplevel):
    def inicializa(self):
        Label(self, text="Usuario").grid(row=0, sticky=W, pady=5)
        Label(self, text=u"Contraseña").grid(row=1, sticky=W, pady=5)
        self.usuario = Entry(self)
        self.contrasena = Entry(self)
        self.conectar = Button(self, text="Conectar", command=self.autenticar)
        self.usuario.grid(row=0, column=1, pady=5)
        self.contrasena.grid(row=1, column=1, pady=5)
        self.conectar.grid(row=2, columnspan=2, pady=5)
        self.texto_estado = StringVar()
        self.texto_estado.set(u"Esperando conexión")
        Label(self, textvariable=self.texto_estado).grid(row=3, columnspan=2, pady=5)
        self.wm_protocol("WM_DELETE_WINDOW", self.padre.close_handler)


    def autenticar(self):
        user = self.usuario.get()
        if len(user) < 1:
            self.texto_estado.set("Ingrese un nombre de usuario!")
            return
        passwd = self.contrasena.get()
        if len(passwd) < 1:
            self.texto_estado.set(u"Ingrese una contraseña!")
            return
        self.texto_estado.set("Conectando...")
        try:
            connection = httplib.HTTPConnection(AUTH_HOST, AUTH_PORT)
            params = urllib.urlencode({"userid": user, "passwd": passwd})
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            connection.request("POST", "/authenticate", params, headers)
            resp = connection.getresponse()
            if resp.status == 200:
                datadict = json.loads(resp.read())
                if datadict["auth"] == True:
                    tkMessageBox.showinfo("HandBand", u"Identificación exitosa.")
                    self.destroy()
                else:
                    self.texto_estado.set(u"Datos inválidos. Compruebe usuario y clave.")
            else:
                self.texto_estado.set(u"Problemas al intentar iniciar su sesión.")
        except:
            self.texto_estado.set(u"Imposible conectar con el servidor de autenticación.")



class MainWindow(Tk):
    def inicializa(self):
        self.texto_archivo = StringVar()
        self.texto_archivo.set("Archivo seleccionado: Ninguno")
        Label(self, textvariable=self.texto_archivo).grid(row=0, columnspan=2, sticky=W)
        self.selector_archivo = Button(self, text="Clic para buscar archivo...", command=self.get_archivo)
        self.selector_archivo.grid(row=1, columnspan=2)
        Button(self, text="Generar XMLs", command=self.generar_xmls).grid(row=2,column=0)
        Button(self, text="Generar PDFs", command=self.generar_pdfs).grid(row=3,column=0)
        """
        self.pb = Progressbar(self, mode="indeterminate", orient=HORIZONTAL)
        self.pb.grid(row=4, columnspan=2)
        self.pb.start()
        """
        self.last_file = None
        self.webprocess = None
        self.wm_protocol("WM_DELETE_WINDOW", self.close_handler)
        if not SKIP_LOGIN:
            self.wLogin = LoginWindow()
            self.wLogin.padre = self
            self.wLogin.inicializa()
            self.wLogin.transient(self)
            self.wLogin.grab_set() 
            self.wait_window(self.wLogin)

    def get_archivo(self):
        fn = tkFileDialog.askopenfilename(parent=self, title="Elija archivo", filetypes=[("Archivos de eventos", "*.json")], initialdir="static\\saves\\")
        if fn != None and len(fn) > 0:
            tkMessageBox.showinfo("Archivo seleccionado", "Usted ha seleccionado el archivo \"%s\"" % fn)
            self.last_file = fn
            fn_nombre = os.path.basename(fn)
            self.texto_archivo.set("Archivo seleccionado: " + fn_nombre)

    def close_handler(self):
        if self.webprocess != None:
            self.webprocess.send_ctrl_c()
        self.destroy()
        self.quit()

    def start_web_server(self):
        self.webprocess = winctrlc.Popen("python web_everton\\app.py", "log.log")

    def generar_xmls(self):
        pass
    def generar_pdfs(self):
        pass

app = MainWindow()
app.inicializa()
app.mainloop()