import numpy as np 
import matplotlib as mpl
import random 

#En primera instancia creamos una matriz de 640 caramelos 
size = 640 
caramelos = np.zeros(size)

#Ahora en cada posicion del arreglo se ubica una carta diferente. 
for i in range(0,len(caramelos)):
	caramelos[i] = i

#definimos una funcion que mezcle el arreglo de las caramelos cada vez
def my_shuffle(array):
        random.shuffle(array)
        return array

# for i in range(0,640):
# 	PlataGastada = PlataGastada +400	##Con este algoritmo se queria ver cuanto se gastaria si cada carta solo 
# print(PlataGastada)					##apareciera una vez. El precio seria de 256000 COP

def llenarAlbum(caramelos):
	PlataGastada = 0
	miAlbum= []
	repetidas = []
	while len(miAlbum) < 640:
		my_shuffle(caramelos)
		for item in caramelos:
			PlataGastada = PlataGastada + 400 #El precio por cada caramelo es de 400 COP segun el enunciado
			my_shuffle(caramelos)
			if item in miAlbum:
				repetidas.append(item) #Aqui se guardan las repetidas. Just in case... 
			else:
				miAlbum.append(item)
	return PlataGastada
print(llenarAlbum(caramelos))

def LlenarMAlbums(caramelos, llenarAlbum, numAlbums):
	X = []
	i = 1
	while i <= numAlbums:
		X.append(llenarAlbum(caramelos))
		i = i + 1
	E_X   = np.mean(X)
	Var_X = np.var(X)
	return X, Var_X, E_X

print(LlenarMAlbums(caramelos,llenarAlbum, 10))





