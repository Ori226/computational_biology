import numpy as np
import pandas as pd
__author__ = 'ORI'



def alignment_score(char_a, char_b):
    if char_a == '-' or char_b == '-':
        return -3
    if char_a == char_b:
        return 2
    if char_a != char_b:
        return -2

def pretty_print_matrix(matrix, string_a, string_b):
    print pd.DataFrame(data=matrix, columns=list(string_b), index=list(string_a))
    pass
    # print DataFrame(x)


def question_1_NW(string_S, string_T):
    string_S = '-' + string_S
    string_T = '-' + string_T


    dp_matrix = np.zeros((len(string_S)+1, len(string_T)+1))
    dp_matrix[:, :] = -np.inf
    dp_matrix[1,1] = 0


    for iter_a, s_i in enumerate(string_S):
        for iter_b, t_j in enumerate(string_T):
            if iter_a == 0 and iter_b == 0:
                continue
            score = alignment_score(s_i, t_j)

            top_left_val = dp_matrix[iter_a, iter_b] + alignment_score(s_i, t_j)
            top_val = dp_matrix[iter_a, iter_b+1] + alignment_score(s_i, '-')
            left_val = dp_matrix[iter_a+1, iter_b] + alignment_score('-', t_j)


            new_cell_value = np.max([dp_matrix[iter_a, iter_b] + alignment_score(s_i, t_j),
                                     dp_matrix[iter_a, iter_b+1] + alignment_score(s_i, '-'),
                                     dp_matrix[iter_a+1, iter_b] + alignment_score('-', t_j)])
            dp_matrix[iter_a+1, iter_b+1] = new_cell_value

            print score
    pretty_print_matrix(dp_matrix[1:,1:], string_S, string_T)
    max_plac = np.argmax(dp_matrix[-1,:])
    max_row_index = dp_matrix.shape[0] - 1
    max_column_index = np.argmax(dp_matrix[-1,:])
    maximal_path = []
    S_tag = []
    T_tag = []
    while max_row_index > 1:
        left_cell = dp_matrix[max_row_index, max_column_index -1]
        top_left_cell = dp_matrix[max_row_index - 1, max_column_index -1]
        top_cell = dp_matrix[max_row_index - 1, max_column_index]



        max_cell = np.argmax([left_cell, top_left_cell, top_cell])

        max_cell_value = np.max([left_cell, top_left_cell, top_cell])
        print "direction:{0}, value:{1}".format(['left', 'top_left', 'top'][max_cell],max_cell_value)
        maximal_path.insert(0,max_cell)
        direction = max_cell
        if direction == 0:
            S_tag.insert(0, '-')
            T_tag.insert(0, string_T[max_column_index-1])
        elif direction == 1:
            S_tag.insert(0,string_S[max_row_index-1])
            T_tag.insert(0,string_T[max_column_index-1])
            pass
        elif direction == 2:
            S_tag.insert(0, string_S[max_row_index-1])
            T_tag.insert(0, '-')


        if max_cell == 0:
            max_column_index -= 1
        elif max_cell == 1:
            max_column_index -= 1
            max_row_index -= 1
        elif max_cell == 2:
            max_row_index -= 1





    #now follow the max path
    # print [str(i) for i in maximal_path]
    print "Alignment"
    print S_tag
    print T_tag

def question_1_SW(string_S, string_T):
    string_S = '-' + string_S
    string_T = '-' + string_T
    dp_matrix = np.zeros((len(string_S)+1, len(string_T)+1))
    dp_matrix[:, :] = -np.inf
    dp_matrix[1,1] = 0
    dp_direction_matrix = np.zeros_like(dp_matrix)


    for iter_a, s_i in enumerate(string_S):
        for iter_b, t_j in enumerate(string_T):
            if iter_a == 0 and iter_b == 0:
                continue
            score = alignment_score(s_i, t_j)

            top_val = dp_matrix[iter_a, iter_b+1] + alignment_score(s_i, '-')
            top_left_val = dp_matrix[iter_a, iter_b] + alignment_score(s_i, t_j)
            left_val = dp_matrix[iter_a+1, iter_b] + alignment_score('-', t_j)
            empty_match = 0

            movement_options = [top_val,
                                top_left_val,
                                left_val,
                                empty_match]

            new_cell_value = np.max(movement_options)

            new_cell_direction = np.argmax(movement_options)

            dp_matrix[iter_a+1, iter_b+1] = new_cell_value
            dp_direction_matrix[iter_a+1, iter_b+1] = new_cell_direction

            print score
    pretty_print_matrix(dp_matrix[1:,1:], string_S, string_T)
    max_plac = np.argmax(dp_matrix[-1,:])

    #selec one of the arbitray maxima
    [max_row_index, max_column_index] = np.argwhere(dp_matrix.max() == dp_matrix)[0]

    # max_row_index = np.argmax(dp_matrix) #   dp_matrix.shape[0] - 1
    # max_column_index = np.argmax(dp_matrix[-1,:])
    maximal_path = []
    S_tag = []
    T_tag = []
    while max_row_index > 1:
        direction = dp_direction_matrix[max_row_index, max_column_index]

        if direction == 0:
            S_tag.insert(0, string_S[max_row_index-1])
            T_tag.insert(0, '-')
            max_row_index -= 1

        elif direction == 1:
            S_tag.insert(0,string_S[max_row_index-1])
            T_tag.insert(0,string_T[max_column_index-1])
            max_column_index -= 1
            max_row_index -= 1
        elif direction == 2:
            S_tag.insert(0, '-')
            T_tag.insert(0, string_T[max_column_index-1])
            max_column_index -= 1

        elif direction == 3:
            S_tag.insert(0,string_S[max_row_index-1])
            T_tag.insert(0,string_T[max_column_index-1])
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
    pass



if __name__ == "__main__":
    string_S = 'GATTAAGCCAAGGTTCCCCG'
    string_T = 'AATCTAATCCAGGTTCGCG'
    question_1_NW(string_S, string_T)

    question_1_SW(string_S, string_T)


    pass



