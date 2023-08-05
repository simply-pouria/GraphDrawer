import random
import math
import tkinter as tk



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


def havel_hakimi_single_step(degree_sequence):
    degree_sequence.sort(reverse=True)
    # in graph theory,the Greek capital letter 'delta' is associated with the biggest degree in a graph
    delta = degree_sequence[0]
    # as it is in Havel-Hakimi Algorithm, we should first delete the vertical with the biggest degree, then choose the
    # delta number of vertices that have the biggest degrees and  decrease them by 1
    flag = delta - 1
    degree_sequence.remove(degree_sequence[0])

    while flag >= 0:
        degree_sequence[flag] = degree_sequence[flag] - 1
        flag = flag - 1
        degree_sequence.sort(reverse=True)

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

                degree_sequence = havel_hakimi_single_step(degree_sequence)
                drawing_list.insert(0, degree_sequence[:])

                for degree in degree_sequence:

                    if degree == 0:
                        zero_indicator = zero_indicator + 1

                    elif degree < 0:
                        negative_number_indicator = negative_number_indicator + 1

                if zero_indicator == n:
                    drawing_list.remove(drawing_list[0])
                    return drawing_list

                elif negative_number_indicator != 0:
                    return 'The degree set does not belong to a graph'


# **********************************************************************************************************************
# **********************************************DRAWING FUNCTIONS*******************************************************
# **********************************************************************************************************************


# coordinate of the center of the canvas
every_coordinate = [[222.5, 200]]


# generating a random coordinate which isn't too close to others
# arguments are used to indicate the range in which numbers are generated
def coordinate_generator(x0, y0, x1, y1):
    x = random.randint(x0, x1)
    y = random.randint(y0, y1)
    coordinate = [x, y]

    # checking if the coordinates are too close
    global every_coordinate
    for c in every_coordinate:
        # calculating the Euclidean distance between current and other coordinates
        distance = math.dist(c, coordinate)

        if distance < 100:
            return coordinate_generator(x0, y0, x1, y1)

        else:
            every_coordinate.append(coordinate[:])
            return coordinate


# generates a random hex color
def hex_color_generator():
    def get_int():
        return random.randint(0, 255)

    return f'#{get_int():02X}{get_int():02X}{get_int():02X}'


# draws a dot, needed a function for it as it's not straightforward at all in tkinter
def draw_dot(canvas, number):

    while number > 0:
        number -= 1
        center = coordinate_generator(75, 75, 375, 325)
        canvas.create_oval(center[0]-5, center[1]-5, center[0]+5, center[1]+5, fill=hex_color_generator())


# draws what remains from the graph after the Havel-Hakimi algorithm is finished
def draw_base_graph(canvas, info):
    base_graph = info[0]
    p = len(base_graph)
    draw_dot(canvas, p)





























