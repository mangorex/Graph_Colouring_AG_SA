# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Modified on Wed Jun 20 16:28:47 2018

@author: Manuel Atnonio Gómez Angulo. Damián Serrano Fernández
Tutora: Antonia M. Chávez González

INCLUYE ALGORITMO GENETICO HIBRIDO CON ENFRIAMIENTO SIMULADO
Incluye 6 funciones que forman el ALGORITMO GENETICO. Son las siguientes:
    1) generarPoblacionInicialAleatoria
    2) evolucion  Llama a encuentraIndividuoMasFitness y actualizaPoblacion
    3) actualizaPoblacion  Llama a seleccionarPadres, a operadorGeneticoSpc y
        a operadorEnfriamientoSimulado
    4) seleccionarPadres
    5) operadorGeneticoSpc  Realiza cruzamiento simple a dos padres y devuelve
        dos hijos.
    6) encuentraIndividuoMasFitness

Incluye 1 función de ENFRIAMIENTO SIMULADO.
    1) operadorEnfriamientoSimulado. Realiza enfriamiento simulado
        a uno de los hijos del cruzamiento de dos padres.
    
CLASE PARA REPRESENTAR EL GRAFO MapaGrafo. Funciones:
    1) __init__   Inicializa el grafo con los parámetros
    2) __convert_to_nxgraph  Crea el grafo con colores y número de vértices,
        y calcula fitness
    3) print_me  Imprime el grafo

    FUNCIONES AUXILIARES:
    
    1) opcionInstancia  Llama a generarGrafoConListaAdyacencia si la lista de
        adyacencias no está vacía, o llama a generarGrafoAleatorio en caso
        contrario y devuelve lista de adyacencias.
    2) generarGrafoConListaAdyacencia  Genera grafo (sin colores, ni número de 
        vercices) con numero de nodos y lista de adyacencias
    generarGrafoAleatorio con número de nodos y probabilidad de eje.
    3) visualize_results  realiza la visualización del grafo llamando a print_me
        de clase MapaGrafo.
        
    Bibliografía aquí
        stackoverflow.com
        http://instaar.colorado.edu/~jenkinsc/carboClinic/_carboCELL/Docs/colors.py.htm
        https://networkx.github.io/documentation/networkx-1.10/tutorial/tutorial.html
        https://github.com/jankrepl/Graph_Colouring
        http://webdiis.unizar.es/asignaturas/APD/wp/wp-content/uploads/2013/09/151201simulatedAnnealing2.pdf
        
"""
# In[313]:

import networkx as nx # Libreria para generar grafos
# Numpy es un paquete fundamental para la ciencia de la computacion en python
import numpy as np
from math import exp # Librería para expresiones matemáticas. Usada en el segundo if de enfriamiento simulado
import random # Librería de generación de números aleatorios
import matplotlib.pyplot as plt  # Librería para dibujar gráficos


# In[316]:


# Definición de estructura principal
class MapaGrafo:
    def __init__(self, colores, listaAdyacencia):
        """
        colores: Cadenas de 'r', 'g, 'b', y o 'm' - Ejemplo 'rbbgrgbg'
        :tipo colores: str
        listaAdyacencia: lista de adyacencia - lista de vecinos para
            cada nodo
        :tipo listaAdyacencia: lista de listas
        """
        # Atributos de la clase:
        # Cadena.. individuo q representa los 5 posibles colores 
        # 'r' (red), 'g' (grenn), 'b' (blue), 'y' (yellow) y 'm' (magenta)
        self.colores = colores
        self.listaAdyacencia = listaAdyacencia  # lista de listas
        self.numNodos = len(self.colores)
        self.fitness, self.graph_nx = self.__convert_to_nxgraph(
                self.colores, self.listaAdyacencia)
        # Fin de atributos de la clase
        
        
    # Usamos el paquete networkx para las funcionalidades de visualizacion
    # del grafo
    def __convert_to_nxgraph(self, colores, listaAdyacencia):
        """
        Los COLORES están definidos en la librería MATPLOTLIB de python.
        Para más información 
        http://instaar.colorado.edu/~jenkinsc/carboClinic/_carboCELL/Docs/colors.py.htm
        colores: 'r', 'g, 'b', y o 'm'. - Ejemplo 'rbbgrgbg'
        :tipo colores: str
        listaAdyacencia: lista de adyacencia - lista de vecinos para
        :tipo listaAdyacencia: lista de listas
        :return: (fitness, objeto de grafo networkx)
        :rtipo: (int, Grafo netowrkx)
        """
        G = nx.Graph() # Creamos el grafo vacio
        contEjesConectadosMismoColor = 0  # Contador del numero de ejes del mismo color
        numeroEjesDoble = 0

        # Recorre los colores y crea un indice y coge un color del enumerado
        # Ejemplo 'rbbgrgbg': 
        # 1 r El nodo 1 v a ser rojo
        # 2 b El nodo 2 va a ser azul
        # El enumerado colors llega hasta el numero de nodos que le pusimos como parametro
        # y cada nodo tiene un color
        for i, node_color in enumerate(colores):
            
            G.add_node(i, color=node_color)
            for vecino in listaAdyacencia[i]:
                # Añade un nodo al grafo con indice y color. add_node es 
                # funcion de liberia networks
                G.add_edge(i, vecino, illegal=False)  
                numeroEjesDoble += 1
                
                # Comprueba si los vecinos tienen el mismo color
                if  node_color == colores[vecino]:
                    # Si tienen el mismo color ese par de vecinos lo marca como 
                    # illegal, lo penaliza. Penalización en la resta con 
                    # contEjesConectadosMismoColor
                    G[i][vecino]['illegal'] = True
                    # Si son iguales incrementa en 1 el contador de penalizados
                    contEjesConectadosMismoColor += 1
            # fitness = numero vertices - penalizacion
            
            fitness = numeroEjesDoble / 2 - contEjesConectadosMismoColor / 2

        return fitness, G # Pasamos el fitness y el grafo

    # Imprime un grafo representando el objeto
    def print_me(self, numeroFigura=-1, tituloFigura=''):
        """
        numeroFigura: number of the figure
        :tipo numeroFigura: int
        :param tituloFigura: name of the figure
        :tipo tituloFigura: str

        """
        
        # El color de los ejes con vertices de mismo color será rojo (r)
        # El color de los ejes con vertices de distinto color sera verde (g)
        mappingColor = {True: 'r', False: 'g'}

        listaNodo = self.graph_nx.nodes(data=True)
        listaEje = self.graph_nx.edges(data=True)

        nodosColor = [element[1]['color'] for element in listaNodo]
        ejesColor = [mappingColor[element[2]['illegal']] for element in listaEje]
        plt.figure(num = numeroFigura, figsize=(10, 8), dpi=80)
        
        plt.title(tituloFigura)
        nx.draw_networkx(self.graph_nx, with_labels=True, node_color=nodosColor, edge_color=ejesColor)
        plt.draw() # Dibujar el grafo


def generarGrafoConListaAdyacencia(numNodos, listaAdyacencia):
    """
    Función que genera un grafo a partir de un número de nodos determinado
    y una lista de adyacencias determinada.
    
    numNodos: Numero de nodos del grafo
    type numNodos: int
    listaAdyacencia: lista de adyacencia
    :tipo listaAdyacencia: lista de listas
    """
    # Creacion de grafo a mano.
    # Esto solo sirve para la lista de adyacencias dada y para tres nodos
    # Habria que parametrizar
    G = nx.Graph()
    
    for i in range(numNodos):
        G.add_node(i)

    cont = 0
    for elemento1 in listaAdyacencia:
        # G.add_node(i)
        # G.add_node(1)
        for elemento2 in elemento1:
            G.add_edge(cont, elemento2)
        cont += 1
    # nx.draw(G)
    
    # Devolvemos numero de ejes y ejes
    return G.number_of_edges()


# Genera grafo aleatorio con los parametros que le indicamos. 
# Devuelve el numero de ejes y la lista de adyacencias
def generarGrafoAleatorio(numNodos, probabilidadEje):
    """

    Genera un grafo aleatorio con la probabilidad que iondicamos para generar ejes.

    numNodos: Numero de nodos del grafo
    type numNodos: int
    probabilidadEje: Probabilidad de que haya ejes entre dos nodos
    type probabilidadEje: float
    return: (number_of_edges, edges) Número de ejes y lista de adyacencias
    rtipo: (int, lista de listas) Lista con todas las listas de adyacencias
    """

    # Genera grafo aleatorio con los parametros que le indicamos. 
    # El grafo es no dirigido
    G = nx.fast_gnp_random_graph(numNodos, probabilidadEje, seed=None, directed=False)
    edges = []
    
    # Añade los ejes al grafo uniendo los nodos
    for i in range(numNodos):
        temp1 = G.adj[i]
        edges.append(list(G.adj[i].keys()))
    
    # nx.draw(G) # Dibuja el grafo
    return G.number_of_edges(), edges


# In[314]:    

def opcionInstancia(tamPoblacion, numNodos, probabilidadEje,
                listaAdyacencia, numGeneraciones, porcentajePadresMantener):
    """
    Función que llama a generarGrafoAleatorio en el caso de que la lista de
    adyacencias esté vacía, o llama a generarGrafoConListaAdyacencia en el
    caso contrario.
    
    tamPoblacion: tamaño población
    :tipo tamPoblacion: int
    numNodos: numero de nodos
    :tipo numNodos: int
    probabilidadEje: Probabilidad de que haya ejes entre dos nodos
    type probabilidadEje: float
    listaAdyacencia: lista de adyacencia
    :tipo listaAdyacencia: lista de listas
    numGeneraciones: número de generaciones a simular
    :tipo numGeneraciones: int
    :porcentajePadresMantener: Porcentaje de los padres con más fitness para
        transferir a la nueva generación, entre (0,1)
    :tipo porcentajePadresMantener: float
    :return: numEjes, listaAdyacencia
    :rtipo: int, lista de listas
    """
    # Si la lista de adyacencias no está vacía usamos el grafo generado
    # con la lista de adyacencias
    if( len (listaAdyacencia) != 0):
        print('\nINSTANCIA CON GRAFO GENERADO POR NOSOTROS CON LISTA ADYACENCIAS\n')
        numEjes = generarGrafoConListaAdyacencia(numNodos, listaAdyacencia)
    else: # Si la lista de adyacencias está vacía usamos grafo generado aleatoriamente
        # Generamos grafo Aleatorio con probabilidadEje
        print('\nINSTANCIA CON GRAFO GENERADO ALEATORIAMENTE\n')
        numEjes, listaAdyacencia = generarGrafoAleatorio(numNodos, probabilidadEje)
        
    return numEjes, listaAdyacencia

    
# In[315]:



# Función de ALGORITMO GENETICO QUE REALIZA LA
# Generacion aleatoria de la poblacion inicial
def generarPoblacionInicialAleatoria(
        tamPoblacion, numNodos, listaAdyacencia, numColores):
    """
    tamPoblacion: tamaño población
    :tipo tamPoblacion: int
    numNodos: numero de nodos
    :tipo numNodos: int
    listaAdyacencia: lista de adyacencia
    :tipo listaAdyacencia: lista de listas
    numColores: numero de colores
    :tipo numColores: int
    :return: poblacionInicial
    :rtipo: lista de MapaGrafo aleatoria
    """
    poblacionInicial = []

    # Generar población inicial aleatoria
    for _ in range(tamPoblacion):
        # Te genera un color para cada nodo
        if numColores == 3:
            listaColores = np.random.choice(
                    ['r', 'b', 'g'], numNodos, replace=True)
        elif numColores == 4:
            listaColores = np.random.choice(
                    ['r', 'b', 'g', 'y'], numNodos, replace=True)
        else:
            listaColores = np.random.choice(
                    ['r', 'b', 'g', 'y', 'm'], numNodos, replace=True)
        
        # Te pone la lista como una lista de caracteres
        cadenaColores = "".join(listaColores)
        # ['b' 'g' 'b' 'g' 'b' 'g' 'g' 'g' 'g'] Ejemplo de color_string
        
        # Actualiza la poblacion inicial con un mapa que es la lista de colores
        # con lista de adyacencias
        poblacionInicial.append(MapaGrafo(cadenaColores, listaAdyacencia))
    
    print('Una población inicial de ' + str(tamPoblacion) + 
          ' individuos ha sido creada')
    print()
    
    return poblacionInicial




# In[317]:




# In[318]:


# Función de ALGORITMO GENETICO que "evoluciona la población"
# Actualiza iterativamente las generaciones llamando a otras funciones de
# ALGORITMO GENETICO que realizan las siguientes cosas:
# selecciona padres y cruza padres. 
def evolucion(poblacionInicial, numGeneraciones, tamPoblacion,
                      tempIni, numColores = 3, porcentajeAMantener=0.1):
    """
    poblacionInicial: población inicial
    :tipo poblacionInicial: lista de MapaGrafo
    numGeneraciones: número de generaciones a simular
    :tipo numGeneraciones: int
    tamPoblacion: población inicial deseada - se mantiene constante a
        través de algoritmo genético
    :tipo tamPoblacion: int
    tempIni: temperaturaInicial
    :tipo tempIni: int
    numColores: numero de colores
    :tipo numColores: int
    porcentajeAMantener:  porcentaje de padres con más fitness 
        a transferir en una nueva generación, entre (0, 1)
    :tipo porcentajeAMantener: float
    :return: (para cada generación lista de fitness de cada individuo,
              para cada generacionón los individuos con más fitness)
    :rtipo: (lista de listas, lista de MapaGrafo)
    """
    resultadosFitness = []
    resultadosIndividuosMasFitness = []
    
    for i in range(numGeneraciones):
        print('Tu población está en la generación ' + str(i + 1))
        
        # Actualiza la población inicial
        poblacionDeSalida = actualizaPoblacion(poblacionInicial, tamPoblacion,
                                              tempIni, numColores,
                                              porcentajeAMantener =
                                              porcentajeAMantener)
        poblacionInicial = poblacionDeSalida

        # Guardar resultados
        # El \ es sólo para que funcione el salto de línea
        listaFitness, indiceIndividuoMasFitness, coloreadoConMasFittness = \
            encuentraIndividuoMasFitness(poblacionInicial)
        
        resultadosFitness.append(listaFitness)
        
        resultadosIndividuosMasFitness.append(coloreadoConMasFittness)
        
        # Imprime los individuos con más fitness
        print('El individuo con más fitness es: ' + str(max(listaFitness)))
            
    return resultadosFitness, resultadosIndividuosMasFitness


# In[319]:


# FUNCION DE ALGORITMO GENETICO
# Encuentra individuos con mas fitness (fittest element)
# Dada una población, encuentra el individuo con más fitness
def encuentraIndividuoMasFitness(poblacionInicial):
    """
    :param poblacionInicial: población inicial
    :tipo poblacionInicial: lista de MapaGrafo
    :return: lista de valores fitness para la población entera,
              indice del individuo con más fitness 
              y individuo con más fitness
        
    :rtipo: (lista, int, MapaGrafo)
    """
    listaFitness = [individuo.fitness for individuo in poblacionInicial]
    indiceIndividuoMasFitness = np.argmax(listaFitness)
    
    # El \ es para que no de error el salto de linea
    # Devolvemos lista de fitness, el indice individuo mas fitness y el individuo
    # con más fitness
    return listaFitness, indiceIndividuoMasFitness, \
        poblacionInicial[indiceIndividuoMasFitness]



# FUNCION DE ENFRIAMIENTO SIMULADO.
# Aplica enfriamiento simulado a uno de los hijos resultantes
# del cruzamiento de dos padres.
def operadorEnfriamientoSimulado(hijo, contSA, tempIni, numColores):
    """
    Bibliografía: http://webdiis.unizar.es/asignaturas/APD/wp/wp-content/uploads/2013/09/151201simulatedAnnealing2.pdf
    hijo
    :tipo: Objeto de mapa grafo. Primer individuo resultante de cruzamiento de
        padres.
    contSA: Contador de veces que entra en el segundo if de enfriamiento 
        simulado. Contra más veces entre peor solución. Según la teoría de
        nuestro pdf, Las malas soluciones contribuyen a hacer una búsqueda más extensiva,
        de tal forma que baja las probabilidades de aceptar malas soluciones.
    :tipo: int
    tempIni: Temperatura inicial
    :tipo: int
    numColores: numero de colores
    :tipo numColores: int
    :return: s y contSA
    :rtipo: MapaGrafo con enfriamiento simulado aplicado e int
    """
    
    # Enumaremos los puntos de la página 9 de nuestra fuente de SA.
    pruebas = 10
    maxIteraciones = 10
    kb = tempIni
    temp = tempIni
    s = hijo # PUNTO 1. Inicialización. Solución que cogemos del cruzamiento del AG.
    decTempIni = tempIni/100
    
    for k in range(1, pruebas):
        for j in range(1, maxIteraciones):
           
            
            # INICIO Generar un vecino s' aleatorio de s
            # PUNTO 2. Movimiento. Perturbar la solución con algún tipo de movimiento
            # Te genera un color para cada nodo
            if numColores == 3:
                listaColores = np.random.choice(
                        ['r', 'b', 'g'], hijo.numNodos, replace=True)
            elif numColores == 4:
                listaColores = np.random.choice(
                        ['r', 'b', 'g', 'y'], hijo.numNodos, replace=True)
            else:
                listaColores = np.random.choice(
                        ['r', 'b', 'g', 'y', 'm'], hijo.numNodos, replace=True)
            # FIN DE Generar un vecino s' aleatorio de s
            
            # Te pone la lista como una lista de caracteres
            cadenaColores = "".join(listaColores)
            
            sPrima = MapaGrafo(cadenaColores, s.listaAdyacencia)
            # En nuestro algoritmo genetico contra mas grande sea el fitness mejor solución
            # En enfriamiento simulado contra mas chico sea la energia mejor solucion
            # Por eso la energia es un número grande menos el fitness
            energiaS = 100 - s.fitness
            energiaSPrima = 100 - sPrima.fitness
            
            # PUNTO 3. Evauluar. Calcular la variación de la puntuación (energía)
            if energiaS >= energiaSPrima:
                s = sPrima # PUNTO 5. Actualizar
            else:
                # PUNTO 4. Elegir dependiendo del resultado de la evaluación 
                # aceptar o rechazar (primer if del PUNTO 3).
                # Aceptar una solución mala con probabilidad variante. Eso
                # es cuando entra en el if. La probabilidad varía porque varía la
                # energía de s, energiaSprima, temp y hay un número aleatorio.
                if ( exp( (energiaS - energiaSPrima) ) / (kb * temp) ) > random.random():
                # if ( exp( (energiaS - energiaSPrima) / (kb * temp) )) > random.random():
                    s = sPrima # PUNTO 5. Actualizar
                    contSA += 1
            
            # PUNTO 5 Actualizar y repetir. Reducir el valor de la temperatura.
            # Se actuliza el individuo dentro de los dos if si entran.
            # La repetición está en los dos for, con lo cual volvemos al paso 2.
            temp -= decTempIni
            
    return s, contSA     
    
    
# In[320]:


""" FUNCION DE ALGORITMO GENETICO que Actualiza la población.
 Llama a función de ALGORITMO GENETICO seleccionarPadres, que se encarga de
 seleccionar a los padres y también llama a Función de ALGORITMO GENETICO
 operadorGeneticoSpc, que se encarga de realizar los cruzamientos de los 
 padres.
 También llama a la única función de ENFRIAMIENTO SIMULADO operadorEnfriamientoSimulado
 que se encarga de realizar enfriamiento simulado a uno de los hijos del cruzamiento de padres.
 El hijo1, después de actulizarse o no, se agrega a la nueva población.
 El hijo 2 resultante del cruzamiento de padres, al cual no se le aplica enfriamiento simulado,
 se agrega a la nueva población tal como salió despues del cruzamiento.
"""
def actualizaPoblacion(poblacionInicial, tamPoblacionDeSalida, tempIni,
                       numColores = 3, porcentajeAMantener=0.1):
    """
    poblacionInicial: población inicial
    :tipo poblacionInicial: lista de MapaGrafo
    tamPoblacionDeSalida: tamaño de población de salida
    tamPoblacionDeSalida: int
    tempIni: temperaturaInicial
    :tipo tempIni: int
    numColores: numero de colores
    :tipo numColores: int
    :porcentajeAMantener: Porcentaje de los padres con más fitness para
        transferir a la nueva generación, entre (0,1)
    :tipo porcentajeAMantener: float
    :return: poblacionDeSalida
    :rtipo: list of MapaGrafo
    """
    tamPoblacionDeEntrada = len(poblacionInicial)
    poblacionDeSalida = []

    #  Nosotros mantenemos el mejor porcentaje porc de poblacion inicial
    # Ordenamos la población por fitness
    poblacionInicial.sort(key=lambda porc: porc.fitness, reverse=True)
    
    # La \ es para que no de error el salto de linea
    # Cogemos de poblacionDeSalida desde el elemento 0 hasta el elemento
    #tamPoblacionDeEntrada * porcentajeAMantener
    # Ejemplo si tamPoblacionDeEntrada es 50 y porcentajeAMantener es 0'2
    # nos quedamos con 50 * 0'2 = 10, 10 elementos de poblacion Inicial
    poblacionDeSalida += poblacionInicial \
        [:int(tamPoblacionDeEntrada * porcentajeAMantener)]
            
    # Llamamos a la funcion seleccionarPadres, le pasamos la población
    # inicial y el número de parejas (tamPolacionEntrada//2)
    # El // quiere decir que es dividir entre dos y redondear a un numero
    # entero. No puede haber 10'5 parejas. Habría 10
    listaDeParejasDePadres = seleccionarPadres \
        (poblacionInicial, tamPoblacionDeEntrada // 2)

    indicePareja = 0
    contSA = 0
    # Recorremos la poblacion de Salida entera
    # En este bucle se recorre la poblacion de salida
    # desde la longitud de poblacion Salida hasta el tamaño de poblacionSalida
    # Por cada iteracion se cruzan dos padres y se devuelven 2 hijos.
    # Hijos que se añadiran a la población de salida.
    # Al añadir 2 hijos por cada iteración, si el tamaño de poblacion
    # son 50 y empezamos con longitud de poblacion Salida 10
    # sea añadirían 40 poblaciones, hasta llegar a 50 (tamPoblacionDeSalida) 
    while len(poblacionDeSalida) < tamPoblacionDeSalida:
        # Llamamos a funcion para cruzar los padres.
        # Le pasamos la lista de Parejas de Padres con su indice
        # Nos devuelve dos hijos (es lo que hace el cruzamiento simple)
        hijo1, hijo2 = operadorGeneticoSpc(listaDeParejasDePadres[indicePareja])
        
        # ¿Va dentro del bucle simulated annealing aqui?
        
        # Añadimos el hijo 1 y 2 a la población de salida
        # Llamada al algoritmo enfriamiento simulado
        hijo1, contSA = operadorEnfriamientoSimulado(
                hijo1, contSA, tempIni, numColores)
        hijo2, contSA = operadorEnfriamientoSimulado(
                hijo2, contSA, tempIni, numColores)
        poblacionDeSalida.append(hijo1)
        poblacionDeSalida.append(hijo2)
        indicePareja += 1

    print("   En esta generación entrado "+ str(contSA) +
          " veces en el segundo if de enfriamiento simulado")
    return poblacionDeSalida # Devolvemos la población de salida


# In[321]:


# FUNCION DE ALGORITMO GENETICO
# Crea lista de pares de padres desde población inicial
def seleccionarPadres(poblacionInicial, numeroDePares):
    
    """
    poblacionInicial:
    :tipo poblacionInicial: lista de MapaGrafo
    numeroDePares:numero de salida de pares de padres. 
        -> poblacionDeSalida = 2 * numeroDePares
    :tipo numeroDePares: int
    :return: Padres emparejados de población inicial
    :rtipo: lista de pares de MapaGrafo
    """

    longPoblacionInicial = len(poblacionInicial) # Longitud de poblacionInicial

    # Usamos selección proporcional de fitness
   
    # fitness_sum es la suma del fitness de todos los individuos de poblacionIinicial
    fitness_sum = sum([individuo.fitness for individuo in poblacionInicial])
    
     # Nuestro fitness no es negativo, así que podemos aplicar una simple fórmula
    # fitness_m / sum (fitness_i)
    # probabilidadSeleccion es una lista de numeros, la cual expresa la
    # probabilidad de que cada inidividuo sea elegido para ser seleccionado
    # como padres. Esta ordenado de mayor a menor
    lprobabilidadSeleccion = np.array([individuo.fitness / fitness_sum for individuo in poblacionInicial])
    
    # Información np.arange https://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html
    # np.arange genera números desde el 0 hasta longPoblacionInicial. Ejemplo de 0 a 50. 0 1 2 3 4 5 ... 50
    # Información np.random.choice https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.choice.html
    # Selecciona un elemento al azar de 0 a 50 de tamaño 25
    I_x = np.random.choice(np.arange(0, longPoblacionInicial), numeroDePares, p=lprobabilidadSeleccion)
    I_y = np.random.choice(np.arange(0, longPoblacionInicial), numeroDePares, p=lprobabilidadSeleccion)

    # Devolvemos los pares de padres para todos los numeroDePares de padres
    return [(poblacionInicial[I_x[i]], poblacionInicial[I_y[i]]) for i in range(numeroDePares)]


# In[322]:


# FUNCION DE ALGORITMO GENETICO
# Función operador Genetico SPC- Single point crossover (Cruzamiento simple)
# Dado un par de padres se devuelve como salida un par de hijos.
    
def operadorGeneticoSpc(parDePadres):
    """

    parDePadres: par de padres
    :tipo parDePadres: par de MapaGrafo
    :return: par de hijos
    :rtipo: par de MapaGrafo
    """

    numNodos = parDePadres[0].numNodos
    listaAdyacencia = parDePadres[0].listaAdyacencia

    # Step 1) Select a random point
    # Step 2) All colours to the left will be from parent 1, all parent to the right are from parent 2
    point = np.random.randint(0, numNodos)

    # REVISAR CAMBIO. Creo que coloresPadre1 sería parDePadres[1]
    # REVISAR. ¿Es posible tener dos padres iguales en el par?
    coloresPadre1 = parDePadres[0].colores
    coloresPadre2 = parDePadres[1].colores # Sería el segundo elemento de parDePadres.

    # Cruzamos los padres 1 y dos para obtener dos hijos
    coloresHijo1 = coloresPadre1[:point] + coloresPadre2[point:]
    coloresHijo2 = coloresPadre2[:point] + coloresPadre1[point:]

    # Devolvemos un MapaGrafo con cada hijo.
    # Por cada MapaGrafo le pasamos los colores y la lista de adyacencia
    return (MapaGrafo(coloresHijo1, listaAdyacencia),
            MapaGrafo(coloresHijo2, listaAdyacencia))


# In[324]:



# Visualizar los resultados del algoritmo genético
def visualize_results(resultadosFitness, resultadosIndividuosMasFitness):
    """
    resultadosFitness: Todos los fitness de cada individuo por cada 
        generacion
    :tipo resultadosFitness: lista de listas
    resultadosIndividuosMasFitness:
        Individuo con más fitness para cada generación
    :tipo resultadosIndividuosMasFitness: lista de MapaGrafo
    :return: Imprime el individuo (grafo) con más fitness de todas
        las generaciones. Si hay empate coge el que tenga la generación menor.
        Ejemplo. Si el fitness máximo es 15 y lo tiene la generación 4 y 5,
        nos devuelve el individuo de la generación 4
    """
    cont = 0
    maxFitness = 0 # Comenzamos con un maximo de fitness de 0
    posMax = 0
    
    # Esto es un algoritmo de búsqueda simple
    # Recorremos todos los individuos con mas fitness de cada generación
    for i in resultadosIndividuosMasFitness:
        # Si el fitness del inviduo del indice i es mayor que maxFitness
        if i.fitness > maxFitness:
            maxFitness = i.fitness # El max fitness es el del individuo i
            posMax = cont # La posición del maximo es la del individuo con maxFitness
        cont = cont + 1

    print ("\nPosición del individuo de lista resultadosIndividuosMasFitness " + \
           "con más fitness: " + str(posMax) ) # Imprimimos por pantalla la posición
    # Imprimimos por pantalla como texto el individuo ocn mas fitness
    print ("Máximo fitness de todas las generaciones: " + \
           str(resultadosIndividuosMasFitness[posMax].fitness) ) 
    # Imprimimos como grafo el individuo con mas fitness de todas las
    # generaciones
    resultadosIndividuosMasFitness[posMax].print_me(
            numeroFigura=posMax, tituloFigura='generation: ' + str(posMax + 1) 
            + ', fitness: ' + 
            str(resultadosIndividuosMasFitness[posMax].fitness))

    return str(resultadosIndividuosMasFitness[posMax].fitness)