def is_strictly_less_than(a, b):
    return (a[0] < b[0] and a[1] < b[1]) or (a[0] > b[0] and a[1] > b[1])

def find_smallest_elem_as_big_as(sequence, subsequence, elem):
    low = 0
    high = len(subsequence) - 1

    while high > low:
        mid = (high + low) // 2
        if is_strictly_less_than(sequence[subsequence[mid]][1], sequence[elem][1]):
            low = mid + 1
        else:
            high = mid

    return high

def custom_sort(x):
    return (x[1][1], -x[1][0])


def optimized_dynamic_programming_solution(sequence, reference_tuple):
    indexed_sequence = list(enumerate(sequence))  # Create a list of (index, tuple) pairs 
    sorted_sequence = sorted(indexed_sequence, key=lambda x: (x[1][0], -x[0]))   # Sort by X-coordinate in ascending order and descend in tie-break cases
    start_index = 0
    for i, tuple in sorted_sequence:
        if tuple[0] > reference_tuple[0] and tuple[1] > reference_tuple[1]:
            start_index = i
            break
    sorted_sequence = sorted_sequence[start_index:]  # Remove tuples before the valid starting index

    smallest_end_to_subsequence_of_length = []
    added_tuples = set()  # Set to keep track of added tuples
    parent = [None for _ in sorted_sequence]

    for elem in range(len(sorted_sequence)):
        if ((len(smallest_end_to_subsequence_of_length) == 0 or
                is_strictly_less_than(sorted_sequence[elem][1], sorted_sequence[smallest_end_to_subsequence_of_length[-1]][1])) and
                sorted_sequence[elem][1] not in added_tuples):  # Check if tuple not already added
            if len(smallest_end_to_subsequence_of_length) > 0:
                parent[elem] = smallest_end_to_subsequence_of_length[-1]
            smallest_end_to_subsequence_of_length.append(elem)
            added_tuples.add(sorted_sequence[elem][1])  # Add tuple coordinates to the set
        else:
            location_to_replace = find_smallest_elem_as_big_as(sorted_sequence, smallest_end_to_subsequence_of_length, elem)
            smallest_end_to_subsequence_of_length[location_to_replace] = elem
            if location_to_replace != 0:
                parent[elem] = smallest_end_to_subsequence_of_length[location_to_replace - 1]

    curr_parent = smallest_end_to_subsequence_of_length[-1]
    longest_increasing_subsequence = []
    while curr_parent is not None:
        longest_increasing_subsequence.append(sorted_sequence[curr_parent][0] + 1) # + 1 para corregir el offset de la lista que empieza en 0 y la solucion tiene indices que comienzan en 1
        curr_parent = parent[curr_parent]

    longest_increasing_subsequence.reverse()

    print(len(longest_increasing_subsequence))
    for item in longest_increasing_subsequence:
        print(item, end=' ')
    print('') # restore the print's end stream
test_sequence = [(5, 4), (12, 11), (9, 8)]
test_sequence2 = [(2,2), (2,2)]

optimized_dynamic_programming_solution(test_sequence, (3,3))
optimized_dynamic_programming_solution(test_sequence2, (1,1))
 
"""
Current problems
    - (MAYBE, Depending on the tests we must pass) => the solution picks the latter (or bigger) tuple for two tuples with some equal coordinate (x = x' or y = y') 
    - Make it so it returns the original indexes, for the original input collection (not the ordered one)
    - Print 0 if no LIS
    - Re-leer enunciado porlas
"""