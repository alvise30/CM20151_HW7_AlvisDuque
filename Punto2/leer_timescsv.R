#Leer el archivo
times <- read.csv('times.csv')
#Cargar los datos
date <- times[,2]

#Creamos un vector para guardar las diferencias de tiempos obtenidas
x <- c(NULL)

#Calculamos todas las diferencias de tiempo
for (i in 2:20) {
  x <- c(x,strptime(sdate[i], format="%Y.%m.%d_%H:%M:%S")-strptime(sdate[i-1], format="%Y.%m.%d_%H:%M:%S"))
}

#probando maricadas
k=4
strptime(sdate[k], format="%Y.%m.%d_%H:%M:%S")-strptime(sdate[k-1], format="%Y.%m.%d_%H:%M:%S")
