# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 17:53:17 2020

@author: Maria Camila Hernández Ortiz y Vanessa Restrepo Velásquez 
"""
 # # Simulación de un Radome con el método FDTD (Diferencias Finitas) en 1D
# Segundo laboratorio de Electromagnetismo, Ingeniería Física


#Importar librerias
import numpy as np
from math import pi, sin
from matplotlib import pyplot as plt


#Definicion de variables
ke = 300 #Número de interacciones en el tiempo (pasos en el tiempo)
ex = np.zeros(ke) #Vectores que contiene el campo eléctrico 
hy = np.zeros(ke) #Vectores que contiene el campo magnético

# Simulacion con FDTD en 1D
ddx = 0.001 # Esta en m 
dt = ddx / 6e8 # Tamaño del paso en el tiempo (Tamaño de celda)
freq_in = 10.0e9 #Frecuencia (10-10,5Ghz)

boundary_low = [0, 0] #Matriz 
boundary_high = [0, 0]

# Creación del Material 
cb = np.ones(ke)  
cb = 0.5 * cb
cb_start = 100 #Inicio del vector 
cb_finish=220  #Fin del vector 
epsilon = 12   #Epsilon del material 
cb[cb_start:cb_finish] = 0.5 / epsilon #longitud del material 12cm

#Creación de las películas 1  
cb_start_1 = 95
cb_finish_1 = 100
epsilon_1 = 2 
cb[cb_start_1:cb_finish_1] = 0.5 / epsilon_1 #Longitud de la pelicula 

#Creación de las películas 2 
cb_start_2 = 220
cb_finish_2 =225
epsilon_2= 2 
cb[cb_start_2:cb_finish_2] = 0.5 / epsilon_2 #Longitud de la pelicula 

nsteps = 1500

# Frontera absorbente
 

# Seguimiento de los puntos deseados para trazar
plotting_points = [
{'num_steps': 150
, 'data_to_plot': None, 'label': ''},
{'num_steps': 1500, 'data_to_plot': None, 'label': 'Posición x(m) FDTD cells'}
]

# Loop FDTD
for time_step in range(1, nsteps + 1):
 # Calcular el campo eléctrico
    
 for k in range(1, ke):
  ex[k] = ex[k] + cb[k] * (hy[k - 1] - hy[k])
  
 # Poner una sinusoidal en el extremo inferior
 pulse = sin(2 * pi * freq_in * dt * time_step)
 ex[5] = pulse + ex[5]
 
 # Condiciones de contorno
 ex[0] = boundary_low.pop(0)
 boundary_low.append(ex[1])
 ex[ke - 1] = boundary_high.pop(0)
 boundary_high.append(ex[ke - 2])
 
 # Calcular el campo magnético
 for k in range(ke - 1):
  hy[k] = hy[k] + 0.5 * (ex[k] - ex[k + 1])
  
  # Guarde los datos en ciertos puntos para su posterior trazado
 for plotting_point in plotting_points:
  if time_step == plotting_point['num_steps']:
   plotting_point['data_to_plot'] = np.copy(ex)
   
   # Gráfica de las salidas 
plt.rcParams['font.size'] = 12
fig = plt.figure(figsize=(8, 3.5))

def plot_e_field(data, timestep, epsilon, cb, label):
  """Plot of E field at a single time step"""
  plt.plot(data, color='k', linewidth=1)
  plt.ylabel('E$_x$ (V/m))', fontsize='14')
  plt.xticks(np.arange(0, ke-1, step=20))
  plt.xlim(0, ke-1)
  plt.yticks(np.arange(-1, 1.2, step=1))
  plt.ylim(-1.2, 1.2)
  plt.text(50, 0.5, 'T = {}'.format(timestep),
       horizontalalignment='center')
  
  plt.plot((0.5 / cb - 1) / 3, 'b--', linewidth=0.75)
  
  
  # Matemáticas para escalar
  plt.text(170, 0.5, 'Eps = {}'.format(epsilon),
  horizontalalignment='center')
  plt.xlabel('{}'.format(label))

# Grafica del campo E en cada uno de los pasos de tiempo guardados anteriormentePlot the E field at each of the time steps saved earlier
for subplot_num, plotting_point in enumerate(plotting_points):
 ax = fig.add_subplot(2, 1, subplot_num + 1)
 plot_e_field(plotting_point['data_to_plot'],
     plotting_point['num_steps'], epsilon, cb,
     plotting_point['label'])
 
plt.subplots_adjust(bottom=0.2, hspace=0.45)
plt.show()