#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTANTE: ejecutar el script desde el dir donde este el archivo a importar y solo hay que escrbir el nombre.csv

####################################################################################
# CARGAMOS LAS LIBRERIAS A UTLITZAR:
####################################################################################

import itertools
import seaborn as sns
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv
from sys import argv

'''

DATOS USADOS :
 'Producto interior bruto a precios de mercado',
 'Gasto en consumo final',
 'Gasto en consumo final de los hogares',
 'Gasto en consumo final interior de los hogares',
 'Formacion bruta de capital',
 'Formacion bruta de capital fijo',
 'FBCF. Activos fijos materiales',
 'FBCF. Activos fijos materiales. Construccion',
 'FBCF. Activos fijos materiales. Bienes de equipo',
 'FBCF. Activos fijos materiales.Recursos biologicos',
 'FBCF. Productos de la propiedad intelectual',
 'Exportaciones de bienes y servicios',
 'Importaciones de bienes y servicios',

'''

##########################################################################################################
# FORMATO PRESENTACION DEL SCRIPT
##########################################################################################################

form1 = "------------------------------------------------------------------------"
form = "#########################################################################"
lin = "\n"
diss = "\tAnalisis de CNT: Por @mmngreco."
diss1 = "Necesita saber: \n\t\a- El numero variables (sin contar el tiempo) \n\t\a- Nombre del archivo con extension .csv"
diss2 = "\n(!) Es importante que el archivo con datos este en el mismo directorio que este script."

print ""
print form + lin + diss + lin + form
print lin
print form1 + lin + diss1 + lin + diss2 + lin + form1
print lin

x = int(raw_input("> Numero de variables: "))
f = raw_input("> Nombre del archivo: ")
var = x + 1 # cantidad de variables + time (etiquetas temporales)

reader = csv.reader(open(f, "rb"), delimiter=";") # DECLARAMOS PARAMETROS DE LECTURA DEL ARCHIVO
data = [] # AGREGAMOS LOS DATOS EN LA MEMORIA PARA USARLOS:

for fila in reader:
	data.append(fila)

# CONVERTIMOS LA LISTA DE LISTAS EN UNA LISTA UNIFICADA:

merged = list(itertools.chain(*data)) # junta todos los elementos en la misma lista
# matrix = np.matrix(data) # interesante para operar con todos los datos

##########################################################################################################
# TABULACION DE LOS DATOS
##########################################################################################################

# -------------------------------------------------------------------------------------------------------------
# Estructura del INE, los primeros datos son informacion de la serie y luego los nombres de las variables:
# -------------------------------------------------------------------------------------------------------------

# limpiamos la serie para poder transformala en una matriz y operar con ella.

inutil = 4 # numero de posiciones que contiene info y eliminamos de los datos
info = []

for i in range(inutil -1, -1, -1):
	info.append(merged.pop(i)) # desde la posicion 0 a 4 (5 - 1) incluida

del merged[x] # Elimina la frase: "Dato Base"


# Eliminamos los espacios vacios

for i in range(len(merged) - 1, -1, -1):
	if merged[i] == "":
		del merged[i]
	else:
		pass

merged.insert(0, "Time") # agregamos nombre para la variable año y trimestre
el = len(merged) / var # cantidad de elementos menos el nombre de la columna# cantidad de datos 

print lin, form1, lin,"Resumen:", lin, form1
print "> Hay %s variables incluyendo time" % float(var)
print "> Hay %s elementos en cada variable, incluyendo los nombres de las variables" % float(el)
print form1

##########################################################################################################
# TRANSFORMAMOS UNA LISTA EN UNA MATRIZ
##########################################################################################################

m = [] # array esta variable sera una lista de listas que contendrá todas las variables
buff = [] # buffer para almacenar la lista y añadirla a nuestro array m

for v in range(var): # agrupar los elementos de una misma variable en una lista
	for e in range(v, len(merged), var):
		buff.append(merged[e])
	

	m.append(buff) # agrega la lista de elementos de una variable como una lista en una lista.
	buff = []

# print lin, form1, "m[0]", m[0],form1, lin

# -------------------------------------------------------------------------------------------------------------
# MOVER LOS NOMBRES DE LAS VARIABLES A NAMES
# -------------------------------------------------------------------------------------------------------------

names = [] # nombres de las variables

for v in range(var):
	names.append(m[v][0])
	del m[v][0]

# -------------------------------------------------------------------------------------------------------------
# PRESENTAR LOS NOMBRES DE LAS VARIABLES
# -------------------------------------------------------------------------------------------------------------


print lin
print form1
print "Los datos: "
for i in range(len(names)):
	print "m[%s] = names[%s] =%s" % (i, i, names[i])
print form1
print lin

# -------------------------------------------------------------------------------------------------------------
# eliminar el punto de los miles y convertir en numeros:
# -------------------------------------------------------------------------------------------------------------

for v in range(1, var): # para cada 'v'ariable (columnas) menos time (1)
	for e in range(el - 1): # para cada 'e'lemento (filas) 
		m[v][e] = float(m[v][e].replace(".", "")) # convierte en numero y eliminan los puntos de miles

m_qq = [] # incremento intercuatilico
m_yy = [] # incremento anual
m_qq2 = [] # intensidad del incremento q-q
m_yy2 = [] # intensidad del incremento y-y

# -------------------------------------------------------------------------------------------------------------
# CALCULOS
# -------------------------------------------------------------------------------------------------------------
# calculo de incrementos y-y y q-q
m_yy.append(m[0][4:])
m_qq.append(m[0][1:])
m_yy2.append(m[0][8:])
m_qq2.append(m[0][2:])

for v in range(1, var):
	for e in range(el - 4 - 1): # - 4 ( y-y ~> 4 trimestres ) - 1 (fila del nombre que quitamos)
		buff.append((m[v][e + 4] / m[v][e]) - 1) # calcula el incremento porcentual y-y
	
	m_yy.append(buff) # lo guarda
	buff = []
	
	for e in range(el - 1 - 1):
		buff.append(m[v][e + 1] / m[v][e] - 1)
	
	m_qq.append(buff)
	buff = []

for v in range(1, var):

	for e in range(len(m_yy[1]) - 4):
		try:
			buff.append((m_yy[v][e + 4] / m_qq[v][e]) - 1)
		except ZeroDivisionError:
			buff.append(0)
	
	m_yy2.append(buff)
	buff = []
	
	for e in range(len(m_qq[0]) - 1):
		try:
			buff.append((m_qq[v][e + 1] / m_qq[v][e]) - 1)
		except ZeroDivisionError:
			buff.append(0)
	
	m_qq2.append(buff)
	buff = []


# -------------------------------------------------------------------------------------------------------------
# GRAFICOS
# -------------------------------------------------------------------------------------------------------------

plt.figure("Grafico 2", figsize=(12,8))
plt.suptitle(names[1])
plt.plot(m[1])

plt.show()



def grf_var():
	
	dib = [1,4,5,9]
	plt.figure("Variaciones", figsize=(14,8))
	
	for i in range(1, len(dib) + 1):

		plt.subplot(2,2,i)
		plt.plot(m_yy[dib[i-1]], label=names[dib[i-1]])
		plt.legend()

	plt.show()
grf_var()
