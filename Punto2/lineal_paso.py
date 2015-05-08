

from pylab import *
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

def inicializar(x_obs, y_obs,i,j):
    a_walk = empty((0)) #this is an empty list to keep all the steps
    b_walk = empty((0))
    c_walk = empty((0))
    d_walk = empty((0))
    e_walk = empty((0))
    l_walk = empty((0))

    #randrange(start, stop[, step])

    a_walk = append(a_walk, (200*(np.random.random()-0.5))) #ATENCION!! Mirar que tipo de generador de nuemeros aleatoreas debe usarse
    b_walk = append(b_walk, -16)
    c_walk = append(c_walk, 2.5)
    d_walk = append(d_walk, 3.0)
    e_walk = append(e_walk, 3.4)

    y_init = linear_paso_model(x_obs, a_walk[0], b_walk[0], c_walk[0], d_walk[0], e_walk[0])
    l_walk = append(l_walk,likelihood(y_obs[:,i,j], y_init))
    return a_walk, b_walk, c_walk, d_walk, e_walk, l_walk

def iteraciones(a_walk, b_walk, c_walk, d_walk, e_walk, l_walk,  i, j):
    
    n_iterations = 20000 #this is the number of iterations I want to make
    for k in range(n_iterations):
        a_prime = np.random.normal(a_walk[k], 0.5) 
        b_prime = np.random.normal(b_walk[k], 0.3)
        c_prime = np.random.normal(c_walk[k], 0.2)
        d_prime = np.random.normal(d_walk[k], 0.3)
        e_prime = np.random.normal(e_walk[k], 0.1)

        y_init = linear_paso_model(x_obs, a_walk[k], b_walk[k], c_walk[k], d_walk[k], e_walk[k])
        y_prime = linear_paso_model(x_obs, a_prime, b_prime, c_prime, d_prime, e_prime)
    
        l_prime = likelihood(y_obs[:,i,j], y_prime)
        l_init = likelihood(y_obs[:,i,j], y_init)
    
        alpha = l_prime-l_init
        if(alpha>=0.0):
            a_walk  = append(a_walk,a_prime)
            b_walk  = append(b_walk,b_prime)
            c_walk  = append(c_walk,c_prime)
            d_walk  = append(d_walk,d_prime)
            e_walk  = append(e_walk,e_prime)
            l_walk = append(l_walk, l_prime)
        else:
            beta = np.random.random()
            if(beta<=alpha):
                a_walk = append(a_walk,a_prime)
                b_walk = append(b_walk,b_prime)
                c_walk = append(c_walk,c_prime)
                d_walk = append(d_walk,d_prime)
                e_walk = append(e_walk,e_prime)
                l_walk = append(l_walk, l_prime)
            else:
                a_walk = append(a_walk,a_walk[k])
                b_walk = append(b_walk,b_walk[k])
                c_walk = append(c_walk,c_walk[k])
                d_walk = append(d_walk,d_walk[k])
                e_walk = append(e_walk,e_walk[k])
                l_walk = append(l_walk, l_init)
                
    return a_walk, b_walk, c_walk, d_walk, e_walk, l_walk


#Cargar y leer ficheros
#Leemos el FITS
hdulist = pyfits.open('hmi.m_45s.magnetogram.subregion_x1y1.fits')
#Cargamos el archivo que contiene los intervalos de medicion
timesfile = pd.read_table('intervalos.txt')

#Extraemos los datos del fichero FITS
data = hdulist[0].data
#Extraemos la informacion .txt
times = timesfile['Intervalo']

ztimes = prep_time(times) #Preparamos los tiempos
#Cargamos los datos y definimos x_obs y y_obs
y_obs = data[:,138:140,241:243]
x_obs = ztimes

#Likelihood
def likelihood(y_obs, y_model):
    chi_squared = (1.0/2.0)*sum(((y_obs-y_model))**2)
    return -chi_squared

#Modelo lineal Paso
def linear_paso_model(x_obs, a, b, c, d, e):
    return a + b*x_obs + c*(1 + (2*arctan(d*(x_obs-e))/pi))

a_walk = []
b_walk = []
c_walk = []
d_walk = []
e_walk = []
l_walk = []

fileout = open('lineal_paso.txt', 'w')
fileout.write('Observacion\tMejor Ajuste\tParametro\n')
fileout.close()

for i in range(len(y_obs[0,:,0])):
    for j in range(len(y_obs[0,0,:])):
        a_walk, b_walk, c_walk, d_walk, e_walk, l_walk = inicializar(x_obs, y_obs, i, j)
        a_walk, b_walk, c_walk, d_walk, e_walk, l_walk = iteraciones(a_walk, b_walk, c_walk, d_walk, e_walk, l_walk, i, j)
        
        #Escoger el mejor
        max_likelihood_id = argmax(l_walk)
        best_a = a_walk[max_likelihood_id]
        best_b = b_walk[max_likelihood_id]
        best_c = c_walk[max_likelihood_id]
        best_d = d_walk[max_likelihood_id]
        best_e = e_walk[max_likelihood_id]

        #Escribir el archivo
        fileout = open('lineal_paso.txt', 'a')
        fileout.write('Obser_'+str(i)+'_'+str(j) +'\t'+ str(best_a) +'\ta\n'+
                      'Obser_'+str(i)+'_'+str(j) +'\t'+ str(best_b) +'\tb\n'+                       
                      'Obser_'+str(i)+'_'+str(j) +'\t'+ str(best_c) +'\tc\n'+ 
                      'Obser_'+str(i)+'_'+str(j) +'\t'+ str(best_d) +'\td\n'+ 
                      'Obser_'+str(i)+'_'+str(j) +'\t'+ str(best_e) +'\te\n'+
                      'Obser_'+str(i)+'_'+str(j) +'\t'+ str(-l_walk[max_likelihood_id]) +'\tLikelihood\n')    
        fileout.close()
