# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw
import Code128b
foto = {}
cort = {}

foto["galeria"]     = Image.open("images/GALERIA.png")
foto["preferencial"] = Image.open("images/PREFERENCIAL.png")
foto["andes"]        = Image.open("images/ANDES.png")

cort["galeria"] = Image.open("images/GALERIA CORTESIA.png")
cort["preferencial"] = Image.open("images/PREFERENCIAL CORTESIA.png")
cort["andes"] = Image.open("images/ANDES CORTESIA.png")


pagina = 1
Buf = []

SERIE = 1

fuente = ImageFont.truetype("arial.ttf",35)
fuente_chica = ImageFont.truetype("arial.ttf", 26)
fuente_serie = ImageFont.truetype("arial.ttf", 20)


ancho_foto_texto = 700






rangos = {}
"""
rangos["preferencial"] = {
	"Dirigente Butacas":	[26,  "0101", u"Preferencial"],
	"Jugador y CT Butacas": [90,  "0201", u"Preferencial"],
	"Auspiciadores":[28,  "0301", u"Preferencial"],
	"Medios Prensa":[16,  "0401", u"Preferencial"],
	"Funcionarios": [3,  "0501", u"Preferencial"],
	"Compromisos":  [30,  "0601", u"Preferencial"],
	"Compromisos Butacas" : [77, "0601", "Preferencial"],
	#"Homecenter":   [100, "0705", u"Butacas"],
	#"Caja 18":      [50,  "0805", u"Butacas"],
	#"UVM":			[100, "0905", u"Butacas"],
	#"Municipalidad":[360, "1005", u"Butacas"]
	"-": 			[200, "1101", "Preferencial"]
}
rangos["andes"] = {
	#"Dirigente":	[26,  "0105", u"Butacas"],
	"Jugador y CT": [50,  "0203", u"Andes"],
	"Auspiciadores":[57,  "0303", u"Andes"],
	"Medios Prensa":[27,  "0403", u"Andes"],
	"Funcionarios": [18,  "0503", u"Andes"],
	"Compromisos":  [20,  "0603", u"Andes"],
	#"Homecenter":   [100, "0705", u"Butacas"],
	#"Caja 18":      [50,  "0805", u"Butacas"],
	"UVM":			[100, "0903", u"Andes"],
	#"Municipalidad":[360, "1005", u"Butacas"]
	"-": 			[400, "1303", u"Andes"]
}
rangos["galeria"] = {
	"Dirigente":	[34,  "0102", u"Galería"],
	"Jugador y CT": [20,  "0202", u"Galería"],
	"Auspiciadores":[5,  "0302", u"Galería"],
	"Medios Prensa":[14,  "0402", u"Galería"],
	#"Funcionarios": [18,  "0503", u"Andes"],
	"Compromisos":  [17,  "0602", u"Galería"],
	"Homecenter":   [100, "0702", u"Galería"],
	"Caja 18":      [50,  "0802", u"Galería"],
	#"UVM":			[100, "0905", u"Butacas"],
	"Municipalidad":[360, "1002", u"Galería"],
	"Iquique":		[300, "1502", u"Galería"],
	"-": 			[1500, "1302", u"Galería"]
}
"""
rangos["galeria"] = {
	"-": [1, "1302", u"Galería"],
	u"Niño": [1, "2202", u"Galería"]
}
rangos["preferencial"] = {
	"-": [1, "1101", "Preferencial"],
	"Credencial": [1, "2101", "Preferencial"]
}
rangos["andes"] = {
	"-": [1, "1303", "Andes"],
	"Socio": [1, "2003", "Andes"]
}

def ajustar(img,**kwargs):
	w, h = img.size
	factor = 1
	if "alto" in kwargs:
		factor = kwargs["alto"] / h
		return img.resize((w * factor, h * factor))
	elif "ancho" in kwargs:
		factor = kwargs["ancho"] / w
		return img.resize((w * factor, h * factor))
	else:
		raise Exception("no argument found")



def flush_buf():
	global Buf, pagina
	print "Buffer: %d fotos" % len(Buf) 
	print "Pagina %d" % pagina
	W, H = Buf[0].size
	L = Image.new("RGBA", (W, H*10), (255,255,255,255))
	for i in range(len(Buf)):
		L.paste(Buf[i], (0, i*H))
	dpi = 600
	margen_superior = 1.1
	ancho_pag = int(dpi * (7.5))
	alto_pag = int(dpi * 10)
	Doc = Image.new("RGB", (ancho_pag, alto_pag), (255,255,255))
	L = L.rotate(-90,expand=True)
	lw, lh = L.size
	escala = 4500.0/lw
	L = L.resize((int(lw*escala), int(lh*escala)))
	Doc.paste(L, (0, int(margen_superior*dpi), L.size[0], int(margen_superior*dpi) + L.size[1]))
	Doc.save("pdfs_prueba/pagina%d.pdf" % pagina, "PDF", resolution=dpi)
	pagina = pagina +1
	Buf = []

def agrega_entrada(codigo,sector,tipo_foto,segmento=None):

	foto_codigo = Code128b.code128_image(codigo)
	w,h = foto_codigo.size
	factor = 360 / h
	foto_codigo = foto_codigo.resize((w*factor, h*factor))

	fotoTexto = Image.new("CMYK", (ancho_foto_texto, 543), (0,0,0,0))

	drawer = ImageDraw.Draw(fotoTexto)
	alto_linea = 60

	drawer.text((alto_linea,50), sector, font=fuente)

	alto_linea += fuente.getsize("A")[1]*1.1

	if segmento != None:
		drawer.text((50,alto_linea), segmento, font=fuente)
		alto_linea += fuente.getsize("A")[1]*1.1
	if tipo_foto == "cortesia":
		drawer.text((50,alto_linea), u"Entrada de cortesía", font=fuente_chica)


	ancho_total = foto[tipo_foto].size[0] + foto_codigo.size[0] + ancho_foto_texto


	lienzo = Image.new("CMYK", (ancho_total, 543), (0,0,0,0))

	altura_codigo = (543 - 360) / 2
	width_seek = 0
	lienzo.paste(foto_codigo, (width_seek,altura_codigo, width_seek + foto_codigo.size[0], altura_codigo + foto_codigo.size[1]))
	width_seek = width_seek + foto_codigo.size[0]
	lienzo.paste(fotoTexto, (width_seek, 0, width_seek + fotoTexto.size[0], fotoTexto.size[1]))
	width_seek = width_seek + fotoTexto.size[0]
	lienzo.paste(foto[tipo_foto], (width_seek, 0, width_seek + foto[tipo_foto].size[0], foto[tipo_foto].size[1]))


	if len(Buf) == 10:
		flush_buf()
	achique = 1

	Buf.append(lienzo.resize((int(lienzo.size[0]*achique), int(lienzo.size[1]*achique))))

def agrega_entrada2(codigo, sector, tipo_foto, segmento):
	
	imagen_ref = None
	if segmento not in ["-", "Iquique"]:
		imagen_ref = cort[tipo_foto]
	else:
		imagen_ref = foto[tipo_foto]

	alto_total = imagen_ref.size[1]

	foto_codigo = Code128b.code128_image(codigo)
	
	foto_codigo = ajustar(foto_codigo, alto=alto_total)

	ancho_total = imagen_ref.size[0] + foto_codigo.size[0]

	lienzo = Image.new("RGBA", (ancho_total, alto_total), (255,255,255,255))

	lienzo.paste(foto_codigo, (0, 24))
	lienzo.paste(imagen_ref, (foto_codigo.size[0], 0))

	# agregar texto

	drawer = ImageDraw.Draw(lienzo)

	margen_lat = int((363 - fuente.getsize(sector.upper())[0])/2)
	margen_sup = 24 + 5

	drawer.text((foto_codigo.size[0] + margen_lat, margen_sup), sector.upper(), font=fuente)

	if segmento != "-":
		margen_sup = margen_sup + 50
		margen_lat = int((363 - fuente_chica.getsize(segmento.upper())[0]) / 2)

		drawer.text((foto_codigo.size[0] + margen_lat, margen_sup), segmento.upper(), font=fuente_chica)

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

	if len(Buf) == 10:
		flush_buf()
	achique = 1

	Buf.append(lienzo.resize((int(lienzo.size[0]*achique), int(lienzo.size[1]*achique))))


for tipo_foto, segmentos in rangos.iteritems():
	for titulo, datos in segmentos.iteritems():
		cantidad = datos[0]
		sufijo = datos[1]
		sector = datos[2]
		for n in range(cantidad):
			codigo_completo = "%03d%s" % (n+1, sufijo)
			agrega_entrada2(codigo_completo,sector,tipo_foto,titulo)


if len(Buf) > 0:
	flush_buf()