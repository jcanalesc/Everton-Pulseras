# -*- coding: utf-8 -*-
import glob
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
import xlwt

tipo = sys.argv[1]

files = glob.glob("registros_%s*.xml" % tipo)

mapper = ET.parse("permisos.xml")
r = mapper.getroot()

cantidad_rep = {}
segmentos = {}
for child in r:
	if child[1].text == tipo.capitalize() and child[4].text not in [u"Niño", "Socio", "Credencial"]:
		segmentos[child[3].text] = child[4].text
		cantidad_rep[child[3].text] = int(child[5].text)

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Informe")

sheet.write(0,0, "Codigo")
sheet.write(0,1, "Sector")
sheet.write(0,2, "Segmento")
sheet.write(0,3, "Fecha/Hora")


fila = 1
for f in files:
	print "Procesando archivo %s" % f
	tree = ET.parse(f)
	root = tree.getroot()
	for ch in root:
		codigo = ch[1].text
		if codigo == None or len(codigo) < 4:
			continue
		seg = codigo[-4:-2]
		sec = codigo[-2:]
		if seg not in segmentos:
			continue
		hora = ch[2].text
		#output.write("%s;%s;%s;%s\n" % (codigo, sectores[sec], segmentos[seg], hora))
		sheet.write(fila, 0, codigo)
		sheet.write(fila, 1, tipo.capitalize())
		sheet.write(fila, 2, segmentos[seg])
		sheet.write(fila, 3, datetime.strptime(hora, "%Y-%m-%d %H:%M:%S"), xlwt.easyxf("", "YYYY/MM/DD HH:MM:SS AM/PM"))
		fila += 1

# formulas

sheet.write(0, 6, "Cantidad")
sheet.write(0, 7, "% del total")

fila2 = 1
for i in segmentos:
	sheet.write(fila2, 5, segmentos[i])
	sheet.write(fila2, 6, xlwt.Formula("COUNTIF($C$2:$C$%d,F%d)" % (fila-1, fila2 + 1)))
	sheet.write(fila2, 7, xlwt.Formula("G%d/$G$%d" % (fila2+1, len(segmentos)+2)), xlwt.easyxf("", "0.00%"))
	fila2 += 1

sheet.write(fila2, 5, "Total")
sheet.write(fila2, 6, xlwt.Formula("SUM(G2:G%d)" % fila2))
sheet.write(fila2, 7, xlwt.Formula("G%d/$G$%d" % (fila2+1, len(segmentos)+2)), xlwt.easyxf("", "0.00%"))

fila2 += 2

sheet.write(fila2, 6, "Cantidad registrada")
sheet.write(fila2, 7, "Cantidad Repartida")
sheet.write(fila2, 8, "%")

fila2 += 1

for i in segmentos:
	sheet.write(fila2, 5, segmentos[i])
	sheet.write(fila2, 6, xlwt.Formula("COUNTIF($C$2:$C$%d,F%d)" % (fila-1, fila2 + 1)))
	sheet.write(fila2, 7, cantidad_rep[i])
	sheet.write(fila2, 8, xlwt.Formula("G%d/H%d" % (fila2+1, fila2+1)), xlwt.easyxf("", "0.00%"))
	fila2 += 1

sheet.write(fila2, 5, "Total")
sheet.write(fila2, 6, xlwt.Formula("SUM(G%d:G%d)" % (len(segmentos)+5, 2*len(segmentos)+4)))
sheet.write(fila2, 7, xlwt.Formula("SUM(H%d:H%d)" % (len(segmentos)+5, 2*len(segmentos)+4)))
sheet.write(fila2, 8, xlwt.Formula("G%d/H%d" % (fila2+1, fila2+1)), xlwt.easyxf("", "0.00%"))

workbook.save("informe_%s.xls" % tipo)