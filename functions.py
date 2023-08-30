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

    except ValueError:

        return False

    else:
        # sorting the list (descending) and turning it into a degree sequence
        degree_sequence.sort(reverse=True)
        return degree_sequence


def havel_hakimi_single_step(degree_sequence):

    degree_sequence.sort(reverse=True)

    # in graph theory,the Greek capital letter 'delta' is associated with the biggest degree of a graph
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


# ******************************************************************************************************************** #
# **********************************************DRAWING FUNCTIONS***************************************************** #
# ******************************************************************************************************************** #


# coordinate of the center of the canvas is already in so for loop can be used
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
def draw_dot(canvas):

    center = coordinate_generator(75, 75, 375, 325)
    canvas.create_oval(center[0]-3, center[1]-3, center[0]+3, center[1]+3, fill=hex_color_generator())
    return center


# draws what remains from the graph after the Havel-Hakimi algorithm is finished
def draw_base_graph(canvas,
                    info: list):

    # a dictionary that stores vertices' degrees and their coordinates
    vertices = {}
    degree_1 = []
    base_graph = info[0]
    flag = 0
    neighbour_vertices = {}

    # creates a dictionary containing the coordinates of the vertices and their degrees
    for vertex_degree in base_graph:

        # tuple() was needed to prevent a 'unhashable type: 'list'' error
        vertex_coordinate = tuple(draw_dot(canvas))
        vertices[vertex_coordinate] = vertex_degree

    # creates a list of vertices which their degree is 1
    for vertex in vertices:

        if vertices[vertex] == 1:
            degree_1.append(vertex)

    # this works because the number of 1's is always even, it creates a dictionary containing the vertices that
    # should be connected to each other
    for coordinate in degree_1:
        flag += 1

        if flag % 2 == 1:
            key = tuple(coordinate)

        else:
            neighbour_vertices[key] = tuple(coordinate)

    for neighbours in neighbour_vertices:

        canvas.create_line(neighbours[0],  # X0
                           neighbours[1],  # Y0
                           neighbour_vertices[neighbours][0],  # X1
                           neighbour_vertices[neighbours][1])  # Y1

    return vertices


# since dictionaries are not indexed in Python, and yet 'for loop' iterates a dictionary from left
# while new keys are added to right, therefore this function is needed to add a key to the left of a dictionary.
def add_to_left(dictionary, new_key, new_value):

    dictionary_holder = dictionary.copy()
    dictionary.clear()
    new_dictionary = {new_key: new_value}
    new_dictionary.update(dictionary_holder)

    return new_dictionary


# it draws lines between it and vertices which their degree has been reduced in that specific step
# it also updates the dictionary to a higher level and returns it
def line_drawer_single_step(lower_level: dict,
                            higher_level: list,
                            biggest_degree_coordinate: tuple,
                            delta: int,
                            canvas):

    higher_level_index = 1  # this starts from 1 since the first value (index 0) in higher_level is not needed

    for coordinate in lower_level:

        higher_degree = higher_level[higher_level_index]
        lower_degree = lower_level[coordinate]
        higher_level_index += 1

        if higher_degree - lower_degree == 1:

            canvas.create_line(coordinate[0],  # X0
                               coordinate[1],  # Y0
                               biggest_degree_coordinate[0],  # X1
                               biggest_degree_coordinate[1])  # Y1

            lower_level[coordinate] += 1

    new_higher_level = add_to_left(lower_level,
                                   tuple(biggest_degree_coordinate),
                                   delta)

    return new_higher_level


# iterates through levels and feeds them to line_drawer_single_step
def draw_graph(canvas, info):

    lower_level = draw_base_graph(canvas, info)

    for level in info:

        if level == info[0]:  # level 0 is already generated by draw_base_graph function
            continue

        else:

            # it creates its lower level  dictionary as it goes on
            lower_level = line_drawer_single_step(lower_level=lower_level,
                                                  higher_level=level,
                                                  biggest_degree_coordinate=draw_dot(canvas),
                                                  delta=info[info.index(level)][0],
                                                  canvas=canvas)































































































