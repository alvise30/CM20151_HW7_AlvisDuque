import numpy as np 
import matplotlib as mpl
import random 
import time
import pylab as pl

#En primera instancia creamos una matriz de 640 caramelos 
size = 640 
caramelos = np.zeros(size)
probabilidades = np.zeros(size)
#Ahora en cada posicion del arreglo se ubica una carta diferente. 
for i in range(0,len(caramelos)):
	caramelos[i] = i

for i in range(0,560):
	probabilidades[i] = 0.5
for i in range(560,600):
	probabilidades[i] = 1.0/6.0
for i in range(600,640):
	probabilidades[i] = 1.0/3.0


def llenarAlbum(caramelos):
	PlataGastada = 0
	miAlbum= []
	repetidas = []
	while len(miAlbum) < 640:
		PlataGastada = PlataGastada + 400 #El precio por cada caramelo es de 400 COP segun el enunciado
		item = random.choice(caramelos, p= probabilidades)
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
#Ahora se hace un loop que llena el album 10000 veces, dado a que se quiere que el paso sea de 10 en 10. 
for i in range(1,100):
	j = i*10
	paso.append(j)
	E_x.append(LlenarMAlbums(caramelos,llenarAlbum,j)[0])
	Var_x.append(LlenarMAlbums(caramelos,llenarAlbum,j)[1])
print(E_x)
print(Var_x)
print("--- El programa se demora en correr %s segundos. Tener paciencia por favor.Gracias ---" % (time.time() - start_time))


# pl.plot(paso, E_x, color="blue", linewidth=2.5, linestyle="-", label="Media")
# pl.plot(paso, Var_x, color="red", linewidth=2.5, linestyle="-", label="Varianza")
# pl.show()
fig1,ax1 = pl.subplots()
ax1.plot(paso,E_x,'b')
ax1.set_ylabel('Promedio $',color='b')

ax2 = ax1.twinx()
ax2.plot(paso,Var_x,'r')
ax2.set_ylabel('Varianza $',color='r')
pl.show()

E_x_m = np.mean(E_x)
dif = np.abs(E_x - E_x_m)
mini = np.min(dif)
itemindex = np.where(dif==mini)
int1= itemindex[0]
mbuscado= (int1[0] +1)*10
print(mbuscado)
nProme = LlenarMAlbums(caramelos,llenarAlbum, mbuscado)

pl.plot(paso, dif, color="DarkOliveGreen", linewidth=2.5, linestyle="-", label="Media")
pl.ylabel('Diferencia de las medias')
pl.xlabel('Numero de veces que se llena el album (m)')
pl.title('Grafica de la diferencia entre los premedios\n en funcion de los albums llenados')
pl.show()