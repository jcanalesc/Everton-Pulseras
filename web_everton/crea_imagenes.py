# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw
import Code128b
from lxml import etree
import sys
from optparse import OptionParser
import json
import os
pagina = 1
Buf = []

SERIE = 1

fuente = ImageFont.truetype("arial.ttf",35)
fuente_chica = ImageFont.truetype("arial.ttf", 22)
fuente_serie = ImageFont.truetype("arial.ttf", 20)
fuentes_datos = [ImageFont.truetype("Arial_Bold.ttf", 28), ImageFont.truetype("Arial.ttf", 20)]

ancho_foto_texto = 700

descripcion = u"Everton vs Wanderers\nMartes 16 de Julio\n15:30 hrs.\nEstadio Lucio Fariña"

sectores = ["Preferencial",u"Galería"]
fotos_entradas = {
	(u'01','33'): "../haztesocio.jpg",
	(u'02','33'): "../haztesocio.jpg"
}
color_recuadro = {
	"Preferencial": 	(0xFF, 0xC5, 0x0C, 255),
	u"Galería":			(0, 0, 0xFF, 255)
}

segmentos = {
	"33": [u"Promoción Entel", 100, 200]
	# "01": [u"Dirigentes",		24, 4, 30],
	# "02": [u"Jugadores y CT", 	90, 50, 20],
	# "03": [u"Go Zuko",			0, 4, 0],
	# "04": [u"Coca Cola",		4, 5, 0],
	# "05": [u"Gaucho",			2, 18, 0],
	# "06": [u"O Concept",		5, 0, 5],
	# "07": [u"Productos Fernandez",	2, 20, 0],
	# "08": [u"Clínica Reñaca",		14, 0, 0],
	# "09": [u"Clos de Pirque",		0, 10, 0],
	# "10": [u"Radio Valparaíso",		0, 5, 0],
	# "11": [u"Radio Portales",		0, 5, 0],
	# "12": [u"Radio UCV",			0, 10, 0],
	# "13": [u"Radio Festival",		8, 0, 0],
	# "14": [u"Carlos Williams",		8, 0, 0],
	# "15": [u"Radio Pasión del Cerro",	0, 0, 10],
	# "16": [u"Radio Carnaval",			0, 0, 4],
	# "17": [u"Radio Amor",				0, 2, 0],
	# "18": [u"Quintavisión",				0, 5, 0],
	# "19": [u"Administrativos",			3, 18, 2],
	# "20": [u"Municipalidad",			0, 0, 360],
	# "21": [u"Estadio Quillota",			30, 0, 10],
	# "22": [u"Concejales",				20, 0, 0],
	# "23": [u"Virginia Reginato",		10, 0, 0],
	# "24": [u"María Angélica Maldonado",	10, 0, 0],
	# "25": [u"Club Visita",				30, 0, 0],
	# "26": [u"Compromisos",				4, 20, 7],
	# "27": [u"Univ. Viña del Mar",		0, 100, 0],
	# "28": [u"Galería Everton",			0, 0, 1300],
	# "29": [u"Galería Visita",			0, 0, 500],
	# "30": [u"Preferencial",				200, 0, 0],
	# "31": [u"Andes",					0, 400, 0]
}

# no se generan pulseras para estos
segmentos_adicionales = {
	#"40": [u"Butaca",						2000, 0, 0],
	#"41": [u"Preferencial",					2000, 0, 0],
	#"42": [u"Andes Vip",					0, 2000, 0],
	#"43": [u"Andes Simpatizante",			0, 2000, 0],
	#"44": [u"Hincha Vip",					0, 0, 2000],
	#"45": [u"Hincha Simpatizante",			0, 0, 2000],
	#"46": [u"Simpatizante",					0, 0, 2000]
}

def ajustar(img,**kwargs):
	w, h = img.size
	factor = 1
	if "alto" in kwargs:
		factor = kwargs["alto"] / float(h) * 1.0
		print factor
		c = img.copy()
		c.thumbnail(((int(w * factor), int(h * factor))), Image.ANTIALIAS)
		return c
	elif "ancho" in kwargs:
		factor = kwargs["ancho"] / float(w) * 1.0
		print factor
		c = img.copy()
		c.thumbnail(((int(w * factor), int(h * factor))), Image.ANTIALIAS)
		return c
	else:
		raise Exception("no argument found")



def flush_buf():
	global Buf, pagina
	W, H = Buf[0].size
	L = Image.new("RGBA", (W, H*10), (255,255,255,255))
	print len(Buf)
	for i in range(len(Buf)):
		L.paste(Buf[i], (0, i*H))
	dpi = 450
	margen_superior = 1.1
	ancho_pag = int(dpi * (7.5))
	alto_pag = int(dpi * 10)
	Doc = Image.new("RGB", (ancho_pag, alto_pag), (255,255,255))
	L = L.rotate(-90,expand=True)
	lw, lh = L.size
	escala = ancho_pag*1.0 / lw
	L = L.resize((int(lw*escala), int(lh*escala)))
	Doc.paste(L, (0, int(margen_superior*dpi), L.size[0], int(margen_superior*dpi) + L.size[1]))
	Doc.save("pdfs_prueba/pagina%d.pdf" % pagina, "PDF", resolution=dpi)
	pagina = pagina +1
	Buf = []

def agrega_entrada2(codigo, sector, tipo_foto, segmento):
	imagen_ref = ajustar(tipo_foto, alto=160)
	print imagen_ref
	"""
	if segmento not in sectores and segmento not in [u"Galería Everton", u"Galería Visita"]:
		imagen_ref = cort[tipo_foto]
	else:
		imagen_ref = foto[tipo_foto]
	"""
	alto_total = imagen_ref.size[1] + 20

	foto_codigo = Code128b.code128_image(codigo)
	
	foto_codigo = ajustar(foto_codigo, alto=alto_total)
	ancho_datos = foto_codigo.size[0]/2
	alto_recuadro = foto_codigo.size[1] + 30
	ancho_recuadro = foto_codigo.size[0] + 80
	margen_sup = 10

	margen_recuadro = 24
	

	inicio_recuadro = (foto_codigo.size[0] + margen_recuadro, margen_recuadro)
	fin_recuadro = (inicio_recuadro[0] + ancho_recuadro, inicio_recuadro[1] + alto_recuadro)

	ancho_datos = 350
	alto_datos = foto_codigo.size[1] + 30

	inicio_datos = (fin_recuadro[0] + 5, inicio_recuadro[1])
	fin_datos = (inicio_datos[0] + ancho_datos, inicio_datos[1] + alto_datos)

	ancho_total = imagen_ref.size[0] + foto_codigo.size[0] + ancho_datos + margen_recuadro*2 + ancho_recuadro


	lienzo = Image.new("RGBA", (ancho_total, alto_total), (255,255,255,255))


	lienzo.paste(foto_codigo, (0, 30))
	lienzo.paste(imagen_ref, (ancho_total - imagen_ref.size[0], 10))

	# agregar texto

	drawer = ImageDraw.Draw(lienzo)
	

	margen_lat = int((ancho_recuadro - fuente.getsize(sector.upper())[0])/2)
	

	COLOR = color_recuadro[sector]
	if segmento == u"Galería Visita":
		COLOR = color_recuadro[segmento]

	drawer.rectangle([inicio_recuadro, fin_recuadro], fill=COLOR)

	drawer.text((inicio_recuadro[0] +  margen_lat, inicio_recuadro[1] + margen_sup), sector.upper(), font=fuente)

	if segmento not in sectores:
		margen_sup = margen_sup + 50
		margen_lat = int((ancho_recuadro - fuente_chica.getsize(segmento.upper())[0]) / 2)
		drawer.text((inicio_recuadro[0] + margen_lat, inicio_recuadro[1] + margen_sup), segmento.upper(), font=fuente_chica, fill=(255,255,255,255))

		if segmento not in [u"Galería Everton", u"Galería Visita", u"Promoción Entel"]:
			texto_cortesia = "Prohibida su venta".upper()
			margen_sup = fin_recuadro[1] + 5
			margen_lat = inicio_recuadro[0] + int((ancho_recuadro - fuente_serie.getsize(texto_cortesia)[0]) / 2)
			drawer.text((margen_lat, margen_sup), texto_cortesia, font=fuente_serie, fill=(0,0,0,255))

	# datos evento

	

	datos = descripcion.split("\n")

	margen_izq = inicio_datos[0] + int(ancho_datos - fuentes_datos[0].getsize(datos[0])[0]) / 2
	margen_sup = inicio_datos[1]

	drawer.text((margen_izq, margen_sup), datos[0], font=fuentes_datos[0], fill=COLOR)

	for i in range(1,len(datos)):
		margen_sup += 30
		margen_izq = inicio_datos[0] + int(ancho_datos - fuentes_datos[1].getsize(datos[i])[0]) / 2

		drawer.text((margen_izq, margen_sup), datos[i], font=fuentes_datos[1], fill=COLOR)	


	# numero de serie

	global SERIE

	texto_serie = "%04d" % SERIE

	foto_serie = Image.new("RGBA", (120 + 48, 30), (255,255,255,0))

	wr = ImageDraw.Draw(foto_serie)

	marg =  int((117  + 48 - fuente_serie.getsize(texto_serie)[0]) / 2)

	wr.text((marg,0), texto_serie, font=fuente_serie, fill=(0,0,0,255))

	foto_serie = foto_serie.rotate(90, expand=True)

	wr = ImageDraw.Draw(foto_serie)

	wr.rectangle((0, 0, foto_serie.size[0]+1, 3), outline=(255,255,255,255), fill=(255,255,255,255))
	

	lienzo.paste(foto_serie, (0,0))


	SERIE += 1

	achique = 1

	return lienzo.resize((int(lienzo.size[0]*achique), int(lienzo.size[1]*achique)))

def genera_xml(sector):
	root = etree.Element('localidades')
	for i, v in enumerate(sectores):
		for cod_seg, props in segmentos.iteritems():
			if props[i+1] > 0:
				localidad = etree.SubElement(root, 'localidad')
				codLoc = etree.SubElement(localidad, 'codLoc')
				codLoc.text = "%02d" % (i+1)
				nombreLoc = etree.SubElement(localidad, 'nombreLoc')
				nombreLoc.text = v
				activa = etree.SubElement(localidad, 'activa')
				activa.text = "1" if v == sector else "0"
				idUsr = etree.SubElement(localidad, 'idUsr')
				idUsr.text = cod_seg
				nombreUsr = etree.SubElement(localidad, 'nombreUsr')
				nombreUsr.text = props[0]
				entradas = etree.SubElement(localidad, 'entradas')
				entradas.text = str(props[i+1])

		for cod_seg, props in segmentos_adicionales.iteritems():
			if props[i+1] > 0:
				localidad = etree.SubElement(root, 'localidad')
				codLoc = etree.SubElement(localidad, 'codLoc')
				codLoc.text = "%02d" % (i+1)
				nombreLoc = etree.SubElement(localidad, 'nombreLoc')
				nombreLoc.text = v
				activa = etree.SubElement(localidad, 'activa')
				activa.text = "1" if v == sector else "0"
				idUsr = etree.SubElement(localidad, 'idUsr')
				idUsr.text = cod_seg
				nombreUsr = etree.SubElement(localidad, 'nombreUsr')
				nombreUsr.text = props[0]
				entradas = etree.SubElement(localidad, 'entradas')
				entradas.text = str(props[i+1])
	return etree.tostring(root, pretty_print=True, encoding="UTF-8")

"""
for tipo_foto, segmentos in rangos.iteritems():
	for titulo, datos in segmentos.iteritems():
		cantidad = datos[0]
		sufijo = datos[1]
		sector = datos[2]
		for n in range(cantidad):
			codigo_completo = "%03d%s" % (n+1, sufijo)
			agrega_entrada2(codigo_completo,sector,tipo_foto,titulo)

"""

def genera_xml_todos():
	for i,v in enumerate(sectores):
		fp = open("permisos_%s.xml" % v, "w+")
		fp.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
		fp.write(genera_xml(v).replace(os.linesep, "\r\n"))
		fp.close()

def genera_fotos():
	for i,v in enumerate(sectores):
		for cod_seg, props in sorted(segmentos.iteritems()):
			if props[i+1] == 0:
				continue
			ruta_foto = fotos_entradas[(u"%02d" % (i+1), cod_seg)]
			foto_evento = Image.open(ruta_foto)
			for n in range(props[i+1]):
				codigo_completo = "%04d%s%02d" % (n+1, cod_seg, i+1)
				Buf.append(agrega_entrada2(codigo_completo, v, foto_evento, props[0]))
				if len(Buf) == 10:
					flush_buf()
	if len(Buf) > 0:
		flush_buf()

def hex_a_tupla(h):
	assert(h[0] == "#")
	r = int(h[1:3], 16)
	g = int(h[3:5], 16)
	b = int(h[5:7], 16)
	return (r,g,b,255)

def inicializar_variables(jsondata):
	global pagina, SERIE
	pagina = 1
	SERIE = 1
	import glob
	pdfs = glob.glob(os.path.join("pdfs_prueba", "*.pdf"))
	for arch in pdfs:
		os.remove(arch)
	t_registros = json.loads(jsondata["t_registros"])
	t_sectores = json.loads(jsondata["t_sectores"])
	for i,d in enumerate(t_sectores):
		t_sectores[i]["Color"] = hex_a_tupla(d["Color"])
		print t_sectores[i]["Color"]
	t_segmentos = json.loads(jsondata["t_segmentos"])
	global segmentos, sectores, color_recuadro, fotos_entradas, descripcion
	descripcion = jsondata["descripcion"]
	segmentos = {}
	sectores = []
	color_recuadro = {}
	fotos_entradas = {}

	for i,d in enumerate(t_sectores):
		sectores.append(d["Etiqueta"])
		color_recuadro[d["Etiqueta"]] = d["Color"]
	color_recuadro[u"Galería Visita"] = (0x00, 0xB0, 0x6F, 255) # 00B06F
	for i,d in enumerate(t_segmentos):
		segmentos[d["Codigo"]] = [d["Etiqueta"]] + [0 for x in sectores]

	for i,d in enumerate(t_registros):
		indice_sector = int(d["Sector"])
		fotos_entradas[(d["Sector"], d["Segmento"])] = d["Foto"][1:]
		segmentos[d["Segmento"]][indice_sector] = int(d["Entradas"])

def vista_previa(codigo, sector, foto, segmento):
	ofoto = Image.open(foto)
	f = agrega_entrada2(codigo, sector, ofoto, segmento)
	ruta = "static/previews/" + codigo + ".jpg"
	f.save(ruta)
	return ruta
if __name__ == "__main__":
	parser = OptionParser(usage="%prog [opciones] archivo_json")
	parser.add_option("-x", "--xml", action="store_true", dest="generate_xml", default=False, help="Generar archivos XML de permisos")
	parser.add_option("-p", "--pdf", action="store_true", dest="generate_pdfs", default=False, help="Generar archivos PDF para imprimir")
	parser.add_option("-t", "--test", action="store_true", dest="test", default=False, help=u"No leer archivo y ejecutar con parámetros por defecto")
	parser.add_option("--serie", action="store", dest="serie_inicial", default=1, help=u"Serie inicial")

	(options, args) = parser.parse_args()

	if len(args) != 1 and options.test is None:
		parser.print_help()
		quit()
	if not options.test:
		jdata = json.loads(open(args[0],"r").read())
		inicializar_variables(jdata)
	else:
		global SERIE
		SERIE = int(options.serie_inicial)

	if options.generate_xml:
		genera_xml_todos()

	if options.generate_pdfs:
		genera_fotos()

