import numpy as np


class AlgoritmoGenetico:

    #  Constructor del algoritmo genético, setea las funciones de puntajes generacion de genes e individuos.
    def __init__(self, poblacion, puntaje,
                 generagen, generaind, tasa_mutacion=0.2,
                 cond_ter=500, met_sel=True, maximo=True, cov=False, prop= 0.02):
        self.poblacion = poblacion
        self.puntaje = puntaje
        self.generagen = generagen
        self.generaind = generaind
        self.generaind = generaind
        self.tasa_mutacion = tasa_mutacion
        self.cond_ter = cond_ter
        self.met_sel = met_sel
        self.lista_individuos = []
        self.maximo = maximo
        self.cov = cov
        self.prop = prop
        for i in range(poblacion):
            nuevo_ind = self.generaind(self.generagen)
            self.lista_individuos.append(nuevo_ind)

    # Evaluación Retorna el x% de la población con mejor puntaje y los puntajes de todos.
    def evaluacion(self, prop):
        aux_dic = dict()
        for individuo in self.lista_individuos:
            aux_dic[individuo] = self.puntaje(individuo)
        mejores = [k for k in sorted(aux_dic, key=aux_dic.get, reverse=False)]
        return mejores[:int(np.floor(prop*self.poblacion))], aux_dic

    # Selección retorna el x% de los indiviuos a competir ya sea en ruleta o en torneo.
    def seleccion(self):
        if self.met_sel:
            sum_tot = 0
            if self.maximo:
                for individuo in self.lista_individuos:
                    sum_tot += self.puntaje(individuo)
                prob = sum_tot * np.random.random()
                sum_par = 0
                for individuo in self.lista_individuos:
                    sum_par += self.puntaje(individuo)
                    if sum_par >= prob:
                        return individuo
            else:
                for individuo in self.lista_individuos:
                    sum_tot += 1/(self.puntaje(individuo))
                prob = sum_tot * np.random.random()
                sum_par = 0
                for individuo in self.lista_individuos:
                    sum_par += 1/(self.puntaje(individuo))
                    if sum_par >=prob:
                        return individuo

        else:

            nindividuos =int(np.floor(self.poblacion * self.prop))
            indices = [int(self.poblacion * np.random.random()) for ni in range(nindividuos)]

            if self.maximo:
                punt_comparacion = -1000000000000000
            else: # if minimo
                punt_comparacion = +1000000000000000

            individuo = None
            for indice in indices:
                if self.maximo:
                    if self.puntaje(self.lista_individuos[indice]) > punt_comparacion:
                        punt_comparacion = self.puntaje(self.lista_individuos[indice])
                        individuo = self.lista_individuos[indice]
                else:
                    if self.puntaje(self.lista_individuos[indice]) < punt_comparacion:
                        punt_comparacion=self.puntaje(self.lista_individuos[indice])
                        individuo = self.lista_individuos[indice]
            return individuo

    # Reproducción retorna el o los individuos que resultan de un crossOver o de una mutación.
    def reproduccion(self, individuo1, individuo2=None):
        corte = int(np.floor(len(individuo1) * np.random.random()))
        hijo1 = individuo1[0:corte] + individuo2[corte:]

        if not self.cov:
            return hijo1
        else:
            lista_nuevos_individuos = [hijo1,]
            corte = np.floor(len(individuo1) * np.random.random())
            hijo2 = individuo1[0:corte] + individuo2[corte:]
            lista_nuevos_individuos.append(hijo2)
        return lista_nuevos_individuos

    def mutacion(self, individuo):
        if np.random.random()< self.tasa_mutacion:
            cambio = int(np.floor(len(individuo) * np.random.random()))
            lista_genes_individuo = []
            for gen in individuo:
                lista_genes_individuo.append(gen)
            lista_genes_individuo[cambio] = self.generagen()
            individuo=''
            for gen in lista_genes_individuo:
                individuo += gen
            return individuo
        else:
            return individuo

    def evoluciona(self):
        # Datos por generación (tendrá individuos y sus respectivos fitness).
        datos_por_generacion = []
        for n_iteracion in range(self.cond_ter):
            mejores, evaluacion_general = self.evaluacion(0.5)

            mejor_iteracion=mejores[0]
            if n_iteracion % 5 == 0:
                print('Iteración número {}'.format(n_iteracion))
            datos_por_generacion.append(evaluacion_general)

            # CrossOver (1 solo hijo)
            nueva_lista_individuos = []
            if not self.cov:
                iters_para_repoblar = self.poblacion
            else:
                iters_para_repoblar = np.round(self.poblacion/2)
                # La Ruleta
            for n in range(self.poblacion):
                individuo1 = self.seleccion()
                individuo2 = self.seleccion()
                nueva_lista_individuos.append(self.reproduccion(individuo1, individuo2))
            self.lista_individuos = nueva_lista_individuos

            # Mutaciones.
            for indice in range(self.poblacion):
                aux = self.mutacion(self.lista_individuos[int(indice)])
                self.lista_individuos[indice] = aux
        mejores, evaluacion_general = self.evaluacion(1)
        mejor_iteracion = mejores[0]
        return mejor_iteracion, self.puntaje(mejor_iteracion), datos_por_generacion
