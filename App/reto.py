"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from Sorting import selectionsort as ss
from Sorting import insertionsort as Is
from Sorting import shellsort as shs


from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("0- Salir")




def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1



def loadCSVFile (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        t1_start = process_time()
        with open(  cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
        t1_stop = process_time()
        print("Tiempo de ejecución de carga del casting es: "+str(t1_stop-t1_start)+" segundos")
    except:
        print("Hubo un error con la carga del archivo")
    return lst

def loadCSVFile1 (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        t1_start = process_time()
        with open(  cf.data_dir + file, encoding="utf-8-sig") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
        t1_stop = process_time()
        print("Tiempo de ejecución de carga de movies_details es: "+str(t1_stop-t1_start)+ " segundos")
    except:
        print("Hubo un error con la carga del archivo")
    return lst


def loadMovies ():
    lst = loadCSVFile("themoviesdb/MoviesCastingRaw-small.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def loadMovies1():
    lst = loadCSVFile1 ("themoviesdb/AllMoviesDetailsCleaned.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def less_greater(element1, element2, column, tipo_ordenamiento):
    if tipo_ordenamiento==1:
        if float(element1[column])<float(element2[column]):
            return True
        else:
            return False
    else:
        if float(element1[column])>float(element2[column]):
            return True
        else:
            return False

def crear_ranking_peliculas(function,column,lst,elements,cantidad):
    """
    requerimiento_2
    """
    if lst['size']==0:
        print("La lista esta vacía")
        return 0
    
    else:
        tipo_ordenamiento=int(elements)
        columna=None
        if column=="1":
            columna="vote_average"
        else:
            columna="vote_count"
        iterator=it.newIterator(lst)
        if function=="1":
            t1_start = process_time()
            ss.selectionSort(lst,less_greater,columna,tipo_ordenamiento)
            t1_stop = process_time()
            print("Tiempo de ejecución del ordenamiento SELECTION_SORT es de ",t1_stop-t1_start," segundos")
        elif function=="2":
            t1_start = process_time()
            Is.insertionSort(lst,less_greater,columna,tipo_ordenamiento)
            t1_stop = process_time()
            print("Tiempo de ejecución del ordenamiento INSERTION_SORT es de ",t1_stop-t1_start," segundos")
        else:
            t1_start = process_time()
            shs.shellSort(lst,less_greater,columna,tipo_ordenamiento)
            t1_stop = process_time()
            print("Tiempo de ejecución del ordenamiento SHELL_SORT es de ",t1_stop-t1_start," segundos")
        i=int(cantidad)    
        top=lt.subList(lst,lst["size"]-int(cantidad)+1,int(cantidad))
        iterator_top=it.newIterator(top)
        while it.hasNext(iterator_top):
                elemento_top=it.next(iterator_top)
                print(str(i)+". "+elemento_top["original_title"]+" con un "+columna+" de "+elemento_top[columna])
                i-=1
        return top

def crear_ranking_genero(genero,lst,column,elements,cantidad):
    """"
    requerimiento_6 
    """
    tipo_ordenamiento=int(elements)
    genero_iterador=it.newIterator(lst)
    genero_lista=lt.newList()
    columna=None
    if column=="1":
        columna="vote_average"
    else:
        columna="vote_count"       
    while it.hasNext(genero_iterador):
        element=it.next(genero_iterador)
        if genero.lower() in element["genres"].lower():
            lt.addLast(genero_lista,element)
    if genero_lista["size"]==0:
        print("\nNo hay coincidencias")
        return 0
    else:
        if int(cantidad)<=genero_lista["size"]:
            shs.shellSort(genero_lista, less_greater,columna,tipo_ordenamiento)
            iterator_top=it.newIterator(genero_lista)
            suma=0
            num_elementos=int(cantidad)
            sub_lista=lt.subList(genero_lista,genero_lista["size"]-int(cantidad)+1,int(cantidad))
            iterator_sub=it.newIterator(sub_lista)
            i=int(cantidad)
            print("\n")
            while it.hasNext(iterator_sub):
                elemento=it.next(iterator_sub)
                print(str(i)+". "+elemento["original_title"]+" con un "+columna+" de "+elemento[columna])
                suma+=float(elemento[columna])
                i-=1
            promedio=round((suma/num_elementos),2)
            print("El promedio de los "+columna+"s del ranking "+genero+" es de "+str(promedio))
            print("Hay un total de "+str(genero_lista["size"])+" películas que coinciden con este género\nRecuerde que estas películas también podrían coincidir con otros géneros\ndebido a que existen películas de varios géneros")
            return (genero_lista,promedio)
        else:
            print("\nLa cantidad excede el tamaño de la lista-> "+str(genero_lista["size"]))
            return 0

def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:

            if int(inputs[0])==1: #opcion 1
                lstmovies = loadMovies()

                lstmovies1 = loadMovies1() 
            elif int(inputs[0])==2: #opcion 2
                pass
                if lstmovies1==None or lstmovies1["size"]==0: #obtener la longitud de la lista
                    print("La lista está vacía")
                else:
                    print("1. VOTE_AVERAGE\n2. VOTE_COUNT")
                    column=input("Ingrese un número: ")
                    while True:
                        if column.isnumeric():
                            if int(column) in range(1,3):
                                break
                        else:
                            function=input("Ingrese una opción válida: ")   
                    print("\n1. SELECTION_SORT\n2. INSERTION_SORT\n3. SHELL_SORT")
                    function=input("Ingrese un número: ")
                    while True:
                        if function.isnumeric():
                            if int(function) in range(1,4):
                                break
                        else:
                            function=input("Ingrese una opción válida: ")
                    cantidad=input("\nIngrese el número de péliculas a retornar, mínimo 10: ")
                    while True:
                        if cantidad.isnumeric():
                            if int(cantidad) in range(10,lstmovies1["size"]+1):
                                break
                        else:
                            cantidad=input("Ingrese una cantidad válida: ")             
                    print("\n1. MEJORES/ASCENDENTE\n2. PEORES/DESCENDENTE")
                    elements=input("Ingrese un número: ")
                    while True:
                        if elements.isnumeric():
                            if int(elements) in range(1,3):
                                break
                        else:
                            elements=input("Ingrese una opción válida: \n")        
                    crear_ranking_peliculas(function,column,lstmovies1,elements,cantidad)


            elif int(inputs[0])==3: #opcion 3
                pass

            elif int(inputs[0])==4: #opcion 4
                pass

            elif int(inputs[0])==5: #opcion 5
                pass

            elif int(inputs[0])==6: #opcion 6
                pass

                if lstmovies1==None or lstmovies1["size"]==0: #obtener la longitud de la lista
                    print("\nLa lista está vacía")
                else:
                    genero=input("\nIngrese textualmente uno o varios de los siguientes géneros, puede combinarlos separándolos por un '|':\nDrama, Crime, Comedy, Action, Thriller, Documentary, Adventure,\nScience Fiction, Animation, Family, Romance, Mystery, Music,\nHorror, Fantasy, War, History, Western, Foreign, , TV Movie: ")
                    print("\n1. VOTE_AVERAGE\n2. VOTE_COUNT")
                    column=input("Ingrese un número: ")
                    while True:
                        if column.isnumeric():
                            if int(column) in range(1,3):
                                break
                        else:
                            function=input("Ingrese una opción válida: ")          
                    cantidad=input("\nIngrese el número de péliculas del género escogido a retornar: ")
                    while True:
                        if cantidad.isnumeric():
                            if int(cantidad)>=1:
                                break
                        else:
                            cantidad=input("Ingrese una cantidad válida: ")             
                    print("\n1. MEJORES/ASCENDENTE\n2. PEORES/DESCENDENTE")
                    elements=input("Ingrese un número: ")
                    while True:
                        if elements.isnumeric():
                            if int(elements) in range(1,3):
                                break
                        else:
                            elements=input("Ingrese una opción válida: \n")
                    crear_ranking_genero(genero,lstmovies1,column,elements,cantidad)

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()