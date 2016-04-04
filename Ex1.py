import numpy as np
import pandas as pd
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


def pretty_print_matrix(matrix, string_a, string_b):
    print pd.DataFrame(data=matrix, columns=list(string_b), index=list(string_a))


def compute_alignment(string_S, string_T, algo, alignment_score=ex1_alignment_score):
    string_S = '-' + string_S
    string_T = '-' + string_T
    dp_matrix = np.zeros((len(string_S)+1, len(string_T)+1))
    dp_matrix[:, :] = -np.inf
    dp_matrix[1,1] = 0
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


            top_val = dp_matrix[iter_a, iter_b+1] + alignment_score(s_i, '-')
            top_left_val = dp_matrix[iter_a, iter_b] + alignment_score(s_i, t_j)
            left_val = dp_matrix[iter_a+1, iter_b] + alignment_score('-', t_j)


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

            dp_matrix[iter_a+1, iter_b+1] = new_cell_value
            dp_direction_matrix[iter_a+1, iter_b+1] = new_cell_direction




    pretty_print_matrix(dp_matrix[1:,1:], string_S, string_T)
    max_plac = np.argmax(dp_matrix[-1,:])

    #selec one of the arbitray maxima

    if algo == 'NW':
        [current_row_index, current_column_index] = np.asarray(dp_matrix.shape) - 1
    elif algo == 'SW':
        [current_row_index, current_column_index] = np.argwhere(dp_matrix.max() == dp_matrix)[0]
    elif algo == 'overlap':
        max_on_last_row = np.max(dp_matrix[-1,2:])
        max_on_last_column = np.max(dp_matrix[2:,-1])
        if max_on_last_row > max_on_last_column:
            current_row_index = dp_matrix.shape[0] - 1
            current_column_index = np.argmax(dp_matrix[-1,:])
        else:
            current_row_index = np.argmax(dp_matrix[:,-1])
            current_column_index = dp_matrix.shape[1] - 1

    # max_row_index = np.argmax(dp_matrix) #   dp_matrix.shape[0] - 1
    # max_column_index = np.argmax(dp_matrix[-1,:])
    maximal_path = []
    S_tag = []
    T_tag = []
    while True:

        if algo == 'overlap' and (current_row_index == 1 or current_column_index == 1):
            break
        elif algo == 'NW' and current_row_index == 1:
            break

        direction = dp_direction_matrix[current_row_index, current_column_index]

        if direction == 0:
            S_tag.insert(0, string_S[current_row_index-1])
            T_tag.insert(0, '-')
            current_row_index -= 1

        elif direction == 1:
            S_tag.insert(0,string_S[current_row_index - 1])
            T_tag.insert(0,string_T[current_column_index - 1])
            current_column_index -= 1
            current_row_index -= 1
        elif direction == 2:
            S_tag.insert(0, '-')
            T_tag.insert(0, string_T[current_column_index-1])
            current_column_index -= 1

        elif direction == 3:
            S_tag.insert(0,string_S[current_row_index-1])
            T_tag.insert(0,string_T[current_column_index-1])
            break


        # if max_cell == 0:
        #     max_column_index -= 1
        # elif max_cell == 1:
        #     max_column_index -= 1
        #     max_row_index -= 1
        # elif max_cell == 2:
        #     max_row_index -= 1








    #now follow the max path
    # print [str(i) for i in maximal_path]
    print "Alignment"
    print S_tag
    print T_tag



if __name__ == "__main__":
    string_S = 'GATTAAGCCAAGGTTCCCCG'
    string_T = 'AATCTAATCCAGGTTCGCG'


    string_S = 'TATACGGGGGG'
    string_T = 'CGGAGGGGCAS'


    string_S = 'AAAAAA'
    string_T = 'AAAAAGA'


    # question_1_SW(string_S, string_T, algo='NW')
    # question_1_SW(string_S, string_T, algo='SW')
    # question_1_SW(string_S, string_T, algo='NW')
    compute_alignment('CG', 'GT', algo='NW', alignment_score=AWO_alignment_score)

    #2.c
    def AWO_alignment_score_3c(char_a, char_b):
        if char_a == '-' or char_b == '-':
            return -4
        if char_a == char_b:
            return 4
        if char_a != char_b:
            return -1

    compute_alignment('CG', 'GT', algo='NW', alignment_score=AWO_alignment_score_3c)


    pass



