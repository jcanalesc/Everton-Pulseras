# -*- coding: utf-8 -*-
from flask import *
from werkzeug import secure_filename
import os
import glob
import crea_imagenes
from Tkinter import Tk
import tkFileDialog, tkSimpleDialog, tkMessageBox
import httplib, urllib

AUTH_HOST = "186.64.120.145"
AUTH_PORT = 80


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads", "")
SAVE_FOLDER = os.path.join(os.getcwd(), "static", "saves", "")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "tiff", "tif"]

@app.route("/")
def index():
	def nombrearch(str):
		return str.rsplit(os.sep, 1)[1].rsplit(".", 1)[0]
	file_list = map(nombrearch,glob.glob(os.path.join(SAVE_FOLDER, "*.json")))
	return render_template("main.html", archivos=file_list)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/subeArchivo', methods=['POST'])
def upload_file():
    file = request.files['archivo']
    if not file:
    	return render_template("error_subida.html", mensaje="Error en la subida del archivo.")
    elif not allowed_file(file.filename):
    	return render_template("error_subida.html", mensaje=u"El archivo no es un archivo de imagen válido.")
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = "/static/uploads/"+filename
        return render_template("subida_exitosa.html", archivo=file_url, etiqueta=request.form["etiqueta"])

@app.route("/guardaEvento", methods=['POST'])
def guarda_evento():
	try:
		nombre = secure_filename(request.form['nombre'])
		fp = open(os.path.join(SAVE_FOLDER, nombre + ".json"), "w+")
		fp.write(json.dumps(request.form))
		return "success"
	except Exception as e:
		return "failure: " + str(e)

@app.route("/cargaEvento", methods=['GET'])
def cargar_evento():
	arch = request.args.get("archivo", "")
	if arch == "":
		return "failure";
	else:
		fp = open(os.path.join(SAVE_FOLDER, arch + ".json"), "r")
		return jsonify(json.loads(fp.read()))

@app.route("/generaXML", methods=['POST'])
def generar_xml():
	datos_pagina = request.form
	crea_imagenes.inicializar_variables(datos_pagina)
	crea_imagenes.genera_xml_todos()
	return "success"

@app.route("/generaPDF", methods=['POST'])
def generar_entradas():
	datos_pagina = request.form
	crea_imagenes.inicializar_variables(datos_pagina)
	crea_imagenes.genera_fotos()
	return "success"



if __name__ == "__main__":
	# try:
	# 	root = Tk()
	# 	root.geometry("+500+500")
	# 	root.withdraw()
	# 	user = tkSimpleDialog.askstring("HandBand", "Ingrese nombre de usuario:", parent=root)
	# 	if user is None or len(user) == 0:
	# 		tkMessageBox.showerror("HandBand", u"No se ingresó ningún usuario.")
	# 		raise

	# 	passwd = tkSimpleDialog.askstring("HandBand", u"Ingrese contraseña:", parent=root)
	# 	if passwd is None or len(passwd) == 0:
	# 		tkMessageBox.showerror("HandBand", u"No se ingresó contraseña.")
	# 		raise

	# 	connection = httplib.HTTPConnection(AUTH_HOST, AUTH_PORT)
	# 	params = urllib.urlencode({"userid": user, "passwd": passwd})
	# 	headers = {
	# 	"Content-type": "application/x-www-form-urlencoded",
	# 	"Accept": "application/json"
	# 	}
	# 	connection.request("POST", "/authenticate", params, headers)
	# 	resp = connection.getresponse()
	# 	if resp.status == 200:
	# 		datadict = json.loads(resp.read())
	# 		if datadict["auth"] == True:
	# 			tkMessageBox.showinfo("HandBand", u"Identificación exitosa.")
	# 			app.run("0.0.0.0", debug=True)
	# 		else:
	# 			tkMessageBox.showerror("HandBand", u"Datos inválidos. Compruebe usuario y clave.")
	# 	else:
	# 		tkMessageBox.showerror("HandBand", u"Problemas al intentar iniciar su sesión.")
	# except Exception as exc:
	# 	print exc
	# 	quit()
	app.run("0.0.0.0", debug=True)