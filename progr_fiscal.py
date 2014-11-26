#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------------
# CARGAR LIBRERIAS
# ---------------------------------------------------------------------------------

import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import seaborn as sns

# ESTO INCRUSTA LOS GRAFICOS EN LA MISMA PAGINA
# %matplotlib inline 


####################################################################################
####                          DATOS ACTUALES DE IRPF                         #######
####################################################################################

base_actual = [0, 17707.20, 33007.20, 53407.20, 120000.00, 175000.00, 300000.00]
cuota_actual = [0, 4382.53, 8972.53, 17132.53, 48431.15, 75381.15, 139131.15]
t_actual = [0.2475, 0.3000, 0.4000, 0.470, 0.490, 0.510, 0.520]

####################################################################################
#########                     DATOS REFORMA DE 2015:                        ########
####################################################################################

t_estatal = [.10, .125, .155, .195, .235]
t_aragon = [.10, .125, .1550, .19, .215]

t_2015 = [t_estatal[i] + t_aragon[i] for i in range(5)]
base_2015 = [0, 12450.00, 20200.00, 34000.00, 60000.00]
cuota_2015 = [0, 2490, 4427.5, 8705.5, 18715.5]

####################################################################################
################                INCOGNITAS:                         ################
####################################################################################


base_sim = range(5000, 400000, 1000) 
# calculamos una serie de bases liquidas para simular el comportamiento. Agregar # al principio de la linea para activar la siguiente.
# base_sim = range(raw_input("inicio: "),raw_input("fin: "), raw_input("incremento: ")) # eliminar el primer # para controlar la simulacion

t_me_actual = []
t_mg_actual = []
ci_actual = []

ci_2015 = []
t_me_2015 = []
t_mg_2015 = []

####################################################################################
#####         CALCULO DE CUOTA, TIPOS MARGINALES Y MEDIO DEL ACTUAL IRPF:     ######
####################################################################################

'''
Para hallar las incognitas creo dos variables comp_actual e ind_actual,
el primero lo que hace es comparar la lista de las bases de cada tramo con la base
simulada y crea una lista que devuelve TRUE o FALSE para cada tramo, para saber
que indice es y poder aplicar los tipos y cuotas del tramo correspondiente aplicamos
ind_actual que busca el primer TRUE de y devuelve el indice al que corresponde el tramo.
'''

comp_actual = [[base_sim[i] <= base_actual[ii] for ii in range(len(base_actual))] for i in range(len(base_sim))]
ind_actual = []

for i in range(len(base_sim)):
	if True in comp_actual[i]:
	
		ind_actual.append(comp_actual[i].index(True) - 1)
	else: 
		ind_actual.append(len(base_actual) - 1)

for i in range(len(base_sim)):

	ci_actual.append(cuota_actual[ind_actual[i]] + (base_sim[i] - base_actual[ind_actual[i]]) * t_actual[ind_actual[i]])
	t_mg_actual.append(t_actual[ind_actual[i]])
	t_me_actual.append(ci_actual[i] / base_sim[i])

####################################################################################
#        CALCULOS CUOTAS, TIPO MARGINAL Y TIPO MEDIO TRAS LA REFORMA 2015          #
####################################################################################

comp_2015 = [[base_sim[i] <= base_2015[ii] for ii in range(len(base_2015))] for i in range(len(base_sim))]
ind_2015 = []
for i in range(len(base_sim)):
	if True in comp_2015[i]:
	
		ind_2015.append(comp_2015[i].index(True) - 1)
	else: 
		ind_2015.append(len(base_2015) - 1)

for i in range(len(base_sim)):
	ci_2015.append(cuota_2015[ind_2015[i]] + (base_sim[i] - base_2015[ind_2015[i]]) * t_2015[ind_2015[i]])
	t_mg_2015.append(t_2015[ind_2015[i]])
	t_me_2015.append(ci_2015[i] / base_sim[i])


####################################################################################
######                  PRESENTACION DE DATOS VISUALES                     #########
####################################################################################


# ---------------------------------------------------------------------------------
# VISUALIZAR CALCULOS IRPF ACTUAL:
# ---------------------------------------------------------------------------------
def ver_calculos_ac():

	tac = "CALCULOS IRPF ACTUAL PARA ARAGON"
	print tac
	print "=" * len(tac)
	print "BASE\tCUOTA\tt\'\tt*"
	print "-" * len(tac)
	for i in range(len(base_sim)):
	    print "%s\t%s\t%s\t%s" % (base_sim[i], ci_actual[i], t_mg_actual[i], t_me_actual[i])
	print ""

ver_calculos_ac()
# ---------------------------------------------------------------------------------
# VISUALIZAR DATOS REFORMA 2015
# ---------------------------------------------------------------------------------
def ver_datos_ac():

	print "   DATOS IRPF ACTUAL PARA ARAGON"
	print "=" * 40
	print "base\t\tcuota\t\tt_total"
	print "-" * 40
	for i in range(len(base_actual)):
	    print "%s\t\t%s\t\t%s" % (base_actual[i], cuota_actual[i], t_actual[i])
	print ""

ver_datos_ac()

# ---------------------------------------------------------------------------------
# VISUALIZAR DATOS REFORMA 2015
# ---------------------------------------------------------------------------------
def ver_datos_2015():

	print "DATOS IRPF 2015 PARA ARAGON"
	print "=" * len("DATOS IRPF EN 2015 PARA ARAGON")
	print "BASE\tCUOTA\tGRAVAMEN"
	print "-" * len("DATOS IRPF EN 2015 PARA ARAGON")
	for i in range(len(base_2015)):
	    print "%s\t%s\t%s" % (base_2015[i], cuota_2015[i], t_2015[i])
	print ""

ver_datos_2015()

# ---------------------------------------------------------------------------------
# VISUALIZAR LOS RESULTADOS IRPF 2015:
# ---------------------------------------------------------------------------------


def ver_calculos_2015():

	print "\t\tRESULTADO CALCULOS IRPF 2015"
	print "=" * 55
	print "Base\t\tCuota\t\ttme\t\tt\'"
	print "-" * 55
	for i in range(len(base_sim)):
		print "%s\t\t%s\t\t%s\t\t%s"% (base_sim[i], round(ci_2015[i], 3), 
			round(t_me_2015[i], 3), round(t_mg_2015[i],3))

ver_calculos_2015()

# ---------------------------------------------------------------------------------
#                    GRAFICO DE LOS RESULTADOS DE LA REFORMA 2015:
# ---------------------------------------------------------------------------------

plt.figure("cuota_2015")
plt.plot(ci_2015, t_mg_2015, label = "cuota_tmg_2015")
plt.plot(ci_2015, t_me_2015, label = "cuota_tme_2015")
plt.margins(0.1)
plt.legend(loc = 0)

plt.figure("Base_2015")
plt.plot(base_sim, t_mg_2015, label = "base_tmg_2015")
plt.plot(base_sim, t_me_2015, label = "base_tme_2015")
plt.margins(0.1)
plt.legend(loc = 0)

plt.figure("Base_Cuota__tme_2015")
plt.plot(base_sim, t_me_2015, label = "base_tme_2015")
plt.plot(ci_2015, t_me_2015, label = "cuota_tme_2015")
plt.margins(0.1)
# for i in range(len(base_2015)):
#    plt.axvline(base_2015[i], color = 'g')
plt.legend(loc = 0)
# plt.fill_between(base_sim, t_mg2015, t_me2015, where = (t_mg2015 > t_me2015), color = 'g', interpolate = True)  
# Pinta poligonos color verde entre las lineas cuando y1 < y2 
plt.show()


####################################################################################
#                       ANALISIS DE LA PROGRESIVIDAD 2015: 
####################################################################################

lp_actual = []
arp_actual = []
LP_2015 = [] # indice LP_2015
ARP_2015 = [] # indice ARP_2015


for i in range(len(base_sim)):

    LP_2015.append(t_mg_2015[i] / t_me_2015[i]) 
    ARP_2015.append((t_mg_2015[i] - t_me_2015[i]) / base_sim[i])

    lp_actual.append(t_mg_actual[i] / t_me_actual[i])
    arp_actual.append((t_mg_actual[i] - t_me_actual[i]) / base_sim[i])

# ---------------------------------------------------------------------------------
# VISUALIZAR LOS RESULTADOS PROGRESIVIDAD 2015:
# ---------------------------------------------------------------------------------


def ver_calculos_prog():

	print "\tANALISIS DE PROGRESIVIDAD"
	print "=" * 60
	print "Base\tt\'\tt*\tLP_14\tLP_15\tARP_14*\tARP_15*"
	print "-" * 60
	for i in range(len(base_sim)):
	    print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (base_sim[i], round(t_mg_2015[i], 4), 
	    	round(t_me_2015[i], 3), round(lp_actual[i], 3), round(LP_2015[i], 3), 1000000 * arp_actual[i], 1000000 * ARP_2015[i])


ver_calculos_prog()

# ---------------------------------------------------------------------------------
#                        GRAFICO DEL INDICE LP_2015 2015
# ---------------------------------------------------------------------------------

plt.suptitle(u'ANÁLISIS DE PROGRESIVIDAD')
plt.subplot(2,1,1) # Divide en dos el lienzo por la vertical
plt.plot(base_sim, LP_2015, label = u"Índice LP_2015") 
plt.scatter(base_sim, LP_2015) # añade los puntos en cada base

# agrega lineas verticales en cada tramo de base
# for i in range(len(base_2015)):
#     plt.axvline(base_2015[i], color = 'g')

plt.margins(0.1)
plt.legend()

# ---------------------------------------------------------------------------------
#                        GRAFICO INDICE ARP_2015 2015
# ---------------------------------------------------------------------------------

plt.subplot(2,1,2)
plt.plot(base_sim, ARP_2015, label = u"Índice ARP_2015")
plt.scatter(base_sim, ARP_2015)


# for i in range(len(base_2015)):
#    plt.axvline(base_2015[i], color = 'g')

plt.margins(0.1) # AGREGA UN MARGEN PARA VISUALIZAR EL GRÁFICO COMPLETO EN LOS LIMITES
plt.legend()
plt.xlabel('BASE')  # Colocamos la etiqueta en el eje x
plt.ylabel('INDICE')  # Colocamos la etiqueta en el eje y
plt.show()
