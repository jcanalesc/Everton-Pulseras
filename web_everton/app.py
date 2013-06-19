# -*- coding: utf-8 -*-
from flask import *
from werkzeug import secure_filename
import os
import glob

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static/uploads/")
SAVE_FOLDER = os.path.join(os.getcwd(), "static/saves/")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "tiff", "tif"]

@app.route("/")
def index():
	def nombrearch(str):
		return str.rsplit("/",1)[1].rsplit(".", 1)[0]
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
        file_url = os.path.join("/static/uploads/", filename)
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
	return "success"

if __name__ == "__main__":
	app.run("0.0.0.0", debug=True)