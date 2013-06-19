# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import Code128b

dpi = 300

ancho_pag = 5.5
alto_pag = 6.5

ancho_logo = 1.5

ancho_codigo = 2.0

salto_codigos = 1.8

alto_letra = 0.4


def ajustar(img,**kwargs):
	w, h = img.size
	factor = 1
	if "alto" in kwargs:
		factor = kwargs["alto"] / h
		return img.resize((int(w * factor), int(h * factor)))
	elif "ancho" in kwargs:
		factor = kwargs["ancho"] / w
		return img.resize((int(w * factor), int(h * factor)))
	else:
		raise Exception("no argument found")

codigo_nino  = ajustar(Code128b.code128_image("0019701"), ancho=ancho_codigo*dpi)
codigo_socio = ajustar(Code128b.code128_image("0019801"), ancho=ancho_codigo*dpi)
codigo_cred  = ajustar(Code128b.code128_image("0019901"), ancho=ancho_codigo*dpi)

logo = ajustar(Image.open("logo.jpg"),ancho=ancho_logo*dpi )

lienzo = Image.new("RGB", (int(ancho_pag * dpi), int(alto_pag * dpi)), (255,255,255))

lienzo.paste(logo, (lienzo.size[0] - logo.size[0], 0))

fuente = ImageFont.truetype("arial.ttf", int(alto_letra * dpi))

drawer = ImageDraw.Draw(lienzo)

margen_izq = int((ancho_pag*dpi - fuente.getsize(u"Niño")[0]) / 2)
margen_sup = int(0.2 * dpi)

drawer.text((margen_izq, margen_sup), u"Niño", font=fuente, fill=(0,0,0))

margen_izq = int((ancho_pag*dpi - codigo_nino.size[0]) / 2)

lienzo.paste(codigo_nino, (margen_izq, margen_sup + int((alto_letra + 0.1) * dpi)))

margen_sup += int(salto_codigos * dpi)

margen_izq = int((ancho_pag*dpi - fuente.getsize(u"Socio")[0]) / 2)

drawer.text((margen_izq, margen_sup), u"Socio", font=fuente, fill=(0,0,0))

margen_izq = int((ancho_pag*dpi - codigo_socio.size[0]) / 2)

lienzo.paste(codigo_socio, (margen_izq, margen_sup + int((alto_letra + 0.1) * dpi)))

margen_sup += int(salto_codigos * dpi)

margen_izq = int((ancho_pag*dpi - fuente.getsize(u"Credencial")[0]) / 2)

drawer.text((margen_izq, margen_sup), u"Credencial", font=fuente, fill=(0,0,0))

margen_izq = int((ancho_pag*dpi - codigo_cred.size[0]) / 2)

lienzo.paste(codigo_cred, (margen_izq, margen_sup + int((alto_letra + 0.1) * dpi)))

lienzo.save("codigos_especiales.pdf", "PDF", resolution=dpi)

