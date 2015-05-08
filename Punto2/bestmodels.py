

from pylab import *
import pandas as pd
import pyfits
import matplotlib as plt

#Cargamos los archivos del punto anterior
lin = pd.read_table('lineal.txt')
gauss = pd.read_table('lineal_gaussiano.txt')
paso = pd.read_table('lineal_paso.txt')

#Funciones
#Funcion para extraer los valores d elos likelihoods del archivo que pasa como parametro
def ext_llh(lin):
    likelihoods=[]
    for i in range(len(lin.iloc[:,2])):   
        if lin.iloc[i,2] == 'Likelihood':
          likelihoods.append(lin.iloc[i,1])
    return likelihoods

#Esta funcion convierte de segundos a minutos donde sea necesario; luego suma los intervalos para crear continuidad en el tiempo
def prep_time(times): 
    tempo = times.copy()    
    #Pasamos de segundos a minutos donde sea necesario.
    t = where(tempo==45.)
    for i in t:
        tempo[i] = tempo[i]/60.
        
    #Pasamos a horas.    
    for k in range(len(tempo)):
       tempo[k] = tempo[k]/60.
        
    #Sumamos los intervalos
    for j in range(len(times)-1):
       tempo[j+1] = tempo[j] + tempo[j+1]
    return tempo

#Funcion para desplazarse por el arreglo de datos para graficar
def comprobar(i, j, lentotal):
    if j+1/lentotal == 1:
        i+=1
        j=0
    else:
        j+=1        
    return i, j

#Extraemos los valores de los likehoods de los archivos
llh_lin = ext_llh(lin)
llh_gauss = ext_llh(gauss)
llh_paso = ext_llh(paso)

#Comparamos los likelihoods entre ellos para saber cual es el mejor ajuste a los datos en cada una de las situaciones
tmp=[]
for i in range(len(llh_lin)):
    if abs(llh_paso[i]) >= abs(llh_lin[i]):
        if abs(llh_gauss[i]) >= (llh_lin[i]):
            tmp.append(1)
        else:
            tmp.append(2)
    elif abs(llh_gauss[i]) <= abs(llh_paso[i]):
        tmp.append(2)
    else:
        tmp.append(3)

#Escribir el archivo bestmodels.txt
fileout = open('bestmodels.txt', 'w')
fileout.write('Observacion\tModelo\tMejor Ajuste\tParametro\n')
fileout.close()
for i in range(len(llh_lin)):
    element = tmp[i]
    if element == 1: #Comprobar si es lineal        
        fileout = open('bestmodels.txt', 'a')            
        fileout.write(str(lin.iloc[(i*3)+0,0])+ '\tL\t' + str(lin.iloc[(i*3)+0,1]) + '\t' + str(lin.iloc[(i*3)+0,2]) + '\n' + 
                        str(lin.iloc[(i*3)+1,0])+ '\tL\t' + str(lin.iloc[(i*3)+1,1]) + '\t' + str(lin.iloc[(i*3)+1,2]) + '\n' +
                        str(lin.iloc[(i*3)+2,0])+ '\tL\t' + str(lin.iloc[(i*3)+2,1]) + '\t' + str(lin.iloc[(i*3)+2,2]) + '\n')
        fileout.close()
                   
    elif element == 2: #Comprobar si es lineal Gaussiano
        fileout = open('bestmodels.txt', 'a')            
        fileout.write(str(gauss.iloc[(i*5)+0,0])+ '\tL_G\t' + str(gauss.iloc[(i*5)+0,1]) + '\t' + str(gauss.iloc[(i*5)+0,2]) + '\n' + 
                        str(gauss.iloc[(i*5)+1,0])+ '\tL_G\t' + str(gauss.iloc[(i*5)+1,1]) + '\t' + str(gauss.iloc[(i*5)+1,2]) + '\n' +
                        str(gauss.iloc[(i*5)+2,0])+ '\tL_G\t' + str(gauss.iloc[(i*5)+2,1]) + '\t' + str(gauss.iloc[(i*5)+2,2]) + '\n' +
                        str(gauss.iloc[(i*5)+3,0])+ '\tL_G\t' + str(gauss.iloc[(i*5)+3,1]) + '\t' + str(gauss.iloc[(i*5)+3,2]) + '\n' +
                        str(gauss.iloc[(i*5)+4,0])+ '\tL_G\t' + str(gauss.iloc[(i*5)+4,1]) + '\t' + str(gauss.iloc[(i*5)+4,2]) + '\n')
        fileout.close()
               
    elif element == 3: #Comprobar si es lineal Paso
        fileout = open('bestmodels.txt', 'a')            
        fileout.write(str(paso.iloc[(i*6)+0,0])+ '\tL_P\t' + str(paso.iloc[(i*6)+0,1]) + '\t' + str(paso.iloc[(i*6)+0,2]) + '\n' + 
                        str(paso.iloc[(i*6)+1,0])+ '\tL_P\t' + str(paso.iloc[(i*6)+1,1]) + '\t' + str(paso.iloc[(i*6)+1,2]) + '\n' +
                        str(paso.iloc[(i*6)+2,0])+ '\tL_P\t' + str(paso.iloc[(i*6)+2,1]) + '\t' + str(paso.iloc[(i*6)+2,2]) + '\n' +
                        str(paso.iloc[(i*6)+3,0])+ '\tL_P\t' + str(paso.iloc[(i*6)+3,1]) + '\t' + str(paso.iloc[(i*6)+3,2]) + '\n' +
                        str(paso.iloc[(i*6)+4,0])+ '\tL_P\t' + str(paso.iloc[(i*6)+4,1]) + '\t' + str(paso.iloc[(i*6)+4,2]) + '\n' +
                        str(paso.iloc[(i*6)+5,0])+ '\tL_P\t' + str(paso.iloc[(i*6)+5,1]) + '\t' + str(paso.iloc[(i*6)+5,2]) + '\n')
        fileout.close() 

#Modelos
#Modelo lineal
def linear_model(x_obs, a, b):
    return x_obs*a + b
#Modelo lineal Gaussiano
def linear_gauss_model(x_obs, a, b, c, d):
    return a + b*x_obs + 1/(c*sqrt(2*pi)) * exp((-0.5)*((x_obs-d)/c)**2)
#Modelo lineal Gaussiano
def linear_paso_model(x_obs, a, b, c, d, e):
    return a + b*x_obs + c*(1 + (2*arctan(d*(x_obs-e))/pi))

#Leer fifheros
#Leemos el FITS
hdulist = pyfits.open('hmi.m_45s.magnetogram.subregion_x1y1.fits')
#Cargamos el archivo que contiene los intervalos de medicion
timesfile = pd.read_table('intervalos.txt')
#Cargamos el archivo que contiene los parametros de los mejores modelos
bestm = pd.read_table('bestmodels.txt')

#Extraemos los datos del fichero FITS
data = hdulist[0].data
#Extraemos la informacion .txt
times = timesfile['Intervalo']

#Cerramos el archivo (Lei que porq ocupa mucho espacio en la memorio y puede entorpecer los procesos)
hdulist.close()

#Cargamos los datos y definimos x_obs y y_obs
y_obs = data[:,138:140,241:243]
x_obs = prep_time(times)

#Graficar
k=0
i = 0
j = 0
for element in tmp:   
    if element == 1:
        #figsize(8,5.5)
        best_y = linear_model(x_obs, bestm.iloc[k+0,2], bestm.iloc[k+1,2])
        scatter(x_obs,y_obs[:,i,j], color = 'grey', label = (u'Observacion'))
        plot(x_obs, best_y, 'b', label = (u'Ajuste Lineal'))
        legend(loc=4, fontsize=12)
        xlabel(r'$Tiempo\ [horas]$', fontsize=16)
        ylabel(r'$Campo\ Magn\'etico\ [Gauss]$', fontsize=16)
        title(u'Observacion_' +str(i)+ '_' +str(j), fontsize=24)
        text(0,10, 'a= '+str(bestm.iloc[k+0,2]) + '\nb= '+str(bestm.iloc[k+1,2]) + '\nLikelihood= ' 
             +str(bestm.iloc[k+2,2]), fontsize=12)
        text(0,0, r'$at+b$', fontsize=24)
        savefig(u'Observacion_'+str(i)+'_'+str(j)+'.pdf')
        close()
        k+=3        
        print 'lineal',i,j
    elif element == 2:
       # plt.figsize(8,5.5)
        best_y = linear_gauss_model(x_obs, bestm.iloc[k+0,2], bestm.iloc[k+1,2], bestm.iloc[k+2,2], bestm.iloc[k+3,2])
        scatter(x_obs,y_obs[:,i,j], color ='grey', label = u'Observacion')
        plot(x_obs, best_y, 'm', label = u'Ajuste Lineal Gaussiano')
        legend(loc=2)
        xlabel(r'$Tiempo\ [horas]$', fontsize=16)
        ylabel(r'$Campo\ Magn\'etico\ [Gauss]$', fontsize=16)
        title(u'Observacion_' +str(i)+ '_' +str(j), fontsize=24)
        text(4.5,-15, 'a= '+str(bestm.iloc[k+0,2]) + '\nb= '+str(bestm.iloc[k+1,2]) + '\nc= '+str(bestm.iloc[k+2,2]) + 
             '\nd= '+str(bestm.iloc[k+3,2]) + '\nLikelihood= ' +str(bestm.iloc[k+4,2]), fontsize=12)
        text(-0.5,5, r'$a+bt+\frac{1}{c\sqrt{\pi}}e^{-\frac{1}{2}[\frac{t-d}{c}]^2}$', fontsize=24)
        savefig(u'Observacion_'+str(i)+'_'+str(j)+'.pdf')
        close()
        k+=5                
        print 'gauss',i,j
    elif element == 3:
        #figsize(8,5.5)
        best_y = linear_paso_model(x_obs, bestm.iloc[k+0,2], bestm.iloc[k+1,2], bestm.iloc[k+2,2], bestm.iloc[k+3,2], bestm.iloc[k+4,2])
        scatter(x_obs,y_obs[:,i,j], color = 'grey', label = (u'Observacion'))
        plot(x_obs, best_y, 'g', label = (u'Ajuste Lineal Paso'))
        legend(loc=2, fontsize=12)
        xlabel(r'$Tiempo\ [horas]$', fontsize=16)
        ylabel(r'$Campo\ Magn\'etico\ [Gauss]$', fontsize=16)
        title(u'Observacion_' +str(i)+ '_' +str(j), fontsize=24)
        text(4.5,-15, 'a= '+str(bestm.iloc[k+0,2]) + '\nb= '+str(bestm.iloc[k+1,2]) + '\nc= '+str(bestm.iloc[k+2,2]) + 
             '\nd= '+str(bestm.iloc[k+3,2]) + '\ne= '+str(bestm.iloc[k+4,2]) + '\nLikelihood= ' +str(bestm.iloc[k+5,2]), fontsize=12)
        text(-0.5,5, r'$a+bt+c[1+\frac{2}{\pi}arctan(d(t-e))]$', fontsize=20)
        savefig(u'Observacion_'+str(i)+'_'+str(j)+'.pdf')
        close()        
        k+=6        
        print 'paso',i,j
        
    i, j = comprobar(i, j, len(tmp)/2)
