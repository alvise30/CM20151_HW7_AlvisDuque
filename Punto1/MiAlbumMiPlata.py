import numpy as np 
import matplotlib as mpl
import random 
import time
import pylab as pl

#En primera instancia creamos una matriz de 640 caramelos 
size = 640 
caramelos = np.zeros(size)

#Ahora en cada posicion del arreglo se ubica una carta diferente. 
for i in range(0,len(caramelos)):
	caramelos[i] = i

# for i in range(0,640):
# 	PlataGastada = PlataGastada +400	##Con este algoritmo se queria ver cuanto se gastaria si cada carta solo 
# print(PlataGastada)					##apareciera una vez. El precio seria de 256000 COP

def llenarAlbum(caramelos):
	PlataGastada = 0
	miAlbum= []
	repetidas = []
	while len(miAlbum) < 640:
		PlataGastada = PlataGastada + 400 #El precio por cada caramelo es de 400 COP segun el enunciado
		item = random.choice(caramelos)
		if item in miAlbum:
			repetidas.append(item) #Aqui se guardan las repetidas. Just in case... 
		else:
			miAlbum.append(item)
	return PlataGastada

#Ahora esta función define el numero de albums que se van a llenar, y se saca la media y la varianza de los datos 
def LlenarMAlbums(caramelos, llenarAlbum, numAlbums):
	X = []
	i = 1
	while i <= numAlbums:
		X.append(llenarAlbum(caramelos))
		i = i + 1
	mu_m = np.mean(X)
	sigma_m = np.var(X)
	return  mu_m, sigma_m

#print(LlenarMAlbums(caramelos,llenarAlbum, 10))
#Ahora se sacan la variancia y la media de m= 10 : 10*10 : 10

E_x= [] #Aqui se van a guardar todos las medias de cada vez que se llena el album
Var_x= [] #Se guarda la Varianza de cada vez que se llena el album 
start_time = time.time()
paso= []

#Esta es la parte complicada! 
#Ahora se hace un loop que llena el album 100 veces, dado a que se quiere que el paso sea de 10 en 10. Esto para obtener
#100 datos de cuantas veces se está llenando el album de 10 en 10. Es por esto que es tan demorado...  
for i in range(1,100):
	j = i*10
	paso.append(j)
	E_x.append(LlenarMAlbums(caramelos,llenarAlbum,j)[0])
	Var_x.append(LlenarMAlbums(caramelos,llenarAlbum,j)[1])
print(E_x)
print(Var_x)
print("--- El programa se demora en correr %s segundos. Tener paciencia por favor.Gracias ---" % (time.time() - start_time))


pl.subplot(2, 1, 1)
pl.plot(paso,E_x,'b')
pl.title('Promedio y varianza de los precios \n de llenar el album m veces')
pl.ylabel('Promedio')

pl.subplot(2, 1, 2)
pl.plot(paso,Var_x,'r')
pl.xlabel('Numero de veces que se llena el Album (m)')
pl.ylabel('Varianza')
pl.savefig('PromediosMSinProba.png')
pl.show()


#SEGUNDO PUNTO
#El enunciado es un poco confuso acerca de que es lo que se debe hallar, así que se promediaron los precios promedios
#de cada vez que se llena un album M veces. A cada media se le resto ese numero y se le saco valor absoluto.
#Para hallar el mejor m, (dado que en ningún caso la resta dio menos a 10^⁻6) se busco el caso en que el valor fuera
#minimo, se hallo la posición de este valor y se le sumo 1 y multiplico por 10, pues nuestro primer m = 10. 

E_x_m = np.mean(E_x)
dif = np.abs(E_x - E_x_m)
mini = np.min(dif) #Se saca el minimo de las diferencias, así este significa el error mas pequeño 
itemindex = np.where(dif==mini)
int1= itemindex[0]
mbuscado= (int1[0] +1)*10 #La posicion empieza desde cero así que se le suma uno y se mltiplica por 10 y esta es la escala de los m 
print('El m buscado es entonces %s ' %mbuscado)
PromeBuscado = LlenarMAlbums(caramelos,llenarAlbum, mbuscado)[0]

print('Dado a que esto es un proceso bastante aleatorio pues entre caso y caso varia considerablemente como se puede ver en la varianza y en las diferencias. ')
print('Según esto es dificil sacar un valor fijo del album pues es algo bastante aleatorio. Sin embargo haciendo el caso con el mbuscado %s' %mbuscado)
print('Encontramos que en el mejor caso del precio es %s sin embargo esto es un promedio de los casos que se llena el album  ' %PromeBuscado )



pl.plot(paso, dif, color="DarkOliveGreen", linewidth=2.5, linestyle="-", label="Media")
pl.ylabel('Diferencia de las medias')
pl.xlabel('Numero de veces que se llena el album (m)')
pl.title('Grafica de la diferencia entre los premedios\n en funcion de los albums llenados')
pl.savefig('DiferenciaMSinProba.png')
pl.show()