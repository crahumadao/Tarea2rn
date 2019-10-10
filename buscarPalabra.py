import numpy as np
import nltk
import matplotlib.pyplot as plt
from AlgoritmoGenetico import AlgoritmoGenetico

# Búsqueda de una palabra a partir de los ejemplos.

# Genes del problema son las letras del abecedario.
genes_disponibles = {0: 'a',
                     1: 'b',
                     2: 'c',
                     3: 'd',
                     4: 'e',
                     5: 'f',
                     6: 'g',
                     7: 'h',
                     8: 'i',
                     9: 'j',
                     10: 'k',
                     11: 'l',
                     12: 'm',
                     13: 'n',
                     14: 'ñ',
                     15: 'o',
                     16: 'p',
                     17: 'q',
                     18: 'r',
                     19: 's',
                     20: 't',
                     21: 'u',
                     22: 'v',
                     23: 'w',
                     24: 'x',
                     25: 'y',
                     26: 'z',
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


# Seteo de parámetros para el GA.
tamano = len('palabra')
np.random.seed(42)
poblacion = 100
puntaje = (lambda x: nltk.edit_distance(x, 'palabra'))
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


