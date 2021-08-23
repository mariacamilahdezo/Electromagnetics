#!/usr/bin/env python
# coding: utf-8

# # Simulación capacitor de placas paralelas en 2D

# Primer laboratorio para la materia de Electromagnetismo, Ingeniería Física. Vanessa Restrepo Velásquez y Maria Camila Hernández Ortiz. Medellín, Colombia. 2020

# In[ ]:


'''
Electromagnetismo: "Evolución al estado estacionario" del potencial eléctrico en un capacitor de placas paralelas, 
con dimensiones La:33mm y An:3mm.
Vanessa Restrepo Velásquez y Maria Camila Hernández Ortiz
Agosto 14/2020

'''
#Llamado de librerías necesarias para el código
import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# In[ ]:


#Segunda aproximación matriz de 132x3400, las placas con potenciales de 100 y -100, 
#CON las dimensiones indicadas de la placa real (Ancho:30celdas=3mm y Largo:3300celdas=330mm)
#donde cada celda equivale a 100 micras.
'''
Obtención de la matriz de estado (semi) estacionario para el potencial eléctrico:

'''
phi=np.zeros((132,3400)) #Matriz phi de Potenciales eléctricos
phi1=np.zeros((132,3400))#Matriz phi1 de Potenciales eléctricos
phi2=np.zeros((132,3400))#Matriz phi2 de Potenciales eléctricos

for i in range(50,3350):#Asignación de valores fijo de potencial eléctrico en la placa superior
    phi[50,i]=100
    phi1[50,i]=100  
    
for i in range(5,3350):#Asignación de valores fijo de potencial eléctrico en la placa inferior
    phi[81,i]=-100
    phi1[81,i]=-100
erphi=1e-2 #Diferencia mínima del código punto a punto, entre dos matrices consiguientes

#Inicio del ciclo FOR para las iteraciones del potencial, evitando cambios en las placas
for n in range (0,10000):
    for i in range(1,131):
        for j in range(1,3399):
            if (i==50 or i==81) and (50<=j<=3350): pass
            else:
                phi1[i,j]=(phi[i+1,j]+phi[i-1,j]+phi[i,j+1]+phi[i,j-1])*0.25#Contrucción de la nueva matriz de potenciales
                
    #Se entra al condicional si el error es menor o igual a erphi
    if np.max(np.fabs(phi2-phi1))<=erphi:
        print('Última iteración:', n)#Se imprime la última iteración
        print(np.max(np.fabs(phi2-phi1)))
        print('Gráficos de contorno para el potencial y el campo eléctrico de un capacitor de placas paralelas:')
        #print ("phi estado estacionario:", phi1) #Puede imprimirse la última matriz en estado estacionario...(potencial a ese erphi)
        Pot=phi1 #Se extrae la matriz de potenciales (E. estacionario)
        break
        
    #Se realiza una reasignación para que la matriz phi1 vuelva a estar vacía.    
    phi=phi1
    phi2=phi1
    phi1=np.zeros((132,3400))
    for i in range(50,3350):
        phi1[50,i]=100
    for i in range(50,3350):
        phi1[81,i]=-100
     
'''
Graficación Potencial eléctrico (phi)

'''        
Pot2=Pot[:,3310:3360]#Graficación de una menor parte de la matriz, para visualizar detalles
Pot1=Pot2[40:93,:]
fig1 = plt.figure(1)
plt.figure(figsize=(15,6))
plt.contourf(Pot1, 50, origin='upper',cmap='inferno') #Gráfico de contorno para 'E'
plt.axis('image')# Ejes de la gráfica
plt.colorbar() #Barra indicativa de la representación de colores
#Labels, title...
plt.xlabel('Celdas del arreglo en (100$\\mu$ c/u)', fontsize="18")
plt.ylabel('Celdas del arreglo en y (100$\\mu$ c/u)', fontsize="18")
plt.title('Potencial eléctrico $\\phi$ en Volts', fontsize="21")#Titulo y magnitud de la 'colorbar'
plt.tick_params(labelsize="15")

'''
Obtención de la matriz de Campo Eléctrico (E), de acuerdo a la matriz de potenciales:

'''
Ey, Ex = np.gradient(Pot)  # Define los componentes del campo eléctrico
Ey, Ex = -Ey, -Ex  # Corrección de signo par el gradiente del campo
E = np.sqrt(Ex*Ex + Ey*Ey)  # Magnitud del campo eléctrico

'''
Graficación Campo eléctrico (E)

'''
E2=E[:,3310:3360] #Graficación de una menor parte de la matriz, para visualizar detalles
E1=E2[42:90,:]
fig2 = plt.figure(2)
plt.figure(figsize=(15,6))
plt.contourf(E1, 50, origin='upper',cmap='inferno') #Gráfico de contorno para 'E'
plt.axis('image')# Ejes de la gráfica
plt.colorbar() #Barra indicativa de la representación de colores
#Labels, title
plt.xlabel('Celdas del arreglo en (a.u)', fontsize="18")
plt.ylabel('Celdas del arreglo en y (a.u)', fontsize="18")
plt.title('Campo Eléctrico E(a.u)', fontsize="21")
plt.tick_params(labelsize="15")
#plt.streamplot(E, Ex, Ey, v, color='m')  # Dirección del campo eléctrico
plt.show()

Potpy=Pot[50:82,1650] #Datos de la linea media vertical del capacitor Python
#Datos linea media vertical COMSOL
Potcom=[100,99.974,92.876,85.762,78.639,71.765,64.678,57.845,50.755,42.997,35.654,27.899,21.692,14.605,7.836,0.855,0.102,-7.132,-14.381,-21.775,-28.002,-35.754,-42.201,-49.100,-56.523,-63.723,-70.176,-78.003,-85.156,-92.684,-99.894,-100]
#Ajuste lineal y comparación de datos en la linea media vertical del capacitor
def f(x,a,b):
    return a*x+b
x=np.arange(0,32)
init_values=[-1,1]
best_values, covariance=curve_fit(f,x,Potpy,p0=init_values)

plt.figure(figsize=(10,6))
plt.plot(x,f(x,best_values[0],best_values[1]), "k-",label="Ajuste lineal para el modelo python", linewidth="2")
plt.plot(Potpy, "b-", label="Potencial en python", linewidth="2")
plt.plot(Potcom,"r-", label="potencial en COMSOL", linewidth="2")
plt.legend(loc="upper right", fontsize="16")
plt.xlabel('Celdas en la línea vertical', fontsize="18")
plt.ylabel('Potencial eléctrico (V)', fontsize="18")
plt.title('Potencial en la línea vertical media de las placas', fontsize="21")
plt.tick_params(labelsize="15")
plt.grid()
print(best_values)
print(np.sqrt(np.diag(covariance)))
plt.show()

