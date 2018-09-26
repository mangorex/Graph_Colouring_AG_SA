# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 16:28:47 2018

@author: Manuel Atnonio Gómez Angulo. Damián Serrano Fernández
Tutora: Antonia M. Chávez González

INTERFAZ GRAFICA DE ALGORITMO GENETICO HIBRIDO para entrada de datos.
Hemos usado la librería nativa de python para interfaces gráficas, conocida
como tkinter.

Bibliografía aquí:
    https://www.tutorialspoint.com/python3/python_gui_programming.htm
    https://recursospython.com/guias-y-manuales/posicionar-elementos-en-tkinter/
    stackoverflow.com

"""

# tkinter es la librería por defecto de interfaz gráfica de python
from tkinter import *
from tkinter import ttk
# Numpy es un paquete fundamental para la ciencia de la computacion en python
import numpy as np
from AgHibrido import * # Importar todas las funciones de nuestro archivo Algoritmo genético híbrido
from time import time  # Librería que nos sirve para contar el tiempo de ejecución


class Aplicacion():
    def __init__(self):
        
        # En el ejemplo se utiliza el prefijo 'self' para
        # declarar algunas variables asociadas al objeto 
        # ('mi_app')  de la clase 'Aplicacion'. Su uso es 
        # imprescindible para que se pueda acceder a sus
        # valores desde otros métodos:
        
        self.raiz = Tk()
        
        self.raiz.geometry('850x650')
        
        # Impide que los bordes puedan desplazarse para
        # ampliar o reducir el tamaño de la ventana 'self.raiz':
        
        self.raiz.resizable(width=False,height=False)
        self.raiz.title('Trabajo de IA 2018, AG con SA. Manuel Antonio Gómez' +
                        ' Angulo, Damián Serrano Fernández')
        
        # Los Frame son marcos a los cuales les vamos a agregar todos los
        # controles de la interfaz gráfica.
        # Cada uno de ellos aparecerá debajo del otro, para que 
        # la visualización sea atractiva.
        frame = Frame(self.raiz)
        frame.pack()
        
        topFrame = Frame(self.raiz)
        topFrame.pack( side = TOP, padx = 5, pady = 5 )
        
        topFrame2 = Frame(self.raiz)
        topFrame2.pack( side = TOP, padx = 5, pady = 5 )
        
        topFrameColores = Frame(self.raiz)
        topFrameColores.pack( side = TOP, padx = 5, pady = 5 )
        
        topFrame4 = Frame(self.raiz)
        topFrame4.pack( side = TOP, padx = 5, pady = 5 )
        
        bottomFrame  = Frame(self.raiz)
        bottomFrame.pack( side = BOTTOM, padx = 5, pady = 5 )
        
        # Widgets Tamaño de población
        var = StringVar(self.raiz)
        var.set(50) # Variable que sirve para poner un valor por defecto en un control de tKinter
        # Creación de label dentro del marco frame
        self.lblTamPoblacion = ttk.Label(frame, text = "Tamaño población [5, 100]")
        # Empaquetar el label hacia la izquierda, con margen de 5 px
        self.lblTamPoblacion.pack( side = LEFT, padx = 5, pady = 5)

        # Creación de Spinbox (lista desplegable de tkinger), que va de 5 a 1000.
        # con selección por defecto, según lo indicado en var.
        self.spnTamPoblacion = Spinbox(frame, from_ = 5, to = 1000,
                                       textvariable=var)
        self.spnTamPoblacion.pack( side = LEFT, padx = 5, pady = 5)

        # Widgets Número de nodos

        var = StringVar(self.raiz)
        var.set(9)
        self.lblNumNodos = ttk.Label(frame, text = "Número de nodos [5, 100]")
        self.lblNumNodos.pack( side = LEFT, padx = 5, pady = 5)
        self.spnNumNodos = Spinbox(frame, from_ = 5, to = 100, 
                                   textvariable=var)
        self.spnNumNodos.pack( side = LEFT, padx = 5, pady = 5)

         # Widgets Número de generaciones
        var = StringVar(self.raiz)
        var.set(13)
        self.lblNumGeneraciones = ttk.Label(frame, text = "Número de generaciones [5, 100]")
        self.lblNumGeneraciones.pack( side = LEFT, padx = 5, pady = 5)
        self.spnNumGeneraciones = Spinbox(frame, from_ = 5, to = 100, 
                                          textvariable=var)
        self.spnNumGeneraciones.pack( side = LEFT, padx = 5, pady = 5)
                
         # Widgets Porcentaje de Poblacion Inicial A Mantener
        self.lblPorcPoblacionInicialAMantener = ttk.Label(topFrame, text = "Porcentaje de poblacion inicial a mantener")
        self.lblPorcPoblacionInicialAMantener.pack( side = LEFT, padx = 5, pady = 5)
        # Creación de widget ListBox de tkinter para el porcentaje padres a mantener
        # de altura 7
        self.lstPorcPoblacionInicialAMantener = Listbox(topFrame, exportselection=0, height=7)

        i = 0
        # Añadir del 0.2 al 0.8 en el Listbox de porcentaje de padres
        for cont in np.arange(0.2, 0.8, 0.1): 
            i+=1
            self.lstPorcPoblacionInicialAMantener.insert(i, round(cont,2) )
        self.lstPorcPoblacionInicialAMantener.pack( side = LEFT, padx = 5, pady = 5)
        # Selección por defecto del primer elemento
        self.lstPorcPoblacionInicialAMantener.selection_set( first = 0 )
        
         # Widgets Probabilidad Eje
        self.lblProbEje = ttk.Label(topFrame, text = "Probabilidad de eje")
        self.lblProbEje.pack( side = LEFT, padx = 5, pady = 5)
        self.lstProbEje = Listbox(topFrame, exportselection=0, height=5)

        i = 0
        for cont in np.arange(0.3, 0.8, 0.1): 
            i+=1
            self.lstProbEje.insert(i, round(cont,2) )
        self.lstProbEje.pack( side = LEFT, padx = 5, pady = 5)
        self.lstProbEje.selection_set( first = 2 )
        
        # Widgets Temperatura Inicial
        self.lblTempIni = ttk.Label(topFrame, text = "Temperatura Inicial")
        self.lblTempIni.pack( side = LEFT, padx = 5, pady = 5)
        self.lstTempIni = Listbox(topFrame, exportselection=0, height=5)

        self.lstTempIni.insert(1, 0.8 )
        self.lstTempIni.insert(2, 0.9 )
        self.lstTempIni.insert(3, 1 )
        self.lstTempIni.insert(4, 10 )
        self.lstTempIni.insert(5, 100 )

        self.lstTempIni.pack( side = RIGHT, padx = 5, pady = 5)
        self.lstTempIni.selection_set( first = 4 )
        
        # Widgets Número de colores
        var = StringVar(self.raiz)
        var.set(3)
        self.lblNumColores = ttk.Label(topFrameColores, text = "Número de colores [3, 5]")
        self.lblNumColores.pack( side = LEFT, padx = 5, pady = 5)
        self.spnNumColores = Spinbox(topFrameColores, from_ = 3, to = 5, 
                                          textvariable=var)
        self.spnNumColores.pack( side = LEFT, padx = 5, pady = 5)
        
         # Widgets lista de adyacencias
        self.lblListaAdyacencias = Label(topFrame2, text = "Lista de adyacencias")
        self.lblListaAdyacencias.pack( side = LEFT)
        self.txtListaAdyacencias = Text(topFrame2, width=80, height=5)
        self.txtListaAdyacencias.pack(side = RIGHT)
        self.txtListaAdyacencias.insert(
                END, '1, 4, 5, 6 | 0, 2, 3, 4, 7 | 1, 4, 5, 6 | ' + \
                '1, 4, 5, 6, 8 | 0, 1, 2, 3 | 0, 2, 3 | 0, 2, 3 | 1 | 3')
        
        # Widgets donde muestro los datos seleccionados
        self.lblTinfo = Label(topFrame4, text = "Errores y lista de adyacencia")
        self.lblTinfo.pack(side=LEFT, padx = 3, pady = 3)
        self.tinfo = Text(topFrame4, width=80, height=15)
        
        # Define el widget Text 'self.tinfo ' en el que se
        # pueden introducir varias líneas de texto:
        # Sitúa la caja de texto 'self.tinfo' en la parte
        # superior de la ventana 'self.raiz':
        
        self.tinfo.pack(side=RIGHT, padx = 3, pady = 3)
        
        # Define el widget Button 'self.binfo' que llamará 
        # al metodo 'self.verinfo' cuando sea presionado
        
        self.binfo = ttk.Button(bottomFrame, text='Ejecutar', 
                                command=self.ejecutar)
        
        # Coloca el botón 'self.binfo' debajo y a la izquierda
        # del widget anterior
                                
        self.binfo.pack(side=LEFT)
        
        # Define el botón 'self.bsalir'. En este caso
        # cuando sea presionado, el método destruirá o
        # terminará la aplicación-ventana 'self.raíz' con 
        # 'self.raiz.destroy'
        
        self.bsalir = ttk.Button(bottomFrame, text='Salir', 
                                 command=self.raiz.destroy)
                                 
        # Coloca el botón 'self.bsalir' a la derecha del 
        # objeto anterior.
                                 
        self.bsalir.pack(side=RIGHT)
        
        # El foco de la aplicación se sitúa en el botón
        # 'self.binfo' resaltando su borde. Si se presiona
        # la barra espaciadora el botón que tiene el foco
        # será pulsado. El foco puede cambiar de un widget
        # a otro con la tecla tabulador [tab]
        
        self.spnTamPoblacion.focus_set()
        
        self.raiz.mainloop()
    
    def ejecutar(self):
        
        # Borra el contenido que tenga en un momento dado
        # la caja de texto
        
        self.tinfo.delete("1.0", END)
        
        # Obtiene información de la ventana 'self.raiz':
        
        texto_info = "" # Limiaamos el txt texto_info
        msnError = "" # Variable para mostrar mensaje de error en interfaz gráfica
        error = False # Variable en la que guardamos si hay o no hay error.
        tamPoblacion = self.spnTamPoblacion.get()
        numNodos = self.spnNumNodos.get()
        numGeneraciones = self.spnNumGeneraciones.get()
        porcPoblacionAMantener = self.lstPorcPoblacionInicialAMantener.get(
                self.lstPorcPoblacionInicialAMantener.curselection())
        probEje = self.lstProbEje.get(
                self.lstProbEje.curselection())
        numColores = self.spnNumColores.get()
        
        # Cogemos el texto de lista de incidencias completo menos el carácter \n
        txtListaAdyacencia = self.txtListaAdyacencias.get("1.0",'end-1c')
        # Captura de valor del widget ListBox de tempIni
        tempIni = self.lstTempIni.get(self.lstTempIni.curselection())
        listaAdyacencia = [] # Inicializamos la lista de adyacencias a vacío
        
        # COMPROBAMOS LOS POSIBLES ERRORES EN LA ENTRADA DE DATOS
        if not tamPoblacion.isdigit():
            error = True
            msnError+="Error. El tamaño de población debe ser un número entero\n"
        
        elif( int(tamPoblacion) < 5 or int(tamPoblacion) >100):
            error = True
            msnError += "Error. El tamaño de población debe estar entre 5 y 100\n"
        else:
            tamPoblacion = int(tamPoblacion)
        
        if not numGeneraciones.isdigit():
            error = True
            msnError += "Error. El número de generaciones debe ser un número entero\n"
        
        elif( int(numGeneraciones) < 5 or int(numGeneraciones) >100):
            error = True
            msnError += "Error. El número de generaciones debe estar entre 5 y 100\n"
        else:
            numGeneraciones = int(numGeneraciones)
        
        if not numColores.isdigit():
            error = True
            msnError += "Error. El número de colores debe ser un número entero\n"
        
        elif( int(numColores) < 3 or int(numColores) > 5):
            error = True
            msnError += "Error. El número de colroes debe estar entre 3 y 5\n"
        else:
            numColores = int(numColores)
            
        if not numNodos.isdigit():
            error = True
            msnError += "Error. El número de nodos debe ser un número entero\n"
        
        elif( int(numNodos) < 5 or int(numNodos) >100):
            error = True
            msnError += "Error. El número de nodos debe estar entre 5 y 100\n"
        else:
            numNodos = int(numNodos)
            
            # Creación de lista de listas con la lista de adyacencias, mediante
            # la lista de adyacencias que introdujo el usuario.
            if txtListaAdyacencia and not txtListaAdyacencia.isspace():
                
                # Lo pasamos a tipo lista de String, gracias a los símbolos | y ,
                listaAdyacenciaStr = [x.split(',') for x in txtListaAdyacencia.split('|')]
                
                # Comprobamos que la lista de adyancencias que introdujo el
                # usuario es válida. Es decir, si casa con el número de nodos.
                if len(listaAdyacenciaStr) != numNodos:
                    error = True
                    msnError += "La lista de adyacencias no coincide con el " + \
                        "número de nodos.\n Número de nodos: " + str(numNodos) + \
                        ". Lista de adyacencias: "+ str(len(listaAdyacenciaStr))+ \
                        "\n.Un nodo sin adyacencias es con ||." + \
                        "\nDebe haber un símbolo | menos que el número de nodos" + \
                        ". Número de símbolos |: " + str(len(listaAdyacenciaStr)-1) + \
                        "\n"
                        
                # Cogemos la lista de str y la convertimos en lista de enteros.
                # Tiene que ser lista de enteros, si no el programa peta.
                for fila in listaAdyacenciaStr:
                    try:
                        listaAdyacencia.append([int(elem) for elem in fila])
                    except:
                        error = True
                        msnError += "Error. Lista de adyacencias incorrecta." + \
                            " Ha introducido un campo que no es numérico.\n"
                    
        if not error:
            msnError = "Ninguno"
        
        # Construye una cadena de texto con toda la
        # información obtenida y la asignamos al widget texto_info :

        texto_info += "Error: " + msnError + "\n"
        texto_info += "Lista de adyacencias: " + str(listaAdyacencia)
         # Inserta la información en la caja de texto:
        
        self.tinfo.insert("1.0", texto_info)

        # Si no hay error ejecutamos ALGORITMO GENETICO HIBRIDO 
        # y realizamos impresiones por pantalla con la información necesaria.
        if not error:
            
            # ---> INICIO DE ESTO NO FUNCIONA BIEN. ES SOLO UN DETALLITO SIN IMPORTANCIA
            # Borra el contenido que tenga en un momento dado
            # la caja de texto
        
            self.tinfo.delete("1.0", END)
            texto_info = ""
            texto_info = "Lista de adyacencias: " + str(listaAdyacencia)
            self.tinfo.insert("1.0", texto_info)

            # <--- FIN DE NO FUNCIONA BIEN
            
            print ("\nTrabajo realizado por Manuel Antonio Gómez Angulo y "+ \
                   "Damían Serrano Fernández. Bajo la tutoría de Antonia " + \
                   "M. Chávez González")
            aleatorio = False
            
            # Si la lista de adyacencias está vacía se trata de que vamos a 
            # generar el grafo de forma aleatoria, con el número de nodos
            # establecido por el usuario y una probabilidad eje.
            if len(listaAdyacencia) == 0:
                aleatorio = True

            start_time = time() # Comenzamos a contar el tiempo desde aquí 


            # Llamamos a opcionInstancia, que se encargará de
            # generar el grafo con la lista de adyacencias, si no está vacía
            # o generar el grafo de forma aleatoria en caso contrario.
            numEjes, listaAdyacencia = opcionInstancia(tamPoblacion,
                numNodos, probEje,
                listaAdyacencia, int(numGeneraciones),
                float(porcPoblacionAMantener))
            
            print("Contra más alto sea el tamaño de población, mejor "+ \
                  "resultado devolverá el algoritmo genético híbrido"+ \
                  ", porque habrá más individuos que 'evolucionar' y " + \
                  "más posibles soluciones. Idem con el número de generaciones\n")
            print("\nContra más alta sea la temperatura Inicial, mejor " + \
                  "resultados devolverá el Algoritmo genético híbrido porque" + \
                  " entrará menos veces en el segundo if de enfriamiento " + \
                  "simulado.\n")
            
            print("\n*** DATOS PARA COPIAR ***. Por si se quiere ejecutar "+ \
                  "varias veces los mismos datos y para recordar lo que "+ \
                  "se introdujo antes\n")
            print("Tamaño de población: " + str(tamPoblacion))
            print("Número de nodos: " + str(numNodos))
            
            print("Número de generaciones: "+ str(numGeneraciones) )
            print ("\nPorcentaje de Poblacion Inicial A Mantener: " + str(porcPoblacionAMantener))
            if aleatorio:
                # Solo mostramos la probabilidad eje cuando el grafo
                # se ha generado de forma aleatoria.
                print ("Probabilidad de eje: " + str(probEje))
            print ("Temperatura inicial: " + str(tempIni))

            
            print ("LISTA DE ADYACENCIAS DE ENTRADA: ")
            print(txtListaAdyacencia)
           
            if aleatorio:
                print("\nLISTA DE ADYACENCIAS EN FORMATO DE ENTRADA")
                print (devuelveListaDeAdyacenciaFormatoEntrada(listaAdyacencia))    
            
            print ("\nNúmero de colores: " + str(numColores) + "\n")
            
            print ("\n *** FIN DE DATOS PARA COPIAR ***\n")
            print("\nNúmero de ejes: " + str(numEjes) + "\n")
            # Llamada a algoritmo principal creación POBLACION INICIAL
            # FUNCION DE ALGORIMO GENETICO
            poblacionInicial = generarPoblacionInicialAleatoria(
                    tamPoblacion, numNodos, listaAdyacencia, numColores)
            
            
            # Ejecutar funcion EVOLUCION. FUNCION DE ALGORIMO GENETICO
            # Le pasamos la población inicial, el número de generaciones,
            # el tamaño de población y el porcentaje de padres a mantener.
            # Nos devuevle los fitness y los individuos con mas fitness
            resultadosFitness, resultadosIndividuosMasFitness = evolucion(
                    poblacionInicial, numGeneraciones, tamPoblacion, tempIni,
                    numColores = numColores, 
                    porcentajeAMantener=porcPoblacionAMantener)
            
            print ("\nLISTA DE ADYACENCIA: ")
            print(listaAdyacencia)
            # Llamada  función VISUALIZAR RESULTADOS
            # Se le pasa los fitness y los individuos con mas fitness
            maxFitness = visualize_results(resultadosFitness, resultadosIndividuosMasFitness)
            print("Número de nodos: " + str(numNodos))
            print("Número de ejes: " + str(numEjes))
            print("Número de ejes con vecinos del mismo color: " + \
                  str( int(int(numEjes) - float(maxFitness)) ) )
    
            tiempoTranscurrido = time() - start_time
            print("TIEMPO TRANSCURRIDO: %.2f SEGUNDOS." % tiempoTranscurrido)

            # Salimos de la interfaz gráfica.
            # Es obligatorio salir de la interfaz gráfica para ver el grafo
            # dibujado. Por algún motivo, la librería de la interfaz gráfica 
            # de python (tkinter), no casa con la librería de interfaz gráfica
            # del grafo (matplotlib)
            self.raiz.destroy()            


"""
    Esta función sirve para que cuando generemos grafo de forma aleatoria, 
    le pasemos la lista de adyacencias  (tipo lista de listas) que genera ese
    grafo aleatorio y nos devuelve esa lista con el formato de entrada
    correspondiente con los símbolos |, en lugar de [].
    
    Básicamente esta función es para que si el usuario ejecuta el grafo
    aleaotorio, pueda copiar la lista de adyacencias directamente para hacer
    pruebas con ese mismo grafo, sin necesidad de convertir esa lista
    con el formato de entrada con los | por su cuenta.
    Es muy conveniente para lista de adyacencias muy grande.
"""
def devuelveListaDeAdyacenciaFormatoEntrada(listaAdyacencia):
    
    listaAdyacenciaFormEntrada = [] # Inicializamos lista a vacio
    
    # Recorremos lista
    for elem in listaAdyacencia:
        for elem2 in elem:
            # Añadimos cada elemento de la lista de adyacencia
            listaAdyacenciaFormEntrada.append(elem2)
            # Le ponemos una coma
            listaAdyacenciaFormEntrada.append(',')
        
        # Eliminamos la última coma
        listaAdyacenciaFormEntrada = listaAdyacenciaFormEntrada[:-1]
        # Añadimos el simbolo barra
        listaAdyacenciaFormEntrada.append('|')
    
    # Eliminamos la última barra
    listaAdyacenciaFormEntrada = listaAdyacenciaFormEntrada[:-1]
    # Ponemos todo de tipo String
    listaAdyacenciaFormEntradaStr = " ".join(
            str(x) for x in listaAdyacenciaFormEntrada)
    
    # Devolvemos lista con el formato de entrada
    return listaAdyacenciaFormEntradaStr



def main():
    # Ejecutamos la función princial de nuestra interfaz gráfica de tkinter
    mi_app = Aplicacion()
    return 0

if __name__ == '__main__':
    main()