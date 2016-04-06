import numpy as np
import pandas as pd
from termcolor import colored

__author__ = 'ORI'


def ex1_alignment_score(char_a, char_b):
    if char_a == '-' or char_b == '-':
        return -3
    if char_a == char_b:
        return 2
    if char_a != char_b:
        return -2


def AWO_alignment_score(char_a, char_b):
    if char_a == '-' or char_b == '-':
        return 1
    if char_a == char_b:
        return 4
    if char_a != char_b:
        return -1


def pretty_print_matrix(matrix, string_a, string_b, indexes_to_highligh):
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print "S: {0}".format(string_a[1:])
    print "T: {0}".format(string_b[1:])
    toggle = True
    matrix = matrix.astype(np.int)
    string_to_print = "".join([colored("%5s" % s, 'blue') for s in string_b])
    print "%5s" % " " + string_to_print

    for s_counter_i, s_i in enumerate(string_a):
        string_to_print = ""

        string_to_print += colored("%5s" % s_i, 'blue')
        for t_counter_i, t_i in enumerate(string_b):
            if np.any([x == [s_counter_i + 1, t_counter_i + 1] for x in indexes_to_highligh]):
                string_to_print += colored("%5s" % matrix[s_counter_i, t_counter_i], 'red')
            else:
                string_to_print += colored("%5s" % matrix[s_counter_i, t_counter_i], 'green')
            toggle = not toggle
        print string_to_print

    # style is not supported for non-unique indicies.
    # df = pd.DataFrame(data=matrix)
    # print df
    from IPython.display import HTML


def compute_alignment(string_S, string_T, algo, alignment_score=ex1_alignment_score):
    string_S = '-' + string_S
    string_T = '-' + string_T
    dp_matrix = np.zeros((len(string_S) + 1, len(string_T) + 1))
    dp_matrix[:, :] = -np.inf
    dp_matrix[1, 1] = 0
    dp_direction_matrix = np.zeros_like(dp_matrix)
    if algo == 'overlap':
        dp_matrix[1, :] = 0
        dp_matrix[:, 1] = 0

    for iter_a, s_i in enumerate(string_S):
        for iter_b, t_j in enumerate(string_T):
            if algo == 'overlap' and (iter_a == 0 or iter_b == 0):
                continue
            elif iter_a == 0 and iter_b == 0:
                continue

            top_val = dp_matrix[iter_a, iter_b + 1] + alignment_score(s_i, '-')
            top_left_val = dp_matrix[iter_a, iter_b] + alignment_score(s_i, t_j)
            left_val = dp_matrix[iter_a + 1, iter_b] + alignment_score('-', t_j)

            if algo == 'NW' or algo == 'overlap':
                movement_options = [top_val,
                                    top_left_val,
                                    left_val]
            elif algo == 'SW':
                empty_match = 0
                movement_options = [top_val,
                                    top_left_val,
                                    left_val,
                                    empty_match]

            new_cell_value = np.max(movement_options)

            new_cell_direction = np.argmax(movement_options)

            dp_matrix[iter_a + 1, iter_b + 1] = new_cell_value
            dp_direction_matrix[iter_a + 1, iter_b + 1] = new_cell_direction

    max_plac = np.argmax(dp_matrix[-1, :])

    # selec one of the arbitray maxima

    if algo == 'NW':
        [current_row_index, current_column_index] = np.asarray(dp_matrix.shape) - 1
    elif algo == 'SW':
        [current_row_index, current_column_index] = np.argwhere(dp_matrix.max() == dp_matrix)[0]
    elif algo == 'overlap':
        max_on_last_row = np.max(dp_matrix[-1, 2:])
        max_on_last_column = np.max(dp_matrix[2:, -1])
        if max_on_last_row > max_on_last_column:
            current_row_index = dp_matrix.shape[0] - 1
            current_column_index = np.argmax(dp_matrix[-1, :])
        else:
            current_row_index = np.argmax(dp_matrix[:, -1])
            current_column_index = dp_matrix.shape[1] - 1

    S_tag = []
    T_tag = []
    path_indexes = []
    while True:

        direction = dp_direction_matrix[current_row_index, current_column_index]

        if algo == 'overlap' and (current_row_index == 1 or current_column_index == 1):
            break
        elif algo == 'NW' and current_row_index == 1:
            break
        elif algo == 'SW' and dp_matrix[current_row_index, current_column_index] == 0:
            break

        path_indexes.insert(0, [current_row_index, current_column_index])
        if direction == 0:
            S_tag.insert(0, string_S[current_row_index - 1])
            T_tag.insert(0, '-')
            current_row_index -= 1

        elif direction == 1:
            S_tag.insert(0, string_S[current_row_index - 1])
            T_tag.insert(0, string_T[current_column_index - 1])
            current_column_index -= 1
            current_row_index -= 1
        elif direction == 2:
            S_tag.insert(0, '-')
            T_tag.insert(0, string_T[current_column_index - 1])
            current_column_index -= 1

        elif direction == 3:
            S_tag.insert(0, string_S[current_row_index - 1])
            T_tag.insert(0, string_T[current_column_index - 1])
            break

    pretty_print_matrix(dp_matrix[1:, 1:], string_S, string_T, path_indexes)

    print "Alignment"
    print S_tag
    print T_tag


if __name__ == "__main__":

    """
    question 1
    """
    string_S = 'GATTAAGCCAAGGTTCCCCG'
    string_T = 'AATCTAATCCAGGTTCGCG'
    """
    a-c
    """
    compute_alignment(string_S, string_T, algo='NW', alignment_score=ex1_alignment_score)

    """
    d
    """
    compute_alignment(string_S, string_T, algo='SW', alignment_score=ex1_alignment_score)

    """
    e
    """
    compute_alignment(string_S, string_T, algo='overlap', alignment_score=ex1_alignment_score)

    string_S = 'TATACGGGGGG'
    string_T = 'CGGAGGGGCAS'
    compute_alignment(string_S, string_T, algo='overlap', alignment_score=ex1_alignment_score)

    compute_alignment(string_S, string_T, algo='NW', alignment_score=ex1_alignment_score)

    string_S = 'AAAAAA'
    string_T = 'AAAAAGA'

    """
    2.b
    """


    def AWO_alignment_score_2b_1(char_a, char_b):
        if char_a == '-' or char_b == '-':
            return -7
        if char_a == char_b:
            return 40
        if char_a != char_b:
            return -10


    compute_alignment('ACGTTCGAA', 'GCATTAGCC', algo='SW', alignment_score=AWO_alignment_score_2b_1)


    def AWO_alignment_score_2b_2(char_a, char_b):
        if char_a == '-' or char_b == '-':
            return 3
        if char_a == char_b:
            return 50
        if char_a != char_b:
            return 0


    compute_alignment('ACGTTCGAA', 'GCATTAGCC', algo='SW', alignment_score=AWO_alignment_score_2b_2)

    """
    2.c
    """
    compute_alignment('G', 'T', algo='NW', alignment_score=AWO_alignment_score_2b_1)
    compute_alignment('G', 'T', algo='NW', alignment_score=AWO_alignment_score_2b_2)

    """
    3.a
    """

    pass
