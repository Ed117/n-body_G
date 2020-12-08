# -*- coding: UTF-8 -*-

import constantes
from integrador import euler_step
import scipy as sp
import numpy as np
import scipy.constants
import matplotlib.pyplot as plt
from calculos import calcula_energia_total
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

# inicializacion de condiciones iniciales


visualizacion = "animado"

dt = 60. * 60.

# Condiciones iniciales

# Lista de cuerpos que componen el sistema
cuerpos =   [   {   'masa': constantes.MASA_SOL*1.09,
                    'posicion': np.array([-10.9 * sp.constants.astronomical_unit, 0, 0]),
                    'velocidad': np.array([0, 2.1E3, 0]),
                    'nombre': "Estrella A",
                    'color': 'r.'},
                {   'masa': constantes.MASA_SOL*0.9,
                    'posicion': np.array([10.9 * sp.constants.astronomical_unit, 0, 0]),
                    'velocidad': np.array([0, -2.1E3, 0]),
                    'nombre': "Estrella B",
                    'color': 'r.'},
                {   'masa': constantes.MASA_TIERRA,
                    'posicion': np.array([-9.9 * sp.constants.astronomical_unit, 0, 150000]),
                    'velocidad': np.array([0, -3.1E4, 0]),
                    'nombre': "Planeta A",
                    'color': 'b.'},
                {   'masa': constantes.MASA_TIERRA,
                    'posicion': np.array([9.9 * sp.constants.astronomical_unit, 0, sp.constants.astronomical_unit]),
                    'velocidad': np.array([0, -3.1E4, 0]),
                    'nombre': "Planeta B",
                    'color': 'b.'},
                {   'masa': constantes.MASA_TIERRA,
                    'posicion': np.array([0, 0, 7.9 * sp.constants.astronomical_unit]),
                    'velocidad': np.array([-4.1E3, 0, -2.1E3]),
                    'nombre': "Planeta D",
                    'color': 'b.'},
                {   'masa': constantes.MASA_TIERRA,
                    'posicion': np.array([0, 0, -7.9 * sp.constants.astronomical_unit]),
                    'velocidad': np.array([4.1E3, 0, 2.1E3]),
                    'nombre': "Planeta D",
                    'color': 'b.'}
            ]

# 50 años
steps = 366 * 30 * 100
guarde_cada = 300

# Listas en memoria para guardar todos los datos de la evolución para luego graficarlos.
archivo = []
time = 0

# Guardamos la energia total al inicio de la simulación
# para verificar que al final el sistema conserve la energía
etot_inicial = calcula_energia_total(cuerpos)

while steps >= 0:
    euler_step(cuerpos, dt)
    # Mensaje para ir viendo el avance del proceso
    if steps % 1000 == 0:
        print("Faltan " + str(steps) + " steps ")

    # En cada paso, guardamos los valores de posición y velocidad para graficarlos al final

    if steps % guarde_cada == 0:

        for i in range(0, len(cuerpos)):

            # cuerpo, x, y, z, t, vx, vy, vz, m(masa)
            archivo.append([i, cuerpos[i]['posicion'][0], cuerpos[i]['posicion'][1], cuerpos[i]['posicion'][2], cuerpos[i]['velocidad'][0], cuerpos[i]['velocidad'][1], cuerpos[i]['velocidad'][2], time, cuerpos[i]['masa']])

        time = time + 1
    steps -= 1

etot_final = calcula_energia_total(cuerpos)
print("Energia total inicial: " + str(etot_inicial))
print("Energia total final: " + str(etot_final))

np_archivo = np.asarray(archivo)
np.savetxt("posiciones.csv", np_archivo, header="cuerpo, x, y, z, vx, vy, vz, t, masa", delimiter=",")



fig = plt.figure("Alfa Centauri")

ax = plt.axes(projection='3d')

# Dibujo el origen de coordenadas. Ejercicio: centro de masa del sistema
ax.plot([0], [0], [0], 'g+')

plot, = ax.plot([], [], [], 'r.')

ax.set_xlim(-15 * sp.constants.astronomical_unit, 15 * sp.constants.astronomical_unit)
ax.set_ylim(-15 * sp.constants.astronomical_unit, 15 * sp.constants.astronomical_unit)
ax.set_zlim(-15 * sp.constants.astronomical_unit, 15 * sp.constants.astronomical_unit)

def update(i):

    x_pre = []
    y_pre = []
    z_pre = []

    for elemento in archivo:
        if elemento[7] == i :
            x_pre.append(elemento[1])
            y_pre.append(elemento[2])
            z_pre.append(elemento[3])

    x = np.array(x_pre)
    y = np.array(y_pre)
    z = np.array(z_pre)

    plot.set_data(x, y)
    plot.set_3d_properties(z)
    return plot,

# Creacion de la animación, 100 frames signifca que cada 100 ms
# llama a update con un valor entre 0 y 99
# Con repeat = False hace que solo se dibujen los frames una vez
ani = animation.FuncAnimation(fig, update, frames=time, interval=20, repeat=True)
plt.show()
