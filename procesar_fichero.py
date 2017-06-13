# -*- coding: utf-8 -*-

## Autores: Andrés Manrique y Fernando Gualo

import csv
import datetime
from xml.dom import minidom

N_LINES = 500

# Consultamos el precio de la luz para un tramo horario dado, a partir de un fichero extraído de una de las referencias.
doc = minidom.parse("../Datos/perfilconsumo.xml")   
periods = doc.getElementsByTagName("Periodo")
def calcularPrecio(date_filter, hour_filter):
    for period in periods:
        interval = period.getElementsByTagName("IntervaloTiempo")[0]
        aux = interval.getAttribute("v").split("T")
        date = datetime.datetime.strptime(aux[0], "%Y-%m-%d")
        hours = period.getElementsByTagName("Intervalo")
        for hour in hours:
            if date_filter == date:
                pos = hour.getElementsByTagName("Pos")[0].getAttribute("v")
                ctd = hour.getElementsByTagName("Ctd")[0].getAttribute("v")
                if pos == hour_filter:
                    return float(ctd)

def cleanList(list_to_clean):
	for attr in list_to_clean:
		if(row[attr] == ''):
			row[attr] = 0
	return list_to_clean

# Procesamos el fichero, agregamos datos, y creamos uno nuevo.
with open('../Datos/DATATHON_secuencial.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='|')

    with open ('../Datos/DATATHON_2015_Processed.csv', 'w') as newcsv:
        fieldnames = ['Dia', 'Dia_Activa', 'Dia_Reactiva', 'Gasto_Dia', 'Noche_Activa', 'Noche_Reactiva', 'Gasto_Noche', 'Gasto_total', 'Municipio','FechaAlta','Target_Tenencia_Cups','Identificador','CNAE','Producto','Mercado']
        writer = csv.DictWriter(newcsv, fieldnames=fieldnames)
        writer.writeheader()
        i = 0

        for row in reader:
			date = datetime.datetime.strptime(row['DIA'], "%Y%m%d")
			date_filter = datetime.datetime(2015,10,01)
			if date > date_filter:
				i += 1
				if i == N_LINES:
					break

				print(i)

                #DIA 8.00 - 21.00
				
				active_to_clean = ['ACTIVA_H1', 'ACTIVA_H2', 'ACTIVA_H3', 'ACTIVA_H4', 'ACTIVA_H5', 'ACTIVA_H6', 'ACTIVA_H7', 'ACTIVA_H8', 'ACTIVA_H9', 'ACTIVA_H10', 'ACTIVA_H11', 'ACTIVA_H12', 'ACTIVA_H13', 'ACTIVA_H14', 'ACTIVA_H15', 'ACTIVA_H16', 'ACTIVA_H17', 'ACTIVA_H18', 'ACTIVA_H19', 'ACTIVA_H20', 'ACTIVA_H21', 'ACTIVA_H22', 'ACTIVA_H23', 'ACTIVA_H24', 'ACTIVA_H25']
				reactive_to_clean = ['REACTIVA_H1', 'REACTIVA_H2', 'REACTIVA_H3', 'REACTIVA_H4', 'REACTIVA_H5', 'REACTIVA_H6', 'REACTIVA_H7', 'REACTIVA_H8', 'REACTIVA_H9', 'REACTIVA_H10', 'REACTIVA_H11', 'REACTIVA_H12', 'REACTIVA_H13', 'REACTIVA_H14', 'REACTIVA_H15', 'REACTIVA_H16', 'REACTIVA_H17', 'REACTIVA_H18', 'REACTIVA_H19', 'REACTIVA_H20', 'REACTIVA_H21', 'REACTIVA_H22', 'REACTIVA_H23', 'REACTIVA_H24', 'REACTIVA_H25']
				others = ['TARGET_TENENCIA_CUPS']

				active_to_clean = cleanList(active_to_clean)
				reactive_to_clean = cleanList(reactive_to_clean)
				others = cleanList(others)

				if row['MERCADO'] == 'M1':
					row['MERCADO'] = 1
				else:
					row['MERCADO'] = 2

				row["CNAE"] = row["CNAE"].replace("T", "")
				row["PRODUCTO"] = row["PRODUCTO"].replace("P", "")

				day_act = int(row['ACTIVA_H8'])  + int(row['ACTIVA_H9']) + int(row['ACTIVA_H10']) + int(row['ACTIVA_H11']) + int(row['ACTIVA_H12']) + int(row['ACTIVA_H13']) + int(row['ACTIVA_H14']) + int(row['ACTIVA_H15']) + int(row['ACTIVA_H16']) + int(row['ACTIVA_H17']) + int(row['ACTIVA_H18']) + int(row['ACTIVA_H19']) + int(row['ACTIVA_H20']) + int(row['ACTIVA_H21'])
				day_ract = int(row['REACTIVA_H8']) + int(row['REACTIVA_H9']) + int(row['REACTIVA_H10']) + int(row['REACTIVA_H11']) + int(row['REACTIVA_H12']) + int(row['REACTIVA_H13']) + int(row['REACTIVA_H14']) + int(row['REACTIVA_H15']) + int(row['REACTIVA_H16']) + int(row['REACTIVA_H17']) + int(row['REACTIVA_H18']) + int(row['REACTIVA_H19']) + int(row['REACTIVA_H20']) + int(row['REACTIVA_H21'])
                
				night_act = int(row['ACTIVA_H22']) + int(row['ACTIVA_H23']) + int(row['ACTIVA_H24']) + int(row['ACTIVA_H25']) + int(row['ACTIVA_H1']) + int(row['ACTIVA_H2']) + int(row['ACTIVA_H3']) + int(row['ACTIVA_H4'])  + int(row['ACTIVA_H5']) + int(row['ACTIVA_H6']) + int(row['ACTIVA_H7']) 
				night_ract = int(row['REACTIVA_H22']) + int(row['REACTIVA_H23']) + int(row['REACTIVA_H24']) + int(row['REACTIVA_H25']) + int(row['REACTIVA_H1']) + int(row['REACTIVA_H2']) + int(row['REACTIVA_H3']) + int(row['REACTIVA_H4']) + int(row['REACTIVA_H5']) + int(row['REACTIVA_H6']) + int(row['REACTIVA_H7'])
                
				gasto_dia = 0
				gasto_dia = (int(row['ACTIVA_H8']) * calcularPrecio(date_filter,"8")) + (int(row['ACTIVA_H9']) * calcularPrecio(date_filter,"9")) + (int(row['ACTIVA_H10']) * calcularPrecio(date_filter,"10")) + (int(row['ACTIVA_H11']) * calcularPrecio(date_filter,"11")) + (int(row['ACTIVA_H12']) *calcularPrecio(date_filter,"12")) + (int(row['ACTIVA_H13']) * calcularPrecio(date_filter,"13")) + (int(row['ACTIVA_H14']) * calcularPrecio(date_filter,"14")) + (int(row['ACTIVA_H15']) * calcularPrecio(date_filter,"15")) + (int(row['ACTIVA_H16']) * calcularPrecio(date_filter,"16")) + (int(row['ACTIVA_H17']) * calcularPrecio(date_filter,"17")) + (int(row['ACTIVA_H18']) *calcularPrecio(date_filter,"18")) + (int(row['ACTIVA_H19']) *calcularPrecio(date_filter,"19")) + (int(row['ACTIVA_H20']) *calcularPrecio(date_filter,"20"))+(int(row['ACTIVA_H21']) *calcularPrecio(date_filter,"21"))
                
				gasto_noche = 0
				gasto_noche = (int(row['ACTIVA_H22'])*calcularPrecio(date_filter,"22")) + (int(row['ACTIVA_H23'])*calcularPrecio(date_filter,"23")) + (int(row['ACTIVA_H24'])*calcularPrecio(date_filter,"24")) + (int(row['ACTIVA_H25'])*calcularPrecio(date_filter,"24")) + (int(row['ACTIVA_H1'])*calcularPrecio(date_filter,"1")) + (int(row['ACTIVA_H2'])*calcularPrecio(date_filter,"2")) + (int(row['ACTIVA_H3'])*calcularPrecio(date_filter,"3")) + (int(row['ACTIVA_H4'])*calcularPrecio(date_filter,"4")) + (int(row['ACTIVA_H5'])*calcularPrecio(date_filter,"5")) + (int(row['ACTIVA_H6'])*calcularPrecio(date_filter,"6")) + (int(row['ACTIVA_H7'])*calcularPrecio(date_filter,"7"))   
				
				gasto_total = float(gasto_dia + gasto_noche)

				writer.writerow({'Dia': row['DIA'],'Dia_Activa': day_act,'Dia_Reactiva': day_ract,'Gasto_Dia': gasto_dia,'Noche_Activa': night_act,'Noche_Reactiva': night_ract,'Gasto_Noche':gasto_noche, 'Gasto_total': gasto_total, 'Municipio': row['DE_MUNICIP'],'FechaAlta': row['FECHA_ALTA_STRO'],'Target_Tenencia_Cups': row['TARGET_TENENCIA_CUPS'],'Identificador':row['IDENTIFICADOR'],'CNAE': row['CNAE'],'Producto': row['PRODUCTO'], 'Mercado': row['MERCADO'] })