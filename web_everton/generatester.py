# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw
import Code128b
import xml.etree.ElementTree as ET
import sys
import random

def ajustar(img,**kwargs):
	w, h = img.size
	factor = 1
	if "alto" in kwargs:
		factor = kwargs["alto"] / float(h) * 1.0
		#print factor
		c = img.copy()
		c.thumbnail(((int(w * factor), int(h * factor))), Image.ANTIALIAS)
		return c
	elif "ancho" in kwargs:
		factor = kwargs["ancho"] / float(w) * 1.0
		#print factor
		c = img.copy()
		c.thumbnail(((int(w * factor), int(h * factor))), Image.ANTIALIAS)
		return c
	else:
		raise Exception("no argument found")

codes = {}

if __name__ == "__main__":
	if len(sys.argv) != 2:
		quit()
	archivo = sys.argv[1]
	root = ET.parse(archivo).getroot()
	for localidad in root.findall('localidad'):
		cod_seg = localidad.find("idUsr").text
		cod_loc = localidad.find("codLoc").text
		maximo = int(localidad.find("entradas").text)
		nombre_sec = localidad.find("nombreLoc").text
		nombre_seg = localidad.find("nombreUsr").text

		numero = random.randint(1,int(maximo*1.4))
		codigo = "%04d%s%s" % (numero, cod_seg, cod_loc)

		codes[(cod_seg, cod_loc)] = {
			"img": Code128b.code128_image(codigo, 50),
			"label": "%s/%s" % (nombre_sec, nombre_seg),
			"code": "%s (max: %d)" % (codigo, maximo),
			"valid": True if numero <= maximo else False
		}
	print "Cantidad de localidades: %d" % (len(codes))
	posx = 0
	posy = 0
	dpi = 100
	ancho_carta_p = 8.5
	alto_carta_p = 11
	ancho_carta = int(ancho_carta_p * dpi)
	alto_carta = int(alto_carta_p * dpi)
	lienzo = Image.new("RGB", (ancho_carta, alto_carta), (255, 255, 255))
	ancho_casilla = int(ancho_carta / 4)
	alto_casilla = int(alto_carta / 10)
	fuente = ImageFont.truetype("arial.ttf", int(alto_casilla / 7))

	img_good = ajustar(Image.open("checkbox_good.png"), alto=int(alto_casilla / 7))
	img_bad = ajustar(Image.open("checkbox_bad.png"), alto=int(alto_casilla / 7))

	pagina = 1

	for k, v in codes.iteritems():
		drawer = ImageDraw.Draw(lienzo)
		lineas = v["label"].split("/")
		drawer.text((posx, posy), lineas[0], font=fuente, fill=(0,0,0))
		drawer.text((posx, posy+int(alto_casilla/7 + 4)), lineas[1], font=fuente, fill=(0,0,0))
		drawer.text((posx, posy+int(alto_casilla/7 + 4)*2), v["code"], font=fuente, fill=(0,0,0))
		lienzo.paste(img_good if v["valid"] else img_bad, (posx + fuente.getsize(v["code"])[0] + 2, posy+int(alto_casilla/7 + 4)*2))
		lienzo.paste(ajustar(v["img"], ancho=(ancho_casilla*0.9)), (posx, posy+int(alto_casilla/7 + 4)*3 + 4))

		posx += ancho_casilla
		if (posx+ancho_casilla) >= ancho_carta:
			posx = 0
			posy += alto_casilla
		if (posy+alto_casilla) >= alto_carta:
			posx = 0
			posy = 0
			lienzo.save("tester_%d.pdf" % pagina, "PDF", resolution=dpi)
			pagina += 1
			lienzo = Image.new("RGB", (ancho_carta, alto_carta), (255, 255, 255))

	if len(codes) % 10 != 0:
		lienzo.save("tester_%d.pdf" % pagina, "PDF", resolution=dpi)


		







