
# coding: utf-8

# # ANALISIS DE PROGRESIVIDAD DE LA REFORMA DEL IRPF PARA EL CASO DE ARAGÓN:
# 
# ## 1. Introducción de datos: Introducimos los datos para hacer cálculos, se presentan capturas de los datos usados.
# 
# 

# In[83]:

#!/usr/bin/env python


# ---------------------------------------------------------------------------------
# CARGAR LIBRERIAS
# ---------------------------------------------------------------------------------

import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import seaborn as sns

# ESTO INCRUSTA LOS GRAFICOS EN LA MISMA PAGINA
get_ipython().magic(u'matplotlib inline')

sns.set_context(rc={"figure.figsize": (18, 13)})

print u"Introducimos datos para simular una serie de rentas para aplicar los tipos del IRPF y estudiar su comportamiento"
print u"La simulación por defecto crea una serie desde 5000 hasta 400000 con incrementos de 1000"

# r = raw_input(u"Para cambiar los parámetros de la simulación escriba 1, sino 0: ")


# ## INTRODUCCIÓN DE LOS DATOS DE IRPF PARA EL CASO DE ARAGON:
# 
# ![Texto alternativo](https://www.evernote.com/shard/s57/sh/bb901ec4-6461-46da-994e-5698cf7e0223/88c2d1cc0207922322f796e822f09901/res/365dce85-0986-4312-89da-3f25e1a1493f/skitch.png?resizeSmall&width=832 "tarifa global Aragon 2014")
# 
# ![](https://www.evernote.com/shard/s57/sh/f4676837-7542-4bfc-bcab-a8e654e884e4/43b8723bb892009dd150738999a6f505/res/4301a6c4-2fc0-4715-885d-05fe9daa6fd2/skitch.png?resizeSmall&width=832 "Tarifa estatal 2015")
# 
# ![](https://www.evernote.com/shard/s57/sh/6f7bc02f-ee12-4857-b875-6123771dbc21/60b284839a59f900a42a47d631f00ed4/res/bd426445-1e02-4b20-8883-9a3c23a5181c/skitch.png "Tarifa de Aragon 2015")

# In[84]:

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


# In[85]:

####################################################################################
##############             SIMULACIÓN E INCOGNITAS:             ####################
####################################################################################

# SIMULAMOS UNA SERIE DE RENTAS:

# calculamos una serie de bases liquidas para simular el comportamiento. Agregar # al principio de la linea para activar la siguiente.
try:
    if int(r) == 1:
        base_sim = range(int(raw_input(">Renta de inicio: ")), int(raw_input(">Renta final: ")), int(raw_input(">Incremento: "))) # eliminar el primer # para controlar la simulacion
    else:
        base_sim = range(5000, 400000, 1000)
except (RuntimeError, TypeError, NameError):
    base_sim = range(5000, 400000, 1000)
    
# DECLARAMOS LAS INCOGNITAS:

t_me_actual = []
t_mg_actual = []
ci_actual = []

ci_2015 = []
t_me_2015 = []
t_mg_2015 = []


# In[86]:

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


# In[86]:




# In[87]:

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


# In[192]:

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

plt.figure(figsize=(10,6), dpi=800)
plt.plot(base_sim, t_mg_actual)
plt.fill_between(base_sim, t_mg_actual, 0, alpha=0.3)
plt.yticks(t_actual)
plt.xticks(base_actual)
plt.margins(0.03)
plt.xlim(0,350000)


plt.show()


# ## DATOS DE LA REFORMA DEL IRPF 2015

# In[194]:

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

plt.figure(figsize=(10,6), dpi=800)
plt.plot(base_sim, t_mg_2015)
plt.fill_between(base_sim, t_mg_2015, 0, alpha=0.3)
plt.yticks(t_2015)
plt.xticks(base_2015)
plt.xlim(0,65000)
plt.margins(0.03)


plt.show()


# ## RESULTADOS SIMULADOS:

# In[195]:

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


# ## ANÁLISIS GRÁFICO DE LA REFORMA:
# 
# > LAS SOMBRAS SON EL AREA ENTRE LAS CURVAS RESPECTO DE TIPO MEDIO Y MARGINAL PARA EL CASO QUE NO SE GRAFICA.
# 
# 

# In[196]:

# ---------------------------------------------------------------------------------
#                    GRAFICO DE IRFP 2014:
# ---------------------------------------------------------------------------------

plt.figure(dpi=900)
plt.subplot(3,2,1)
plt.plot(ci_actual, t_mg_actual, label = "cuota_tmg_2014")
plt.plot(ci_actual, t_me_actual, label = "cuota_tme_2014")
plt.fill_between(ci_2015, t_mg_2015, t_me_2015, color = 'black', interpolate = True, alpha=0.1)
plt.margins(0.1)
plt.legend(loc = 0)

plt.subplot(3,2,3)
plt.plot(base_sim, t_mg_actual, label = "base_tmg_2014")
plt.plot(base_sim, t_me_actual, label = "base_tme_2014")
plt.fill_between(base_sim, t_mg_2015, t_me_2015, color = 'black', interpolate = True, alpha=0.1)  
plt.margins(0.1)
plt.legend(loc = 0)

plt.subplot(3,2,5)
plt.plot(t_me_actual, base_sim, label = "base_tme_2014")
plt.plot(t_me_actual, ci_actual, label = "cuota_tme_2014")
plt.fill_between(t_me_2015, base_sim, ci_2015, color = 'black', interpolate = True, alpha=0.1)
plt.margins(0.1)
plt.xticks([round(t_actual[i], 2) for i in range(len(t_actual))])

# Pinta poligonos color verde entre las lineas cuando y1 < y2 
# ---------------------------------------------------------------------------------
#                    GRAFICO DE LOS RESULTADOS DE LA REFORMA 2015:
# ---------------------------------------------------------------------------------

plt.subplot(3,2,2)
plt.plot(ci_2015, t_mg_2015, label = "cuota_tmg_2015")
plt.plot(ci_2015, t_me_2015, label = "cuota_tme_2015")
plt.fill_between(ci_actual, t_mg_actual, t_me_actual, color = 'black', interpolate = True, alpha=0.1)
plt.margins(0.031)
plt.legend(loc = 0)

plt.subplot(3,2,4)
plt.plot(base_sim, t_mg_2015, label = "base_tmg_2015")
plt.plot(base_sim, t_me_2015, label = "base_tme_2015")
plt.fill_between(base_sim, t_mg_actual, t_me_actual, color = 'black', interpolate = True, alpha=0.1)  
plt.margins(0.031)
plt.legend(loc = 0)

plt.subplot(3,2,6)
plt.plot(t_me_2015, base_sim, label = "base_tme_2015")
plt.plot(t_me_2015, ci_2015, label = "cuota_tme_2015")
plt.fill_between(t_me_actual, base_sim, ci_actual, color = 'black', interpolate = True, alpha=0.1)
plt.margins(0.031)
plt.xticks([round(t_2015[i], 2) for i in range(len(t_2015))])
#for i in range(len(base_2015)):
    # plt.axvline(base_2015[i], color = 'w')
#    plt.axvline(t_2015[i], color = "black", label = "t_2015 = %r" % round(t_2015[i], 3), alpha=0.4)


# Pinta poligonos color verde entre las lineas cuando y1 < y2 
plt.show()


# In[90]:




# In[91]:

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


# In[92]:

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


# # REPRESENTACION DE LOS INDICES ARP Y LP ANTES Y DESPUES DE LA REFORMA:

# In[110]:

plt.subplot(2,1,1)
plt.plot(base_sim, arp_actual, label = "ARP 2014")
plt.plot(base_sim, ARP_2015, label = "ARP 2015")
plt.fill_between(base_sim, arp_actual, ARP_2015, color = 'black', interpolate = True, alpha = 0.3) 
plt.legend()
plt.margins(0.03)

plt.subplot(2,1,2)
plt.plot(base_sim, lp_actual, label = "LP 2014")
plt.plot(base_sim, LP_2015, label = "LP 2015")
plt.fill_between(base_sim, lp_actual, LP_2015, color = 'black', interpolate = True, alpha=0.3) 
plt.legend()
plt.margins(0.03)


# # CALCULO DE GANACIA RELATIVA DE PROGRESIVIDAD:
# 
# > POR ENCIMA DE 0 ESTAMOS ANTES GANANCIAS DE PROGRESIVIDAD (MAS INTENSO) RESPECTO DEL MODELO DE 2014
# > POR DEBAJO DE 0 PERDIDAS DE PROGRESIVIDAD RESPECTO DEL AÑO 2014

# In[127]:

# CALCULO DE GANANCIA O PERDIDA DE PROGRESIVIDAD CON LOS INDICES LP Y ARP NORMALIZADOS

inc_arp = []
inc_lp = []


for i in range(len(base_sim)):
    try:
    
        inc_arp.append((ARP_2015[i] / arp_actual[i]) - 1 )
        inc_lp.append((LP_2015[i] / lp_actual[i]) - 1 )
    except ZeroDivisionError:
        inc_arp.append(0)
        inc_lp.append(0)

plt.figure("saldo", figsize = (13,8), dpi = 800)
plt.figure("saldo")
plt.plot(base_sim, inc_lp, label = "Saldo de Progresividad LP")
plt.plot(base_sim, inc_arp, label = "Saldo de Progresividad ARP")
plt.fill_between(base_sim, inc_lp, 0, color = "b", alpha = 0.1,)
plt.fill_between(base_sim, inc_arp, 0, color = "g", alpha = 0.1,)

plt.legend()


# # GRAFICOS DE LOS INDICES ARP Y LP INDIVIDUALIZADOS:

# In[94]:

# ---------------------------------------------------------------------------------
#                        GRAFICO DEL INDICE LP 2014 2015
# ---------------------------------------------------------------------------------

plt.suptitle(u'ANÁLISIS DE PROGRESIVIDAD')

plt.subplot(2,2,3) # Divide en dos el lienzo por la vertical primer 2 y segundo 2 por la horizontal

plt.plot(base_sim, lp_actual, label = u"Índice LP_2014") 
plt.scatter(base_sim, lp_actual) # añade los puntos en cada base

plt.margins(0.1)
plt.legend()


plt.subplot(2,2,4)

plt.plot(base_sim, LP_2015, label = "LP_2015")
plt.scatter(base_sim, LP_2015)

plt.margins(0.1) # AGREGA UN MARGEN PARA VISUALIZAR EL GRÁFICO COMPLETO EN LOS LIMITES
plt.legend()


# ---------------------------------------------------------------------------------
#                        GRAFICO INDICE ARP 2014 2015
# ---------------------------------------------------------------------------------

plt.subplot(2,2,1)
plt.plot(base_sim, arp_actual, label = u"Índice ARP_2014")
plt.scatter(base_sim, arp_actual, label = "ARP 2014")
plt.margins(0.1) # AGREGA UN MARGEN PARA VISUALIZAR EL GRÁFICO COMPLETO EN LOS LIMITES
plt.legend()

plt.subplot(2,2,2)
plt.plot(base_sim, ARP_2015, label = u"Índice ARP_2015")
plt.scatter(base_sim, ARP_2015, label = "ARP 2015")
plt.legend()

plt.show()


