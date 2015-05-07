library(lubridate)


#Leer el archivo
times <- read.csv('times.csv')
#Cargar los datos
date <- times[,2]

#Creamos un vector para guardar las diferencias de tiempos obtenidas
x <- c('Intervalo',45.0)
#Calculamos todas las diferencias de tiempo
for (i in 2:length(date)) {
  tmp <- strptime(date[i], format="%Y.%m.%d_%H:%M:%S")-strptime(date[i-1], format="%Y.%m.%d_%H:%M:%S")
  x <- c(x,tmp)
}
x <- c(x,45.0)
#Escribimos un .txt para guardar los datos
fout<-file("intervalos.txt")
write(x, fout, sep = '\n')
close(fout)