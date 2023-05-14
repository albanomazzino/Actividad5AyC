def leerEntrada():
    primeraLineaEntrada = input()
    primeraLineaEntrada = list(map(int, primeraLineaEntrada.split()))
    cantidadPlanesExpansion = primeraLineaEntrada[0]
    estadoInicialFabrica = (primeraLineaEntrada[1], primeraLineaEntrada[2])
    
    planesExpansion = []

    for _ in range(cantidadPlanesExpansion):
        lineaActualEntrada = input()
        lineaActualEntrada = list(map(int, lineaActualEntrada.split()))
        planesExpansion.append((lineaActualEntrada[0], lineaActualEntrada[1]))

    return estadoInicialFabrica, planesExpansion


def estrictamenteMenorOEscrictamenteMayor(tuplaA, tuplaB):
    return (tuplaA[0] < tuplaB[0] and tuplaA[1] < tuplaB[1]) or (tuplaA[0] > tuplaB[0] and tuplaA[1] > tuplaB[1])

def minElemTanGrandeComo(planes, planesSubString, elem):
    cursorBajo = 0
    cursorAlto = len(planesSubString) - 1

    while cursorAlto > cursorBajo:
        cursorMitad = (cursorAlto + cursorBajo) // 2
        if estrictamenteMenorOEscrictamenteMayor(planes[planesSubString[cursorMitad]][1], planes[elem][1]):
            cursorBajo = cursorMitad + 1
        else:
            cursorAlto = cursorMitad

    return cursorAlto

def imprimirResultado(lis):
    cardinalidadResultado = len(lis)
    if (cardinalidadResultado) > 0:
        print(cardinalidadResultado)
        for item in lis:
            print(item, end=' ')
        print('') # restore the print's end stream
    else:
        print('0')

# Ordena cada plan de la coleccion (de la forma (index, (x,y)) ascendentemente tomando como criterio a la componente x de la tupla (x,y),
# donde en casos de empate, pone primero el último elemento de la colección (the latest)
def ordenarPlanes(coleccion):
    return sorted(coleccion, key=lambda x: (x[1][0],x[1][1], -x[0]))

# removesPlanesInvalidos(..) realiza una iteracion completa sobre la coleccion, removiendo todo elemento e = (i, (x, y)) cuya tupla (x,y) no satisfaga la condicion de validez
# Notese que solo se usa para realizar una reduccion inicial sobre la cardinalidad de la coleccion. Al cambiar eventualmente el estado de la fabrica,(por aplicar un plan),
# se podria volver a aplicar removerPlanesInvalidos
def removerPlanesInvalidos(coleccion, estadoInicialFabrica):
    coleccionValida = []
    for cursorIndicesColeccion, tuple in coleccion:
        if tuple[0] > estadoInicialFabrica[0] and tuple[1] > estadoInicialFabrica[1]:
            coleccionValida.append([cursorIndicesColeccion, tuple])
    return coleccionValida

def reconstruirIndicesSolucion(minFinParaLISdeLongitud, planesExpansionIndexadosOrdenados, previoAlActual):
    lis = []
    indiceActual = minFinParaLISdeLongitud[-1]
    while indiceActual is not None:
        lis.append(planesExpansionIndexadosOrdenados[indiceActual][0] + 1) # + 1 para corregir el offset de la lista que empieza en 0 y la solucion tiene indices que comienzan en 1
        indiceActual = previoAlActual[indiceActual]
    lis.reverse()
    return lis

def lisPlanesExpansion(planesExpansion, estadoInicialFabrica):
    planesExpansionIndexados = list(enumerate(planesExpansion))  # Create a list of (index, tuple) pairs 
    planesExpansionIndexadosOrdenados = ordenarPlanes(planesExpansionIndexados)
    planesExpansionIndexadosOrdenados = removerPlanesInvalidos(planesExpansionIndexadosOrdenados, estadoInicialFabrica)
    lisPlanesExpansion = []

    if (len(planesExpansionIndexadosOrdenados) > 0):
        minFinParaLISdeLongitud = []
        parent = [None for _ in planesExpansionIndexadosOrdenados]
        for elem in range(len(planesExpansionIndexadosOrdenados)):
            if (len(minFinParaLISdeLongitud) == 0 or
                    estrictamenteMenorOEscrictamenteMayor(planesExpansionIndexadosOrdenados[elem][1], planesExpansionIndexadosOrdenados[minFinParaLISdeLongitud[-1]][1])):
                if len(minFinParaLISdeLongitud) > 0:
                    parent[elem] = minFinParaLISdeLongitud[-1]
                minFinParaLISdeLongitud.append(elem)
            else:
                posAReemplazar = minElemTanGrandeComo(planesExpansionIndexadosOrdenados, minFinParaLISdeLongitud, elem)
                minFinParaLISdeLongitud[posAReemplazar] = elem
                if posAReemplazar != 0:
                    parent[elem] = minFinParaLISdeLongitud[posAReemplazar - 1]

        lisPlanesExpansion = reconstruirIndicesSolucion(minFinParaLISdeLongitud, planesExpansionIndexadosOrdenados, parent)

    return lisPlanesExpansion

def elonQuiereExpandir():
    estadoInicialFabrica, planesExpansion = leerEntrada()
    indicesSolucion = lisPlanesExpansion(planesExpansion, estadoInicialFabrica)
    imprimirResultado(indicesSolucion)

elonQuiereExpandir()