import random
import math


def clean_degree_list(degree_set):
    degree_sequence = []

    # turning the degree set into a list
    degree_set = list(degree_set.split(","))

    # handling the exception where the user inputs anything other than an integer number
    try:
        # turning the list strings into integers and appending it into degree_sequence
        for degree in degree_set:
            degree = int(degree)
            degree_sequence.append(degree)

    except:
        return False

    else:
        # sorting the list (descending) and turning it into a degree sequence
        degree_sequence.sort(reverse=True)
        return degree_sequence


def HavelHakimi_single_step(degree_sequence):
    degree_sequence.sort(reverse=True)
    # in graph theory, the letter 'p' is associated with the number of vertices
    p = len(degree_sequence)
    # in graph theory,the Greek capital letter 'delta' is associated with the biggest degree in a graph
    delta = degree_sequence[0]
    # as it is in Havel-Hakimi Algorithm, we should first delete the vertical with the biggest degree, then choose the
    # delta number of vertices that have the biggest degrees and  decrease them by 1
    flag = delta - 1
    degree_sequence.remove(degree_sequence[0])

    while flag >= 0:
        degree_sequence[flag] = degree_sequence[flag] - 1
        flag = flag - 1

    return degree_sequence


def is_a_graph(degree_set):
    degree_sequence = clean_degree_list(degree_set)

    if not degree_sequence:
        return 'Enter the degree set of a graph in this form: 6,6,4,3,3,2,2'
    else:

        # in graph theory, the letter 'p' is associated with the number of vertices
        p = len(degree_sequence)

        # in graph theory, delta is associated with the biggest degree in a graph
        delta = degree_sequence[0]

        # for a degree sequence to be able to belong to a real graph, the biggest degree shouldn't be more than p-1
        if delta > p - 1:
            return 'The degree set does not belong to a graph'

        # performing the Havel-Hakimi Algorithm on the remaining graphs
        else:

            # the function HavelHakimi_single_step performs only one step of the algorithm, as such a loop is needed

            n = p  # n is used to show the number of vertices after performing the havel-hakimi algorithm
            drawing_list = []
            drawing_list.insert(0, degree_sequence[:])

            # this is continued until the  sequence reaches all zeros (existent graph) or  doesn't (non-existent
            # graph), which leads the program to generate negative numbers
            while True:

                zero_indicator = 0
                negative_number_indicator = 0
                n = n - 1

                degree_sequence = HavelHakimi_single_step(degree_sequence)
                drawing_list.insert(0, degree_sequence[:])

                for degree in degree_sequence:

                    if degree == 0:
                        zero_indicator = zero_indicator + 1

                    elif degree < 0:
                        negative_number_indicator = negative_number_indicator + 1

                if zero_indicator == n:
                    return drawing_list

                elif negative_number_indicator != 0:
                    return 'The degree set does not belong to a graph'


# **************************************************************************************************** DRAWING FUNCTIONS

coordinates = [[222.5, 200]]


# generating a random coordinate which isn't too close to others
def coordinate_generator(x0, y0, x1, y1):
    x = random.randint(x0, x1)
    y = random.randint(y0, y1)
    coordinate = [x, y]

    # checking if the coordinates are too close
    global coordinates
    for c in coordinates:
        # calculating the Euclidean distance between current and other coordinates
        distance = math.dist(c, coordinate)

        if distance < 20:
            return coordinate_generator(x0, y0, x1, y1)

        else:
            coordinates.append(coordinate[:])
            return coordinate

# print(random_coordination(75,75,375,325))
