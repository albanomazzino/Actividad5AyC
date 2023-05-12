def estrictamenteMenorOEscrictamenteMayor(tuplaA, tuplaB):
    return (tuplaA[0] < tuplaB[0] and tuplaA[1] < tuplaB[1]) or (tuplaA[0] > tuplaB[0] and tuplaA[1] > tuplaB[1])

def find_smallest_elem_as_big_as(sequence, subsequence, elem):
    low = 0
    high = len(subsequence) - 1

    while high > low:
        mid = (high + low) // 2
        if estrictamenteMenorOEscrictamenteMayor(sequence[subsequence[mid]][1], sequence[elem][1]):
            low = mid + 1
        else:
            high = mid

    return high

def imprimirResultado(longest_increasing_subsequence):
    cardinalidadResultado = len(longest_increasing_subsequence)
    if (cardinalidadResultado) > 0:
        print(cardinalidadResultado)
        for item in longest_increasing_subsequence:
            print(item, end=' ')
        print('') # restore the print's end stream
    else:
        print('0')

# Ordena cada plan de la coleccion (de la forma (index, (x,y)) ascendentemente tomando como criterio a la componente x de la tupla (x,y),
# donde en casos de empate, pone primero el último elemento de la colección (the latest)
def ordenarPlanes (coleccion):
    return sorted(coleccion, key=lambda x: (x[1][0], -x[0]))

# removesPlanesInvalidos(..) realiza una iteracion completa sobre la coleccion, removiendo todo elemento e = (i, (x, y)) cuya tupla (x,y) no satisfaga la condicion de validez
# Notese que solo se usa para realizar una reduccion inicial sobre la cardinalidad de la coleccion. Al cambiar eventualmente el estado de la fabrica,(por aplicar un plan),
# se podria volver a aplicar removerPlanesInvalidos
def removerPlanesInvalidos(coleccion, estadoInicialFabrica):
    coleccionValida = []
    for cursorIndicesColeccion, tuple in coleccion:
        if tuple[0] > estadoInicialFabrica[0] and tuple[1] > estadoInicialFabrica[1]:
            coleccionValida.append([cursorIndicesColeccion, tuple])
    return coleccionValida

def reconstruirIndicesSolucion(smallest_end_to_subsequence_of_length, planesExpansionIndexadosOrdenados, parent):
    longest_increasing_subsequence = []
    curr_parent = smallest_end_to_subsequence_of_length[-1]
    while curr_parent is not None:
        longest_increasing_subsequence.append(planesExpansionIndexadosOrdenados[curr_parent][0] + 1) # + 1 para corregir el offset de la lista que empieza en 0 y la solucion tiene indices que comienzan en 1
        curr_parent = parent[curr_parent]
    longest_increasing_subsequence.reverse()
    return longest_increasing_subsequence

def optimized_dynamic_programming_solution(planesExpansion, estadoInicialFabrica):
    planesExpansionIndexados = list(enumerate(planesExpansion))  # Create a list of (index, tuple) pairs 
    planesExpansionIndexadosOrdenados = ordenarPlanes(planesExpansionIndexados)
    planesExpansionIndexadosOrdenados = removerPlanesInvalidos(planesExpansionIndexadosOrdenados, estadoInicialFabrica)
    longest_increasing_subsequence = []

    if (len(planesExpansionIndexadosOrdenados) > 0):
        smallest_end_to_subsequence_of_length = []
        parent = [None for _ in planesExpansionIndexadosOrdenados]

        for elem in range(len(planesExpansionIndexadosOrdenados)):
            if (len(smallest_end_to_subsequence_of_length) == 0 or
                    estrictamenteMenorOEscrictamenteMayor(planesExpansionIndexadosOrdenados[elem][1], planesExpansionIndexadosOrdenados[smallest_end_to_subsequence_of_length[-1]][1])):
                if len(smallest_end_to_subsequence_of_length) > 0:
                    parent[elem] = smallest_end_to_subsequence_of_length[-1]
                smallest_end_to_subsequence_of_length.append(elem)
            else:
                location_to_replace = find_smallest_elem_as_big_as(planesExpansionIndexadosOrdenados, smallest_end_to_subsequence_of_length, elem)
                smallest_end_to_subsequence_of_length[location_to_replace] = elem
                if location_to_replace != 0:
                    parent[elem] = smallest_end_to_subsequence_of_length[location_to_replace - 1]

        longest_increasing_subsequence = reconstruirIndicesSolucion(smallest_end_to_subsequence_of_length, planesExpansionIndexadosOrdenados, parent)

    imprimirResultado(longest_increasing_subsequence)
    
test_sequence = [(5, 4), (12, 11), (9, 8)]
test_sequence2 = [(2,2), (2,2)]

optimized_dynamic_programming_solution(test_sequence, (3,3))
optimized_dynamic_programming_solution(test_sequence2, (1,1))
optimized_dynamic_programming_solution(test_sequence2, (2,2))