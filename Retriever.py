import csv

from bs4 import BeautifulSoup
import requests
import webbrowser
from pprint import pprint as print

buildpage = "https://overframe.gg"


def __contructURL__(url):
    return buildpage + url


def __sacarMods__(url, matriz, nodos):
    b = requests.get(url).content
    soup = BeautifulSoup(b, "html.parser")  # se coge el DOM de la página
    mods = []
    for mod in soup.find_all("p", class_="Mod_name__ZXSMB"):
        contenido = mod.contents[0]
        mods.append(contenido)  # Almacena los mods en una lista
    i = 0
    for arma in soup.find_all("div", class_="Mod_itemCompatibility__3eY2_"):
        arma = arma.p.contents[0]
        mod = mods[i]
        nodos[mod] = [mod, arma]
        i += 1

    for modkey in mods:  # Por cada mod
        for modval in mods:
            if modkey == modval:
                pass
            else:
                try:
                    matriz[modkey][modval] += 1

                    matriz[modval][modkey] += 1
                except KeyError:
                    try:
                        matriz[modkey][modval] = 1
                        matriz[modval][modkey] = 1
                    except KeyError:
                        matriz[modkey] = {}
                        matriz[modkey][modval] = 1
                        matriz[modval] = {}
                        matriz[modval][modkey] = 1


def retrieve(url,tipo):
    nodos = {}
    matriz = {}
    pag = requests.get(url).content
    soup = BeautifulSoup(pag, "html.parser")
    for weapon in soup.find_all("a", class_="BuildSummaryFull_buildWrapper__11gpF"):
        __sacarMods__(__contructURL__(weapon["href"]), matriz, nodos)
    matriz=__convertirAGrafo__(matriz)
    EscribirDatos(tipo+"matriz", matriz)
    nodos=__convertirANodos__(nodos)
    EscribirDatos(tipo+"nodos",nodos)


def __convertirANodos__(noNodos:dict):
    g=[["id","label","usage"]]
    for key in noNodos.keys():
       g.append([noNodos[key][0],noNodos[key][0],noNodos[key][1]])
    return g
def __convertirAGrafo__(noGrafo: dict):
    grafo = [[""]]

    for key1 in noGrafo.keys():
        grafo[0].append(key1)

    for key1 in noGrafo.keys():
        grafo.append([key1])
        for key2 in noGrafo.keys():
            if key1 == key2:
                grafo[-1].append(0)

            else:
                try:
                    grafo[-1].append(noGrafo[key1][key2])
                except KeyError:
                    grafo[-1].append(0)

    return grafo


def EscribirDatos(nombre, datos):
    """
    Esta función simplemente escribe a CSV una lista de listas
    :param nombre: El nombre del archivo sin extensión
    :param datos: Los datos a escribir
    :return:
    """
    f = open(nombre + ".csv", "w", newline="")
    fescritor = csv.writer(f, delimiter=";")
    fescritor.writerows(datos)
    f.close()


retrieve("https://overframe.gg/builds/warframes/","warframes")
retrieve("https://overframe.gg/builds/primary-weapons/","primarias")
retrieve("https://overframe.gg/builds/secondary-weapons/","secundarias")
retrieve("https://overframe.gg/builds/melee-weapons/","melee")
retrieve("https://overframe.gg/builds/archwing/","arch")
retrieve("https://overframe.gg/builds/sentinels/","compañeros")