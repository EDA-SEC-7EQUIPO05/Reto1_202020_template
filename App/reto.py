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
        with open(cf.data_dir + file, encoding="utf-8-sig") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst

def loadFile1():
    return loadCSVFile("theMoviesdb/AllMoviesCastingRaw.csv", compareRecordIds)


def loadFile2():
    return loadCSVFile("theMoviesdb/AllMoviesDetailsCleaned.csv", compareRecordIds)

def loadMovies ():
    lst = loadCSVFile("theMoviesdb/movies-small.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst


def conocerActor (casting, movies, actor):
    movies_id = []
    pelis = []
    directores = [[],[]]
    suma = 0
    t1=process_time()
    for i in range(1,lt.size(casting)+1):
        movie = lt.getElement(casting, i)
        actor_1 = movie['actor1_name']
        actor_2 = movie['actor2_name']
        actor_3 = movie['actor3_name']
        actor_4 = movie['actor4_name']
        actor_5 = movie['actor5_name']
        if actor == actor_1 or actor == actor_2 or actor == actor_3 or actor == actor_4 or actor == actor_5:
            movies_id.append(movie['id'])
            if movie['director_name'] not in directores[0]:
                directores[0].append(movie['director_name'])
                directores[1].append(1)
            else:
                for i in range(0,len(directores[0])):
                    if directores[0][i] == movie['director_name']:
                        directores[1][i] += 1
                        break    
    for i in range(1,lt.size(movies)+1):
        movie = lt.getElement(movies, i)
        if movie['id'] in movies_id:
            pelis.append(movie['original_title'])
            suma += float(movie['vote_average'])
    mas_pelis = 0
    for i in range(0, len(directores[0])):
        if directores[1][i] > mas_pelis:
            director = directores[0][i]
            mas_pelis = directores[1][i]
    t2 = process_time()
    print("Tiempo de ejecición",(t2-t1),'segundos.')
    if len(pelis)!=0:
        rta = (pelis, len(pelis), round(suma/len(movies_id),2),director )
    else:
        rta = None
    return rta


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
                lstmovies = loadFile1()
                lstmovies1 = loadFile2()

            elif int(inputs[0])==2: #opcion 2
                pass

            elif int(inputs[0])==3: #opcion 3
                pass

            elif int(inputs[0])==4: #opcion 4
                actor = input("¿Qué actor quiere conocer?\n")
                print(conocerActor(lstmovies, lstmovies1, actor))

            elif int(inputs[0])==3: #opcion 5
                pass

            elif int(inputs[0])==4: #opcion 6
                pass


            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()