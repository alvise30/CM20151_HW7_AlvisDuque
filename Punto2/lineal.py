

from pylab import *
import numpy as np
import pyfits
import pandas as pd


#Funciones

#Esta funcion convierte de segundos a minutos donde sea necesario; luego suma los intervalos para crear continuidad en el tiempo
def prep_time(times): 
    tmp = times.copy()    
    #Pasamos de segundos a minutos donde sea necesario.
    t = where(tmp==45.)
    for i in t:
        tmp[i] = tmp[i]/60.
        
    #Pasamos a horas.    
    for k in range(len(tmp)):
       tmp[k] = tmp[k]/60.
        
    #Sumamos los intervalos
    for j in range(len(times)-1):
       tmp[j+1] = tmp[j] + tmp[j+1]
    return tmp

#Cargamos y leemos los ficheros
#Leemos el FITS
hdulist = pyfits.open('hmi.m_45s.magnetogram.subregion_x1y1.fits')
#Cargamos el archivo que contiene los intervalos de medicion
timesfile = pd.read_table('intervalos.txt')

#Extraemos los datos del fichero FITS
data = hdulist[0].data
#Extraemos la informacion .txt
times = timesfile['Intervalo']

#Cerramos el archivo (Lei que porq ocupa mucho espacio en la memorio y puede entorpecer los procesos)
hdulist.close()

ztimes = prep_time(times) #Preparamos los tiempos

#Implementamos las caminatas para lograr el mejor ajuste con el modelo LINEAL
#Cargamos los datos y definimos x_obs y y_obs
y_obs = data[:,138:148,241:251]
x_obs = ztimes

#Likelihood
def likelihood(y_obs, y_model):
    chi_squared = (1.0/2.0)*sum(((y_obs-y_model))**2)
    return -chi_squared

#Modelo lineal
def linear_model(x_obs, a, b):
    return x_obs*a + b

def inicializar(x_obs, y_obs,i,j):
    a_walk = empty((0)) #this is an empty list to keep all the steps
    b_walk = empty((0))
    l_walk = empty((0))

    a_walk = append(a_walk, 2*(np.random.random()-0.5)) #ATENCION!! Mirar que tipo de generador de nuemeros aleatoreas debe usarse
    b_walk = append(b_walk, 400*(np.random.random()-0.5))

    y_init = linear_model(x_obs, a_walk[0], b_walk[0])
    l_walk = append(l_walk,likelihood(y_obs[:,i,j], y_init))
    return a_walk, b_walk, l_walk

def iteraciones(a_walk, b_walk, l_walk,  i, j):
    
    n_iterations = 20000 #this is the number of iterations I want to make
    for k in range(n_iterations):
        a_prime = np.random.normal(a_walk[k], 0.1) 
        b_prime = np.random.normal(b_walk[k], 0.1)

        y_init = linear_model(x_obs, a_walk[k], b_walk[k])
        y_prime = linear_model(x_obs, a_prime, b_prime)
    
        l_prime = likelihood(y_obs[:,i,j], y_prime)
        l_init = likelihood(y_obs[:,i,j], y_init)
    
        alpha = l_prime-l_init
        
        if(alpha>=1.0):
            a_walk  = append(a_walk,a_prime)
            b_walk  = append(b_walk,b_prime)
            l_walk = append(l_walk, l_prime)
        else:
            beta = np.random.random()
            if(beta<=exp(alpha)):
                a_walk = append(a_walk,a_prime)
                b_walk = append(b_walk,b_prime)
                l_walk = append(l_walk, l_prime)
            else:
                a_walk = append(a_walk,a_walk[k])
                b_walk = append(b_walk,b_walk[k])
                l_walk = append(l_walk, l_init)
                
    return a_walk, b_walk, l_walk

a_walk = []
b_walk = []
l_walk = []

fileout = open('lineal.txt', 'w')
fileout.write('Observacion\tMejor Ajuste\tParametro\n')
fileout.close()

for i in range(len(y_obs[0,:,0])):
    for j in range(len(y_obs[0,0,:])):
        a_walk, b_walk, l_walk = inicializar(x_obs, y_obs, i, j)
        a_walk, b_walk, l_walk = iteraciones(a_walk, b_walk, l_walk, i, j)
        
        #Escoger el mejor
        max_likelihood_id = argmax(l_walk)
        best_a = a_walk[max_likelihood_id]
        best_b = b_walk[max_likelihood_id]

        #Escribir el archivo
        fileout = open('lineal.txt', 'a')
        fileout.write('Obser_'+str(i)+'_'+str(j)+'\t'+str(best_a)+'\ta\n' +
                      'Obser_'+str(i)+'_'+str(j)+'\t'+str(best_b)+'\tb\n' + 
                      'Obser_'+str(i)+'_'+str(j)+'\t'+str(-l_walk[max_likelihood_id]) +'\tLikelihood\n')
        fileout.close()
