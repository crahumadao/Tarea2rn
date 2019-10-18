import numpy as np
import nltk
import matplotlib.pyplot as plt
from AlgoritmoGenetico import AlgoritmoGenetico
from generaLaberinto import divide_mapa,  genera_laberinto


# Búsqueda de ruta óptima (distancia) de salir de laberinto.
# Genes del problema son las letras del abecedario.
genes_disponibles = {0: 'Stop',
                     1: 'E',
                     2: 'N',
                     3: 'O',
                     4: 'S',
                     }


# La generación de genes es una letra del abecedario al azar.
def generagen_(genes_disponibles):
    gen = genes_disponibles[np.floor(len(genes_disponibles) * np.random.random())]
    return gen


# La generación de individios a partir del largo, genera un individuo con letras al azar del tamaño correspondiente-
def generaind_(tamano, generagen):
    individuo = ''
    for i in range(tamano):
        aux = generagen()
        individuo += aux
    return individuo


def puntaje_ruta(indivduo, base_mapa, coord_entrada, coord_salida):
    coord_actual = coord_entrada
    for direccion in indivduo:
        if direccion == 'E':
            coord_actual[0] += 1
        elif direccion == 'N':
            coord_actual[1] += 1
        elif direccion == 'O':
            coord_actual[0] -= 1
        elif direccion == 'S':
            coord_actual[1] -= 1


puntaje = (lambda x: nltk.edit_distance(x, 'palabra'))
# Seteo de parámetros para el GA.
tamano = len('palabra')
np.random.seed(42)
poblacion = 100

generagen = (lambda: generagen_(genes_disponibles))
generaind = (lambda x: generaind_(10, x))

# Construcción del algoritmo para este caso.
GA = AlgoritmoGenetico(poblacion, puntaje, generagen, generaind, tasa_mutacion=0.01, cond_ter=100, prop=0.05,
                       met_sel=True, maximo=False)
# (poblacion, puntaje, generagen, generaind, tasa_mutacion=0.2, cond_ter=500, met_sel=True, maximo=True, cov=False,
# prop= 0.02)

mi, pmi, historia = GA.evoluciona()

n = 0
prom_puntajes = []
for i in historia:
    n += 1
    lista_puntajes = list(i.values())
    prom_puntajes.append(np.mean(lista_puntajes))
    print('Puntaje promedio: {}, Máximo: {}, Mínimo: {}. En iteración {}'.format(np.mean(lista_puntajes),
                                                                                 max(lista_puntajes),
                                                                                 min(lista_puntajes), n))

plt.plot(prom_puntajes)
plt.ylabel('Distancia de Levensthein promedio')
plt.xlabel('Generación')
plt.savefig('Distancia_Generacion.png')
plt.show()


