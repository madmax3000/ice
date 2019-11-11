#! /usr/bin/env python

import sys
import math
import gv
import circuit_exceptions as CktEx
import circuit_elements as CktElem
from matrix import *


def scrub_elements(x, row, col):
    """
    Remove any leading or trailing quotes
    and also carriage returns (\n) that
    may have been added while generating the csv file.
    """


    if x[row][col]:
        if "\n" in x[row][col]:
            x[row][col] = x[row][col][:-1]

        if "\r" in x[row][col]:
            x[row][col] = x[row][col][:-1]

        if len(x[row][col])>1:
            while (x[row][col][0]=='"' or x[row][col][0]=="'"):
                x[row][col] = x[row][col][1:]
            while (x[row][col][-1]=='"' or x[row][col][-1]=="'"):
                x[row][col] = x[row][col][:-1]
            while (x[row][col][0]==' ' or x[row][col][0]==" "):
                x[row][col] = x[row][col][1:]
            while (x[row][col][-1]==' ' or x[row][col][-1]==" "):
                x[row][col] = x[row][col][:-1]

    return



def csv_reader(csv_file):
    """
    This matrix will read the .csv file
    The .csv file will contain the string "wire"
    where a zero impedance direct connection exists.
    Where no connection nor device
    resitor, inductor etc) exists, a blank will be found.
    """

    nw_matrix = []
    for line in csv_file:
        nw_matrix.append(line.split(","))

    nw_rows = len(nw_matrix)
    nw_columns = len(nw_matrix[0])


    # Remove the leading and trailing quotes
    # and carriage returns
    for c1 in range(0, nw_rows):
        for c2 in range(0, nw_columns):
            scrub_elements(nw_matrix, c1, c2)

    return nw_matrix



def reading_params(param_file):
    """ Read a file. Remove additional quotes and
    carriage returns. Remove leading spaces. """

    from_file = []

    for line in param_file:
        from_file.append(line.split(","))

    for c1 in range(len(from_file)):
        for c2 in range(len(from_file[c1])-1, -1, -1):
            # Remove additional quotes and carriage returns
            if from_file[c1][c2]:
                scrub_elements(from_file, c1, c2)
            # Remove blank spaces and null elements
            if from_file[c1][c2]==" " or from_file[c1][c2]=="":
                del from_file[c1][c2]

    return from_file



def csv_element_2D(elem):
    """
    Takes the [row, column] input for a csv file
    and given a human readable spreadsheet position.
    """

    # Convert column numbers to alphabets
    csv_col = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    csv_dict = {}
    csv_col_list = csv_col.split(" ")

    for c1 in range(26):
        csv_dict[c1] = csv_col_list[c1]

    # Because row 0 doesn't exist on a
    # spreadsheet
    row = elem[0]+1
    col = elem[1]

    # Create a list of all the alphabets
    # that a column will have
    col_nos = [-1]
    # On the run, an alphabet will
    # have a remainder and a prefix
    # This is essentially the first and
    # second alphabet
    prefix = 0
    remdr = col
    # The alphabet that is to be found
    col_count = 0

    while remdr-25>0:
        # If the column>26, the first
        # alphabet increments by 1
        prefix += 1
        remdr = remdr-26

        if remdr<26:
            if prefix>25:
                # More than 2 alphabets
                col_nos[col_count] = remdr
                # The remainder takes the prefix
                remdr = prefix-1
                # The prefix is the third/next alphabet
                prefix = 0
                # Add another element to the list
                col_nos.append(-1)
                col_count += 1
            else:
                # 2 alphabets only
                col_nos.append(-1)
                col_nos[-1] = prefix-1

    col_nos[col_count] = remdr

    col_letters = ""
    # The alphabets are backwards
    for c1 in range(len(col_nos)-1, -1, -1):
        col_letters = col_letters + csv_dict[col_nos[c1]]

    csv_format = str(row) + col_letters

    return csv_format




def csv_element(elem):
    """
    Takes the [row, column] input for a csv file
    and given a human readable spreadsheet position.
    """

    # Convert column numbers to alphabets
    csv_col = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    csv_dict = {}
    csv_col_list = csv_col.split(" ")

    for c1 in range(26):
        csv_dict[c1] = csv_col_list[c1]

    # Because row 0 doesn't exist on a
    # spreadsheet
    sheet = elem[0]
    row = elem[1] + 1
    col = elem[2]

    # Create a list of all the alphabets
    # that a column will have
    col_nos = [-1]
    # On the run, an alphabet will
    # have a remainder and a prefix
    # This is essentially the first and
    # second alphabet
    prefix = 0
    remdr = col
    # The alphabet that is to be found
    col_count = 0

    while remdr-25>0:
        # If the column>26, the first
        # alphabet increments by 1
        prefix += 1
        remdr = remdr - 26

        if remdr<26:
            if prefix>25:
                # More than 2 alphabets
                col_nos[col_count] = remdr
                # The remainder takes the prefix
                remdr = prefix - 1
                # The prefix is the third/next alphabet
                prefix = 0
                # Add another element to the list
                col_nos.append(-1)
                col_count += 1
            else:
                # 2 alphabets only
                col_nos.append(-1)
                col_nos[-1] = prefix - 1

    col_nos[col_count] = remdr

    col_letters = ""
    # The alphabets are backwards
    for c1 in range(len(col_nos)-1, -1, -1):
        col_letters = col_letters + csv_dict[col_nos[c1]]

    csv_format = str(row) + col_letters + str(sheet)

    return csv_format




def csv_element_truncate(csv_elem):
    """
    Takes a 3 dimensional input of a spreadsheet and
    removes the last number which is the sheet number.
    """

    c1 = len(csv_elem)-1
    flag = "number"
    while flag=="number":
        # When conversion to int fails
        # it means the element is an alphabet
        try:
            int(csv_elem[c1])
        except ValueError:
            flag = "alphabet"
        else:
            c1 -= 1

    return csv_elem[:c1+1]



def csv_element_extract(csv_elem):
    """
    Takes a 3 dimensional input of a spreadsheet and
    returns the last number which is the sheet number.
    """

    c1 = len(csv_elem)-1
    flag = "number"
    while flag=="number":
        # When conversion to int fails
        # it means the element is an alphabet
        try:
            int(csv_elem[c1])
        except ValueError:
            flag = "alphabet"
        else:
            c1 -= 1

    return int(csv_elem[c1+1:])



def csv_tuple_2D(csv_elem):
    """
    Convert a cell position from spreadsheet form
    to [row, tuple] form.
    """
    csv_elem.upper()

    # Create a dictionary of alphabets
    csv_col = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    csv_dict = {}
    csv_col_list = csv_col.split(" ")

    # Make the alphabets correspond to integers
    for c1 in range(1, 27):
        csv_dict[csv_col_list[c1-1]] = c1

    # The cell position starts with a number
    flag = "number"
    c1 = 0
    while flag=="number":
        # When conversion to int fails
        # it means the element is an alphabet
        try:
            int(csv_elem[c1])
        except ValueError:
            flag = "alphabet"
        else:
            c1 += 1

    # Split them up into numbers and alphabets
    pol_row = int(csv_elem[0:c1])
    pol_col = csv_elem[c1:]

    elem_tuple = [pol_row-1, 0]

    # Convert the alphabets to number
    # Similar to converting binary to decimal
    for c1 in range(len(pol_col)-1, -1, -1):
        if len(pol_col)-1-c1>0:
            elem_tuple[1] += 26*(len(pol_col)-1-c1)*csv_dict[pol_col[c1]]
        else:
            elem_tuple[1] += csv_dict[pol_col[c1]]-1

    return elem_tuple



def csv_tuple(csv_elem):
    """
    Convert a cell position from spreadsheet form
    to [row, tuple] form.
    """
    csv_elem.upper()

    # Create a dictionary of alphabets
    csv_col = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    csv_dict = {}
    csv_col_list = csv_col.split(" ")

    # Make the alphabets correspond to integers
    for c1 in range(1, 27):
        csv_dict[csv_col_list[c1-1]] = c1

    # The cell position starts with a number
    flag = "number"
    c1 = 0
    while flag=="number":
        # When conversion to int fails
        # it means the element is an alphabet
        try:
            int(csv_elem[c1])
        except ValueError:
            flag = "alphabet"
        else:
            c1 += 1

    # Split them up into numbers and alphabets
    pol_row = int(csv_elem[0:c1])
    pol_col = csv_elem[c1:]

    flag = "alphabet"
    c1 = 0
    while flag=="alphabet" and c1<len(pol_col):
        # When conversion to int fails
        # it means the element is an alphabet
        try:
            int(pol_col[c1])
        except ValueError:
            c1 += 1
        else:
            flag = "number"


    pol_sheet = int(pol_col[c1:])
    pol_col = pol_col[0:c1]

    elem_tuple = [pol_sheet, pol_row-1, 0]

    # Convert the alphabets to number
    # Similar to converting binary to decimal
    for c1 in range(len(pol_col)-1, -1, -1):
        if len(pol_col)-1-c1>0:
            elem_tuple[2] += 26*(len(pol_col)-1-c1)*csv_dict[pol_col[c1]]
        else:
            elem_tuple[2] += csv_dict[pol_col[c1]] - 1

    return elem_tuple



def human_loop(loop):
    """
    Takes a loop as a list of tuples.
    And prints a series of elements in spreadsheet format.
    """

    for c1 in range(len(loop)):
        print(csv_element(loop[c1]), end=" ")

    return



def jump_sanity(x, x_jump, sheet, row, column):
    """
    Check if it is a jump, an element
    or simply no connection
    """
    x_elem = x[sheet][row][column]

    if (x_elem ==''):
        del x_jump["exist"]
        del x_jump["jump"]
    elif (len(x_elem)>3):
        if (x_elem.lower()[0:4] == "jump"):
            del x_jump["exist"]
        else:
            del x_jump["jump"]
    else:
        del x_jump["jump"]

    return



def jump_checking(x_matrix, x_jump, sheet, row, col, no_of_rows, no_of_cols, nw_input):
    """
    Check for jump label sanity and add a list
    of elements where jumps exist. Basically
    examines whether element (sheet, c1, c2) is a jump
    and what are the elements around it.
    """
    # Current element
    curr_element = {"exist":0, "jump":1}
    # Determine if it is a jump label
    jump_sanity(x_matrix, curr_element, sheet, row, col)


    if ("jump" in curr_element):
        # If so, what is the element in the same column
        # and next row
        if (row<no_of_rows-1):
            next_row_element = {"exist":0, "jump":1}
            jump_sanity(x_matrix, next_row_element, sheet, row+1, col)
        else:
            next_row_element = {}

        # If so, what is the element in the same column
        # and previous row
        if (row>0):
            prev_row_element = {"exist":0, "jump":1}
            jump_sanity(x_matrix, prev_row_element, sheet, row-1, col)
        else:
            prev_row_element = {}

        # If so, what is the element in the same row
        # and next column
        if (col<no_of_cols-1):
            next_col_element = {"exist":0, "jump":1}
            jump_sanity(x_matrix, next_col_element, sheet, row, col+1)
        else:
            next_col_element = {}

        # If so, what is the element in the same row
        # and previous column
        if (col>0):
            prev_col_element = {"exist":0, "jump":1}
            jump_sanity(x_matrix, prev_col_element, sheet, row, col-1)
        else:
            prev_col_element = {}

    # Check if two jumps are next to each other
        if ("jump" in next_row_element or "jump" in next_col_element or \
            "jump" in prev_row_element or "jump" in prev_col_element):
            print()
            print("*"*40)
            print("Check at {} in {}".format(csv_element_2D([row, col]), nw_input[sheet]+".csv"))
            raise CktEx.AdjacentJumpError


        if not (next_row_element or prev_row_element or next_col_element or prev_col_element):
            print()
            print("*"*40)
            print("Check branch continuity next to jump label {} at {} in {}".format(
                x_matrix[sheet][row][col], csv_element_2D([row, col]), nw_input[sheet]+".csv"
            ))
            raise CktEx.BrokenBranchError

    # Jump must have only one element adjacent to it.
        if ("exist" in next_row_element):
            if ("exist" in next_col_element or "exist" in prev_row_element or \
                "exist" in prev_col_element):
                print()
                print("*"*40)
                print("Check jump at {} in {}".format(csv_element_2D([row, col]), nw_input[sheet]+".csv"))
                raise CktEx.JumpNotExtremeError
            else:
                x_jump.append([sheet, row, col, x_matrix[sheet][row][col], "down"])

        elif ("exist" in next_col_element):
            if ("exist" in next_row_element or "exist" in prev_row_element or \
                "exist" in prev_col_element):
                print()
                print("*"*40)
                print("Check jump at {} in {}".format(csv_element_2D([row, col]), nw_input[sheet]+".csv"))
                raise CktEx.JumpNotExtremeError
            else:
                x_jump.append([sheet, row, col, x_matrix[sheet][row][col], "right"])

        elif ("exist" in prev_row_element):
            if ("exist" in next_row_element or "exist" in next_col_element or \
                "exist" in prev_col_element):
                print()
                print("*"*40)
                print("Check jump at {} in {}".format(csv_element_2D([row, col]), nw_input[sheet]+".csv"))
                raise CktEx.JumpNotExtremeError
            else:
                x_jump.append([sheet, row, col, x_matrix[sheet][row][col], "up"])

        elif ("exist" in prev_col_element):
            if ("exist" in next_row_element or "exist" in next_col_element or \
                "exist" in prev_row_element):
                print()
                print("*"*40)
                print("Check jump at {} in {}".format(csv_element_2D([row, col]), nw_input[sheet]+".csv"))
                raise CktEx.JumpNotExtremeError
            else:
                x_jump.append([sheet, row, col, x_matrix[sheet][row][col], "left"])

    return



def node_checking(x_mat, x_list, sheet, row, col, x_row, x_col):
    """
    A node is defined as a junction of 3 or more branches.
    This function tests whether an element of the circuit
    is a node.
    """

    if ((row==0 and col==0) or (row==x_row-1 and col==x_col-1) or \
        (row==0 and col==x_col-1) or (row==x_row-1 and col==0)):
        # If its a corner point it can't be a node.
        # This prevents array index going out of range.
        pass
        # The next cases, can't be outer edges or corner points.
    else:
        if (row==0):
            # If it is the first row,
            # check if the element in the next and
            # previous columns and same row are connected.
            if not (x_mat[sheet][row][col+1]=='' or x_mat[sheet][row][col-1]==''):
                # Then check if the element in next row and
                # same column is connected. Look for a T junction.
                if not (x_mat[sheet][row+1][col]==''):
                    x_list.append([sheet, row, col])
        if (row==x_row-1):
            # If it is the last row,
            # check if the elements in the next and
            # previous columns and same row are connected.
            if not (x_mat[sheet][row][col+1]=='' or x_mat[sheet][row][col-1]==''):
                if not (x_mat[sheet][row-1][col]==''):
                    # Then check if element in the previous row and
                    # same column is connected. Look for a T junction.
                    x_list.append([sheet, row, col])
        if (col==0):
            # If it is the first column,
            # check if the element in the next column and
            # same row is connected.
            if not (x_mat[sheet][row][col+1]==''):
                # Then check if the elements in next and
                # previous row and same column are connected.
                # Look for a T junction.
                if not (x_mat[sheet][row+1][col]=='' or x_mat[sheet][row-1][col]==''):
                    x_list.append([sheet, row, col])
        if (col==x_col-1):
            # If it is the last column,
            # check if the element in the previous column and
            # same row is connected.
            if not (x_mat[sheet][row][col-1]==''):
                # Then check if the elements in next and
                # previous row and same column are connected.
                # Look for a T junction.
                if not (x_mat[sheet][row+1][col]=='' or x_mat[sheet][row-1][col]==''):
                    x_list.append([sheet, row, col])

        if (row>0 and row<x_row-1 and col>0 and col<x_col-1):
            # If the element is not on the outer boundary
            if (x_mat[sheet][row][col+1]!='' and x_mat[sheet][row][col-1]!=''):
                # Check if the elements in next and
                # previous columns and same row are connected
                if (x_mat[sheet][row+1][col]!='' or x_mat[sheet][row-1][col]!=''):
                    # Then check if elements in either the next and
                    # previous row and same column are connected
                    x_list.append([sheet, row, col])
            elif (x_mat[sheet][row+1][col]!='' and x_mat[sheet][row-1][col]!=''):
                # Check if the elements in next and
                # previous rows and same column are connected
                if (x_mat[sheet][row][col+1]!='' or x_mat[sheet][row][col-1]!=''):
                    # Then check if elements in either the next and
                    # previous column and same row are connected
                    x_list.append([sheet, row, col])

    return


def jump_node_check(x_mat, x_list, jdir, row, nw_input):
    """
    This function checks whether a node is next to
    a jump label and raises an exception.
    """

    n_sheet = x_list[row][0]
    n_row = x_list[row][1]
    n_col = x_list[row][2]
    if (jdir=="up"):
        if (len(x_mat[n_sheet][n_row-1][n_col])>3):
            if (x_mat[n_sheet][n_row-1][n_col].lower()[0:4]=="jump"):
                print()
                print("*"*40)
                print("Check jump at {} in sheet {}.".format(
                    csv_element_2D([n_row-1, n_col]), nw_input[n_sheet]+".csv")
                )
                raise CktEx.JumpAdjacentNodeError

    if (jdir=="down"):
        if (len(x_mat[n_sheet][n_row+1][n_col])>3):
            if (x_mat[n_sheet][n_row+1][n_col].lower()[0:4]=="jump"):
                print()
                print("*"*40)
                print("Check jump at {} in sheet {}.".format(
                    csv_element_2D([n_row+1, n_col]), nw_input[n_sheet]+".csv")
                )
                raise CktEx.JumpAdjacentNodeError

    if (jdir=="left"):
        if (len(x_mat[n_sheet][n_row][n_col-1])>3):
            if (x_mat[n_sheet][n_row][n_col-1].lower()[0:4]=="jump"):
                print()
                print("*"*40)
                print("Check jump at {} in sheet {}.".format(
                    csv_element_2D([n_row, n_col-1]), nw_input[n_sheet]+".csv"))
                raise CktEx.JumpAdjacentNodeError

    if (jdir=="right"):
        if (len(x_mat[n_sheet][n_row][n_col+1])>3):
            if (x_mat[n_sheet][n_row][n_col+1].lower()[0:4]=="jump"):
                print()
                print("*"*40)
                print("Check jump at {} in sheet {}.".format(
                    csv_element_2D([n_row, n_col+1]), nw_input[n_sheet]+".csv"))
                raise CktEx.JumpAdjacentNodeError

    return



def jump_move(x_mat, x_jump, x_element, pos):
    """
    This function connects two branch segments that
    have the same jump label. Each jump label has a
    branch direction that indicates the adjacent element
    on the branch segment and the direction of jump.
    """

    jump_trace = x_mat[x_element[0]][x_element[1]][x_element[2]]
    nxt_sheet = x_jump[jump_trace][pos][0][0]
    if (x_jump[jump_trace][pos][1] == "left"):
        nxt_row = x_jump[jump_trace][pos][0][1]
        nxt_col = x_jump[jump_trace][pos][0][2] - 1
        jmp_exec = "left"
    elif (x_jump[jump_trace][pos][1] == "right"):
        nxt_row = x_jump[jump_trace][pos][0][1]
        nxt_col = x_jump[jump_trace][pos][0][2] + 1
        jmp_exec = "right"
    elif (x_jump[jump_trace][pos][1] == "up"):
        nxt_row = x_jump[jump_trace][pos][0][1] - 1
        nxt_col = x_jump[jump_trace][pos][0][2]
        jmp_exec = "up"
    elif (x_jump[jump_trace][pos][1] == "down"):
        nxt_row = x_jump[jump_trace][pos][0][1] + 1
        nxt_col = x_jump[jump_trace][pos][0][2]
        jmp_exec = "down"

    return [jmp_exec, nxt_sheet, nxt_row, nxt_col]


def branch_jump(x_mat, x_jump, x_element):
    """
    If a jump is encountered.
    Look for the label in the jump_matrix dictionary
    Check which element has been encountered.
    Check the co-ordinates of the other element and
    the sense of movement.
    Depending on the sense of movement, update
    the new co-ordinates with respect
    to the other element
    Add a flag to show which direction movement
    has taken place
    To ensure that we don't go back
    from the next element after the jump.
    """

    nxt_sheet = x_element[0]
    nxt_row = x_element[1]
    nxt_col = x_element[2]
    jump_exec=""

    if (len(x_mat[nxt_sheet][nxt_row][nxt_col])>3):
        if (x_mat[nxt_sheet][nxt_row][nxt_col].lower()[0:4] == "jump"):
            jump_trace=x_mat[nxt_sheet][nxt_row][nxt_col]
            if (x_jump[jump_trace][0][0] == [nxt_sheet, nxt_row, nxt_col]):
                jump_exec, nxt_sheet, nxt_row, nxt_col = \
                jump_move(x_mat, x_jump, x_element, 1)
            elif (x_jump[jump_trace][1][0] == [nxt_sheet, nxt_row, nxt_col]):
                jump_exec, nxt_sheet, nxt_row, nxt_col = \
                jump_move(x_mat, x_jump, x_element, 0)

    return [jump_exec, nxt_sheet, nxt_row, nxt_col]



def branch_advance(x_mat, x_iter, nxt_elem, jmp_exec):
    """
    Advancing one element in a branch
    Checking for jump direction
    to make sure we don't go back.
    """

    nxt_sheet = nxt_elem[0]
    nxt_row = nxt_elem[1]
    nxt_col = nxt_elem[2]

    # This temporary variable is to ensure,
    # two advancements don't take place in one loop.
    branch_proceed = 0
    if ((nxt_col>0) and branch_proceed==0):
        # We are trying to go left, so check if we didn't jump right.
        if (x_mat[nxt_sheet][nxt_row][nxt_col-1] != '' and jmp_exec!="right"):
            # Next check is if we are going backwards.
            if not ([nxt_sheet, nxt_row, nxt_col-1] in x_iter):
                nxt_col = nxt_col-1
                branch_proceed = 1
                # Set jump to null after a movement. We can't go back anyway.
                jmp_exec = ""


    if ((nxt_row>0) and branch_proceed==0):
        # We are trying to go up, so check if we didn't jump down.
        if (x_mat[nxt_sheet][nxt_row-1][nxt_col] != '' and jmp_exec!="down"):
            if not ([nxt_sheet, nxt_row-1, nxt_col] in x_iter):
                nxt_row = nxt_row - 1
                branch_proceed = 1
                # Set jump to null after a movement. We can't go back anyway.
                jmp_exec = ""


    if ((nxt_col<len(x_mat[nxt_sheet][nxt_row])-1) and branch_proceed==0):
        # We are trying to go right, so check if we didn't jump left.
        if (x_mat[nxt_sheet][nxt_row][nxt_col+1] != '' and jmp_exec!="left"):
            if not ([nxt_sheet, nxt_row, nxt_col+1] in x_iter):
                nxt_col = nxt_col + 1
                branch_proceed = 1
                # Set jump to null after a movement. We can't go back anyway.
                jmp_exec = ""


    if ((nxt_row<len(x_mat[nxt_sheet])-1) and branch_proceed==0):
        # We are trying to go down, so check if we didn't jump up.
        if (x_mat[nxt_sheet][nxt_row+1][nxt_col] != '' and jmp_exec!="up"):
            if not ([nxt_sheet, nxt_row+1, nxt_col] in x_iter):
                nxt_row = nxt_row + 1
                branch_proceed = 1
                # Set jump to null after a movement. We can't go back anyway.
                jmp_exec = ""

    return [jmp_exec, nxt_sheet, nxt_row, nxt_col]



def determine_nodes_branches(conn_matrix, nw_input):
    """
    Takes as input the name of the matrix that
    contains the network map. Output is the
    node_list and branch_map between nodes.
    """

    conn_sheets = len(conn_matrix)

    # List of jumps labels
    jump_list = []
    # Structure of jump_list
    # sheet, row, column, jump_label, direction

    # Create a dictionary of jumps -
    # for each jump label - there is a list with two elements.
    jump_matrix = {}
    # Structure of jump_matrix
    # label: [[[sheet, row, col], "dir"], [[sheet, row, col], "dir"]]

    # Check for nodes
    node_list = []
    # Structure of node_list
    # [sheet, row, column]

    for sheet in range(conn_sheets):

        conn_rows = len(conn_matrix[sheet])
        conn_columns = len(conn_matrix[sheet][0])

        # Check for jump sanity
        for c1 in range(conn_rows):
            for c2 in range(conn_columns):
                jump_checking(conn_matrix, jump_list, sheet, c1, c2, conn_rows, conn_columns, nw_input)


    for c1 in range(len(jump_list)):
        jump_count = 1
        for c2 in range(len(jump_list)):
            if not c1==c2:
                if jump_list[c1][3]==jump_list[c2][3]:
                    frst_jmp = jump_list[c1]
                    scd_jmp = jump_list[c2]
                    jump_matrix[frst_jmp[3]] = [[[frst_jmp[0], frst_jmp[1], frst_jmp[2]], frst_jmp[4]],\
                        [[scd_jmp[0], scd_jmp[1], scd_jmp[2]], scd_jmp[4]]]
                    jump_count = jump_count+1

        if (jump_count<2):
            print()
            print("*"*40)
            print("Check jump label {} at {} in sheet {}".format(
                jump_list[c1][3], csv_element_2D([jump_list[c1][1], jump_list[c1][2]]), \
                nw_input[jump_list[c1][0]]+".csv"))
            raise CktEx.SingleJumpError
        elif (jump_count>2):
            print()
            print("*"*40)
            print("Check jump label {} at {} in sheet {}".format(
                jump_list[c1][3], csv_element_2D([jump_list[c1][1], jump_list[c1][2]]), \
                nw_input[jump_list[c1][0]]+".csv"))
            del jump_matrix[jump_list[c1][3]]
            raise CktEx.MultipleJumpError


    for sheet in range(conn_sheets):
        conn_rows = len(conn_matrix[sheet])
        conn_columns = len(conn_matrix[sheet][0])
        for c1 in range(conn_rows):
            for c2 in range(conn_columns):
                curr_element = {"exist":0, "jump":1}
                jump_sanity(conn_matrix, curr_element, sheet, c1, c2)

                if ("exist" in curr_element):
                    node_checking(conn_matrix, node_list, sheet, c1, c2, conn_rows, conn_columns)
                else:
                    pass


    # Map of branches between nodes in node_list
    branch_map = []

    # Creating a square of the dimension
    # of (node_list) x (node_list).
    # Each element will be a list of the
    # series connection of branches between the nodes.
    for c1 in range(len(node_list)):
        branch_rows = []
        for c2 in range(len(node_list)):
            branch_rows.append([])
        branch_map.append(branch_rows)

    # List of branches between nodes
    branch_list=[]

    # Generate a search rule for each node.
    # The concept is to start at a node and
    # search until another node is reached.
    node_iter_rule = []
    for c1 in range(len(node_list)):
        node_sheet = node_list[c1][0]
        node_row = node_list[c1][1]
        node_column = node_list[c1][2]
        conn_rows = len(conn_matrix[node_sheet])
        conn_columns = len(conn_matrix[node_sheet][0])

        iter_rule={"left":0, "down":1, "right":2, "up":3}

        # For nodes in the outer edges,
        # the rules going outwards will be removed.
        if (node_row==0):
            del(iter_rule["up"])
        if (node_row==conn_rows-1):
            del(iter_rule["down"])
        if (node_column==0):
            del(iter_rule["left"])
        if (node_column==conn_columns-1):
            del(iter_rule["right"])

        # Depending on the non-existence of elements
        # in a direction, those rules will be removed.
        if (node_row>0):
            if (conn_matrix[node_sheet][node_row-1][node_column]==''):
                del(iter_rule["up"])

        if (node_row<conn_rows-1):
            if (conn_matrix[node_sheet][node_row+1][node_column]==''):
                del(iter_rule["down"])

        if (node_column>0):
            if (conn_matrix[node_sheet][node_row][node_column-1]==''):
                del(iter_rule["left"])

        if (node_column<conn_columns-1):
            if (conn_matrix[node_sheet][node_row][node_column+1]==''):
                del(iter_rule["right"])

        node_iter_rule.append(iter_rule)


    # Check if a jump is not next to a node.
    for c1 in range(len(node_list)):
        for jump_check_dir in node_iter_rule[c1].keys():
            jump_node_check(conn_matrix, node_list, jump_check_dir, c1, nw_input)


    # For each node in node_list perform the search operation.
    # Each node has a list of possible search rules.
    # Perform a search for each rule.
    # From the starting node, advance in the direction of the rule.
    # After advancing, check if the next element is a node.
    # If it is a node, stop.
    # If it is not a node, there can be only two directions of movement.
    # Move in a direction and check if an element exists.
    # If it exists, check if it is not already an element encountered -
    # shouldn't be moving backwards.
    # If a new element is encountered,
    # update the element in branch iter and continue.

    for c1 in range(len(node_list)):
        # Iterate through every node found
        node_sheet = node_list[c1][0]
        node_row = node_list[c1][1]
        node_column = node_list[c1][2]
        conn_rows = len(conn_matrix[node_sheet])
        conn_columns = len(conn_matrix[node_sheet][0])

        for branch_dir in node_iter_rule[c1].keys():
            # Move in every direction possible
            # for every node
            branch_iter = []
            branch_iter.append([node_sheet, node_row, node_column])

            # Initial advancement.
            if (branch_dir=="left"):
                if (node_column>0):
                    next_node_row = node_row
                    next_node_column = node_column-1
            if (branch_dir=="down"):
                if (node_row<conn_rows-1):
                    next_node_row = node_row+1
                    next_node_column = node_column
            if (branch_dir=="right"):
                if (node_column<conn_columns-1):
                    next_node_row = node_row
                    next_node_column = node_column+1
            if (branch_dir=="up"):
                if (node_row>0):
                    next_node_row = node_row-1
                    next_node_column = node_column

            # As there cannot be a jump next to a node
            next_node_sheet = node_sheet

            # This variable is used when jumps are encountered.
            jump_executed = ""

            # Termination condition - next element is a node.
            while not ([next_node_sheet, next_node_row, next_node_column] in node_list):

                # If a jump is encountered.
                # Look for the label in the jump_matrix dictionary
                # Check which element has been encountered.
                # Check the co-ordinates of the other element and
                # the sense of movement.
                # Depending on the sense of movement, update
                # the new co-ordinates with respect
                # to the other element
                # Add a flag to show which direction movement
                # has taken place
                # To ensure that we don't go back
                # from the next element after the jump.
                next_element = [next_node_sheet, next_node_row, next_node_column]

                jump_executed, next_node_sheet, next_node_row, next_node_column = \
                branch_jump(conn_matrix, jump_matrix, next_element)

                branch_iter.append([next_node_sheet, next_node_row, next_node_column])

                next_element = [next_node_sheet, next_node_row, next_node_column]
                jump_executed, next_node_sheet, next_node_row, next_node_column = \
                    branch_advance(conn_matrix, branch_iter, next_element, \
                                jump_executed)


                # If no advancement is possible, it means circuit is broken.
                # Can improve on this error message later.
                if ([next_node_sheet, next_node_row, next_node_column] in branch_iter):
                    print()
                    print("*"*40)
                    #print conn_matrix[next_node_sheet][next_node_row-1][next_node_column]
                    print("Check branch continuity at {} in sheet {}".format(
                        csv_element_2D([next_node_row, next_node_column]), nw_input[next_node_sheet]+".csv"))
                    raise CktEx.BrokenBranchError


            else:
                branch_iter.append([next_node_sheet, next_node_row, next_node_column])
                next_elem_index = node_list.index([next_node_sheet, next_node_row, next_node_column])
                branch_map[c1][next_elem_index].append(branch_iter)

    return [node_list, branch_map]



def loop_copy(loop_inp):
    """
    Will return a copy of a loop list
    Used when a change needs to be made.
    """

    loop_op = []
    for c1 in range(len(loop_inp)):
        row_vector = []
        for c2 in range(len(loop_inp[c1])):
            row_vector.append(loop_inp[c1][c2])
        loop_op.append(row_vector)

    return loop_op



def check_loop_repeat(lp_iter, lp_list):
    """
    Will return 1 if the loop already
    exists if the loop_list found so far.
    """

    # Make a copy of the entire loop list
    # found so far. Just in case.
    list_cmp = loop_copy(lp_list)

    # As a default, loop is not repeated
    # A single instance of repitition will
    # set it to 1.
    lp_repeat = 0
    # Go through every loop found
    # so far
    for c1 in range(len(list_cmp)):
        # Make a copy of the loop being checked
        iter_cmp = loop_copy(lp_iter)
        # Move in the reverse direction of the loop
        # This is because elements are deleted
        # as they are found.
        for c2 in range(len(iter_cmp)-1, -1, -1):
            # Check if the element is found or if the
            # symmetrical element is found in any of
            # the loops found so far.
            # Because they are the same.
            if ([iter_cmp[c2][0], iter_cmp[c2][1]]  in list_cmp[c1]) or \
            ([iter_cmp[c2][1], iter_cmp[c2][0]]  in list_cmp[c1]):

                # If so, remove the element
                iter_cmp.remove(iter_cmp[c2])

        # If all element have been deleted
        # it means the loop exists
        if not iter_cmp:
            lp_repeat = 1

    return lp_repeat



def loop_addition(br_map, nd_list, lp_list, curr_lp_iter, lp_update, curr_elem, main_loops):
    """
    Take a new element of br_map in any direction.
    Check for a parallel branch at that element.
    Add that element if not already there in the temporary loop.
    """

    row = curr_elem[0]
    col = curr_elem[1]

    # Check if there is an element
    if br_map[row][col]:

        # Temp list to make copies
        # of loops found
        row_vec = []
        for item in curr_lp_iter:
            row_vec.append(item)

        # Check if an element has been
        # encountered before
        # not going back and forth that is
        if not (([row, col] in row_vec) or ([col, row] in row_vec)):
            # Add the element found
            lp_update.append(row_vec)
            lp_update[main_loops].append([row, col])
            # Update the main loops counter
            main_loops += 1
        # If an element has not been found
        # or is a duplicate, lp_update
        # won't contain it.

        #all_loops = all_loops+main_loops

    return main_loops




def loop_closing(br_map, lp_list, nd_list, lp_update, c1):
    """
    The check imposed is whether the loop has the same
    elements as any other loops already found in lp_list.
    """


    # Check if the loop is new even
    # if all nodes have been passed through.
    lp_exist = "found"
    if not check_loop_repeat(lp_update[c1], lp_list):
        lp_exist = "not_found"

    if lp_exist=="not_found":
        # Add that loop to loop list
        lp_list.append(lp_update[c1])
        # Remove the loop from the temp
        # variable.
        del lp_update[c1]

    return



def loop_horiz(br_map, nd_list, lp_list, lp_iter, elem, lp_map_list):
    """
    Moves horizontally in a loop find.
    Looks for every element in a particular column of br_map.
    Each element is added onto the exiting loops.
    """

    # lp_list is the loops found.
    # lp_iter is the list of loops as they are being identified.
    # Those that are loops will be added to lp_list.

    no_nodes = len(br_map)

    start_row = elem[0]
    start_col = elem[1]

    # Temp list to make copies
    # of exisiting lists
    # if elements exist on that row
    lp_update = []
    # Counter for number
    # of elements found in the row
    c2=0
    for c1 in range(len(lp_iter)):
        # Set loop row and counter
        # to the latest element
        # in lp_iter
        loop_row = lp_iter[c1][-1][0]
        loop_column = lp_iter[c1][-1][1]

        # Start from element in next column
        # to end of matrix
        #for c3 in range(loop_column+1, no_nodes):
        for c3 in range(0, no_nodes):
            curr_elem = [loop_row, c3]
            c2 = loop_addition(br_map, nd_list, lp_list, lp_iter[c1], lp_update, curr_elem, c2)


    any_loop_closes = "no"
    c1 = len(lp_update)-1

    while any_loop_closes=="no" and c1>=0:

        # End condition
        # Latest element has ending or starting node
        # Same as last element of first branch
        last_elem_frst = br_map[start_row][start_col][0][-1]
        frst_elem_curr = br_map[lp_update[c1][-1][0]][lp_update[c1][-1][1]][0][0]
        last_elem_curr = br_map[lp_update[c1][-1][0]][lp_update[c1][-1][1]][0][-1]

        if (frst_elem_curr==last_elem_frst or \
            last_elem_curr==last_elem_frst):

            loop_closing(br_map, lp_list, nd_list, lp_update, c1)
            any_loop_closes = "yes"

        c1 -= 1


    if any_loop_closes=="no":
        # lp_iter will be the same as lp_update
        lp_iter = []
        for c1 in range(len(lp_update)):
            lp_iter.append(lp_update[c1])
    else:
        lp_iter = []

    # lp_iter contains ongoing loops
    # Closed loops are moved to lp_list
    # Broken loops are dropped

    return lp_iter




def loop_vert(br_map, nd_list, lp_list, lp_iter, elem, lp_map_list):
    """
    Moves vertically in a loop find.
    Looks for every element in a particular column of br_map.
    Each element is added onto the exiting loops.
    """

    # lp_list is the loops found.
    # lp_iter is the list of loops as they are being identified.
    # Those that are loops will be added to lp_list.
    no_nodes = len(br_map)

    start_row = elem[0]
    start_col = elem[1]

    # Temp list to make copies
    # of exisiting lists
    # if elements exist on that column
    lp_update = []
    # Counter for number
    # of elements found in the column
    c2 = 0
    for c1 in range(len(lp_iter)):
        # Set loop row and counter
        # to the latest element
        # in lp_iter
        loop_row = lp_iter[c1][-1][0]
        loop_column = lp_iter[c1][-1][1]
        # Start from element from first row
        # to end of column
        for c3 in range(0, no_nodes):
            curr_elem = [c3, loop_column]
            c2 = loop_addition(br_map, nd_list, lp_list, lp_iter[c1], lp_update, curr_elem, c2)



    any_loop_closes = "no"
    c1 = len(lp_update)-1

    while any_loop_closes=="no" and c1>=0:
        # End condition
        # Latest element has ending or starting node
        # Same as last element of first branch
        last_elem_frst = br_map[start_row][start_col][0][-1]
        frst_elem_curr = br_map[lp_update[c1][-1][0]][lp_update[c1][-1][1]][0][0]
        last_elem_curr = br_map[lp_update[c1][-1][0]][lp_update[c1][-1][1]][0][-1]

        if (frst_elem_curr==last_elem_frst or \
            last_elem_curr==last_elem_frst):

            loop_closing(br_map, lp_list, nd_list, lp_update, c1)
            any_loop_closes = "yes"

        c1 -= 1

    if any_loop_closes=="no":
        # lp_iter will be the same as lp_update
        lp_iter = []
        for c1 in range(len(lp_update)):
            lp_iter.append(lp_update[c1])
    else:
        lp_iter = []

    # lp_iter contains ongoing loops
    # Closed loops are moved to lp_list
    # Broken loops are dropped

    return lp_iter




def find_loop(br_map, nd_list, lp_list, lp_iter, elem, lp_map_list):
    """
    Find the loops from info on branches and
    nodes. The starting point is the first branch in br_map.
    The loops found need not be independent loops.
    """

    no_nodes = len(br_map)

    # First branch
    start_row = elem[0]
    start_col = elem[1]

    # Move right from that element
    # This is the first element
    # In a general sense, the direction is horiz
    loop_dir = "horiz"

    # The termination condition is
    # that there should not be any element
    # in the nd_list. The nodes are deleted
    # as a completed loop contains them.
    # This is to ensure that all the nodes
    # are included in the loops found.
    # To ensure that parallel loops between
    # a few pair of nodes, do not cause
    # loops to be left out, additionally,
    # it is checked whether
    # Loops < Branches - Nodes + 1
#    while (nd_list or lp_count<lp_limit):
    while (lp_iter):
        # Will be executed if we are moving horizontally
        if (loop_dir == "horiz"):
            lp_iter=loop_horiz(br_map, nd_list, lp_list, lp_iter, elem, lp_map_list)
            # Change direction to vertical
            loop_dir = "vert"

        # Will be executed if we are moving vertically
        if (loop_dir == "vert"):
            lp_iter=loop_vert(br_map, nd_list, lp_list, lp_iter, elem, lp_map_list)
            # Change direction to horizontal
            loop_dir = "horiz"

    return



def determine_loops(conn_matrix,  node_list,  branch_map):
    """
    This function determines the number of loops in the
    system from the branch map i.e the nodes and the
    branches between the nodes.
    """

    # Determining the loops
    loop_list = []

    # Loop map is the list of all the node pairs
    # that have branches between them.
    loop_map_list = []
    for c1 in range(len(branch_map)):
        for c2 in range(c1+1, len(branch_map)):
            if branch_map[c1][c2]:
                if [c1, c2] not in loop_map_list:
                    loop_map_list.append([c1, c2])


    # A special check for parallel branches between nodes
    # Add the pair of nodes directly to the loop_list
    for c1 in range(len(loop_map_list)):
        if len(branch_map[loop_map_list[c1][0]][loop_map_list[c1][1]])>1:
            if not check_loop_repeat([loop_map_list[c1], loop_map_list[c1]], loop_list):
                loop_list.append([loop_map_list[c1], loop_map_list[c1]])


    # loop_iter is the list that iteratively checks the
    # loops for continuity and closing. It is initalized
    # to every branch element that exists between
    # two nodes and the search for loops is done.
    for c1 in range(len(branch_map)):
        for c2 in range(len(branch_map[c1])):
            loop_iter = []
            if branch_map[c1][c2]:
                loop_iter.append([[c1, c2]])

            find_loop(branch_map, node_list, loop_list, loop_iter, \
                    [c1, c2], loop_map_list)


    branch_count_check = 0
    for c1 in range(len(branch_map)):
        for c2 in range(c1, len(branch_map[c1])):
            if branch_map[c1][c2]:
                branch_count_check += len(branch_map[c1][c2])

    print("Number of nodes = {}".format(str(len(node_list))))
    print()

    print("Number of branches = {}".format(str(branch_count_check)))
    print()

    loop_count=len(loop_list)
    print("Number of loops = {}".format(str(loop_count)))
    print()


    test_branch_count = 0
    for c1 in range(len(branch_map)):
        for c2 in range(c1+1, len(branch_map[c1])):
            test_branch_count += len(branch_map[c1][c2])


    # Remove any repitions in loop_list
    for c1 in range(len(loop_list)-1):
        for c2 in range(len(loop_list)-1, c1, -1):
            if loop_list[c1]==loop_list[c2]:
                del loop_list[c2]



    # The actual elements from the branches
    # to be entered into the loops
    loop_branches = []

    # Go through every element in loop_list
    for c1 in range(len(loop_list)):
        # If the loop has two elements
        # it means it is a group of
        # parallel branches between nodes
        if len(loop_list[c1])==2:
            curr_br = loop_list[c1][0]
            # Get every permutation of branch pairs possible
            #for c2 in range(len(branch_map[curr_br[0]][curr_br[1]])-1):
            c2 = 0
            for c3 in range(c2+1, len(branch_map[curr_br[0]][curr_br[1]])):
                loop_updt = []

                # Iterate in the forward direction
                for c4 in range(len(branch_map[curr_br[0]][curr_br[1]][c2])):
                    loop_updt.append(branch_map[curr_br[0]][curr_br[1]][c2][c4])
                # Iterate in the reverse direction
                for c4 in range(len(branch_map[curr_br[0]][curr_br[1]][c3])-2, -1, -1):
                    loop_updt.append(branch_map[curr_br[0]][curr_br[1]][c3][c4])

                loop_branches.append(loop_updt)
        else:
            loop_updt = []

            # Go through all elements in the loop
            for c2 in range(0, len(loop_list[c1])-1):

                # Mark two elements in the loop
                # The current and the next element
                curr_br = loop_list[c1][c2]
                curr_br_beg = branch_map[curr_br[0]][curr_br[1]][0][0]
                curr_br_end = branch_map[curr_br[0]][curr_br[1]][0][-1]
                next_br = loop_list[c1][c2+1]
                next_br_beg = branch_map[next_br[0]][next_br[1]][0][0]
                next_br_end = branch_map[next_br[0]][next_br[1]][0][-1]


                curr_dir = "forward"

                # Start stringing the branches together

                # So if it is the first branch
                # Check if the beginning element of the branch
                # is the same as the beginning or ending element
                # of the next branch
                # In that case, the first/current branch
                # is to be reversed
                if not loop_updt:
                    if curr_br_beg==next_br_beg or curr_br_beg==next_br_end:
                        curr_dir = "reverse"

                # If the loop update is in progress
                # check how the current element is linked to
                # the last element on the updated loop
                else:
                    if curr_br_end==loop_updt[-1]:
                        curr_dir = "reverse"


                # Depending on the direction in which
                # an element is to be added to
                # the loop.
                if curr_dir=="forward":
                    for c3 in range(len(branch_map[curr_br[0]][curr_br[1]][0])):
                        loop_updt.append(branch_map[curr_br[0]][curr_br[1]][0][c3])
                else:
                    for c3 in range(len(branch_map[curr_br[0]][curr_br[1]][0])-1, -1, -1):
                        loop_updt.append(branch_map[curr_br[0]][curr_br[1]][0][c3])

            # Repeat for the last element
            next_dir = "forward"
            if next_br_end==loop_updt[-1]:
                next_dir = "reverse"

            if next_dir=="forward":
                for c3 in range(len(branch_map[next_br[0]][next_br[1]][0])):
                    loop_updt.append(branch_map[next_br[0]][next_br[1]][0][c3])
            else:
                for c3 in range(len(branch_map[next_br[0]][next_br[1]][0])-1, -1, -1):
                    loop_updt.append(branch_map[next_br[0]][next_br[1]][0][c3])

            # Remove any repitions in the elements
            # in consecutive elements only
            for c3 in range(len(loop_updt)-1, 0, -1):
                if loop_updt[c3]==loop_updt[c3-1]:
                    del loop_updt[c3]

            loop_branches.append(loop_updt)

    # In the loop finder function, a check is enforced
    # whether a loop has encountered the same branch
    # before but if a loop passes through the same node
    # again, then also, it should not be included as a loop
    for c1 in range(len(loop_branches)-1, -1, -1):
        node_repeat = "no"
        for c2 in range(len(loop_branches[c1])-1):
            for c3 in range(c2+1, len(loop_branches[c1])-1):
                if loop_branches[c1][c2]==loop_branches[c1][c3]:
                    node_repeat = "yes"
        if node_repeat=="yes":
            del loop_branches[c1]

    # The loops are broken up as branches.
    # Each branch are element between two nodes
    for c1 in range(len(loop_branches)):
        row1_branch_list = []
        row1_node_list = []
        for c2 in range(len(node_list)):
            if node_list[c2] in loop_branches[c1]:
                row1_node_list.append(loop_branches[c1].index(node_list[c2]))
        row1_node_list.sort()

        for c2 in range(len(row1_node_list)-1):
            seg_vector = loop_branches[c1][row1_node_list[c2]:row1_node_list[c2+1]+1]
            row1_branch_list.append(seg_vector)

        seg_vector = loop_branches[c1][row1_node_list[c2+1]:len(loop_branches[c1])]
        row1_branch_list.append(seg_vector)

        loop_branches[c1] = row1_branch_list

    return [loop_list, loop_branches]



def determine_circuit_components(conn_matrix, nw_input):
    """
    This function reads the components from the circuit
    matrix.
    """

    components_found = {}

    for sheet in range(len(conn_matrix)):
        for c1 in range(len(conn_matrix[sheet])):
            for c2 in range(len(conn_matrix[sheet][0])):
                elem = conn_matrix[sheet][c1][c2]
                if elem:
                    while elem[0]==" ":
                        elem = elem[1:]
                    while elem[-1]==" ":
                        elem = elem[:-1]

                    # wire is a zero resistance connection
                    if elem.lower()[:4]!="wire":
                        if len(elem.split("_"))==1:
                            jump_det = elem.split("_")[0]
                            if len(jump_det)>3:
                                if jump_det.lower()[0:4]=="jump":
                                    pass
                                else:
                                    print()
                                    print()
                                    print("Error! Component at {} in sheet {} does not have a unique name/tag.".format(
                                        csv_element_2D([c1, c2]), nw_input[sheet]+".csv"))
                                    raise CktEx.MissingComponentTagError
        ## Not sure if the check below is needed.
        ## A tag could be less than three characters.
        ##                    else:
        ##                        print "Error! Component at %s does not have a unique name/tag." %csv_element([sheet, c1, c2])
                        else:
                            [elem_name, elem_tag] = elem.split("_")
                            elem_type = elem_name.lower()
                            while elem_type[0]==" ":
                                elem_type = elem_type[1:]
                            while elem_type[-1]==" ":
                                elem_type = elem_type[:-1]
                            while elem_tag[0]==" ":
                                elem_tag = elem_tag[1:]
                            while elem_tag[-1]==" ":
                                elem_tag = elem_tag[:-1]

                            # Check if component exists
                            if elem_type in CktElem.component_list.keys():
                                # If found for the first time
                                # Create that dictionary element with key
                                # as component type
                                if elem_type not in components_found:
                                    components_found[elem_type] = [[csv_element([sheet, c1, c2]), elem_tag]]
                                else:
                                    # If already found, append it to
                                    # dictionary item with that key.
                                    components_found[elem_type].append([csv_element([sheet, c1, c2]), elem_tag])
                            else:
                                print()
                                print()
                                print("Error! Component at {} in sheet {} doesn't exist.".format(\
                                    csv_element_2D([c1, c2]), nw_input[sheet]+".csv"))
                                raise CktEx.UnidentifiedComponentError


    # Check if a component of the same type has the same tag.
    for items in components_found.keys():
        for c1 in range(len(components_found[items])):
            for c2 in range(len(components_found[items])):
                if c1!=c2:
                    if components_found[items][c1][1]==components_found[items][c2][1]:
                        print()
                        print()
                        print("Duplicate labels found for components of type {} at {} in sheet {} and {} in sheet {}".format(
                            items, csv_element_truncate(components_found[items][c1][0]), \
                            nw_input[csv_element_extract(components_found[items][c1][0])]+".csv", \
                            csv_element_truncate(components_found[items][c2][0]), \
                            nw_input[csv_element_extract(components_found[items][c2][0])]+".csv"))

                        raise CktEx.DuplicateComponentLabelError


    component_objects = {}

    for items in components_found.keys():
        # Take every type of component found
        # item -> resistor, inductor etc
        for c1 in range(len(components_found[items])):
            # Each component type will be occurring
            # multiple times. Iterate through every find.
            # The list corresponding to each component is
            # the unique cell position in the spreadsheet
            component_objects[components_found[items][c1][0]] = \
                    CktElem.component_list[items](c1+1, components_found[items][c1][0], components_found[items][c1][1], nw_input)


    return [components_found,  component_objects]



def classify_components(components_found,  component_objects):
    """
    Make lists of components that have voltages, that are meters,
    and that can be controlled. These lists determine the size of the
    system matrices, the number of data points that need to be
    stored and whether a control file needs to be generated.
    """

    # The list to be reurned.
    bundled_list_of_components = []

    source_list = []

    for items in components_found.keys():
        for c1 in range(len(components_found[items])):
            if component_objects[components_found[items][c1][0]].has_voltage=="yes":
                source_list.append(components_found[items][c1][0])

    bundled_list_of_components.append(source_list)

    meter_list = []

    for items in components_found.keys():
        for c1 in range(len(components_found[items])):
            if component_objects[components_found[items][c1][0]].is_meter=="yes":
                meter_list.append(components_found[items][c1][0])

    bundled_list_of_components.append(meter_list)

    controlled_elements = []

    for items in components_found.keys():
        for c1 in range(len(components_found[items])):
            if component_objects[components_found[items][c1][0]].has_control=="yes":
                controlled_elements.append(components_found[items][c1][0])

    bundled_list_of_components.append(controlled_elements)

    return bundled_list_of_components



def update_branches_loops(loop_branches, source_list):
    """
    This function creates a list called branch_params where
    the branches along with their parameters such as R, L and
    voltages are added. Simultaneously, a list called system loops
    is created where the branches of each loop are added. Another
    check is make to ensure that branches are not repeated by
    reversing them.
    """

    # A array of all the loops of the system
    # including common branches between loops.
    system_loops = []
    for c1 in range(len(loop_branches)):
        system_loops.append([])


    for c1 in range(len(loop_branches)):
        # The diagonal elements of system_loops
        # will be the loops themselves.
        for c2 in range(len(loop_branches[c1])):
            diag_elem = []
            for c3 in range(len(loop_branches[c1][c2])):
                diag_elem.append(loop_branches[c1][c2][c3])
            diag_elem.append("forward")
            system_loops[c1].append(diag_elem)


    # This list contains every branch and
    # at the end contains the elements that
    # would go into A, B and E matrices.
    branch_params = []

    for c1 in range(len(system_loops)):
        # Check if a branch has already been added to
        # branch_params.
        for c2 in range(len(system_loops[c1])):
            branch_found = "no"
            for c4 in range(len(branch_params)):
                if system_loops[c1][c2][:-1]==branch_params[c4][:-1]:
                    branch_found = "yes"

            # Matrix B will have the number
            # of entries equal to the number
            # of sources.
            if branch_found=="no":
                source_add = []
                for c3 in range(len(source_list)):
                    source_add.append(0.0)
                branch_add = system_loops[c1][c2][:-1]
                params_add = []
                params_add.append([0.0,0.0])
                params_add.append(source_add)
                params_add.append(0.0)
                params_add.append(0.0)
                params_add.append(0.0)
                params_add.append(0)
                branch_add.append(params_add)
                branch_params.append(branch_add)


    # This is an additional layer of check to make sure
    # that none of the branches in branch_params is the
    # reverse of another.
    for c1 in range(len(branch_params)-1, -1, -1):
        # Start from the last branch and compute
        # the reverse.
        # Make a copy
        check_br_reverse = []
        for c2 in range(len(branch_params[c1])-1):
            check_br_reverse.append(branch_params[c1][c2])
        # Reverse the copy
        for c2 in range(len(check_br_reverse)//2):
            check_br_reverse[c2], check_br_reverse[len(check_br_reverse)-1-c2] = \
                                  check_br_reverse[len(check_br_reverse)-1-c2], check_br_reverse[c2]

        # Iterate through the branches.
        c2=0
        while c2<len(branch_params):
            # Check if the reverse of the branch c1
            # is equal to the current branch
            if check_br_reverse==branch_params[c2][:-1]:
                # In this case, two things need to be done
                # Find out where the branch occurs in
                # system_loops and reverse those branches
                # Second, delete that branch from branch_params

                # There will be two instances of the branch
                # One with a forward appended at the end
                check_br_fwd = []
                for c3 in range(len(branch_params[c1][:-1])):
                    check_br_fwd.append(branch_params[c1][c3])
                check_br_fwd.append("forward")

                # The other with a reverse appended at the end.
                check_br_rev = []
                for c3 in range(len(branch_params[c1][:-1])):
                    check_br_rev.append(branch_params[c1][c3])
                check_br_rev.append("reverse")

                # Look through the entire system_loops matrix
                for c3 in range(len(system_loops)):
                    # Check if the branch with forward is found.
                    if (check_br_fwd in system_loops[c3]):
                        # Mark the position
                        ex_br_pos = system_loops[c3].index(check_br_fwd)
                        # Mark the direction
                        ex_br_dir = system_loops[c3][ex_br_pos][-1]
                        # Delete the branch
                        del system_loops[c3][ex_br_pos]

                        # Add the earlier branch found branch_params[c2]
                        # But reverse the direction of the branch just
                        # deleted.
                        if ex_br_dir=="forward":
                            new_br = []
                            for c5 in range(len(branch_params[c2])-1):
                                new_br.append(branch_params[c2][c5])
                            new_br.append("reverse")
                            system_loops[c3].append(new_br)

                        else:
                            new_br = []
                            for c5 in range(len(branch_params[c2])-1):
                                new_br.append(branch_params[c2][c5])
                            new_br.append("forward")
                            system_loops[c3].append(new_br)

                    # Repeat the process with the branch with reverse
                    if (check_br_rev in system_loops[c3]):
                        ex_br_pos = system_loops[c3].index(check_br_rev)
                        ex_br_dir = system_loops[c3][ex_br_pos][-1]
                        del system_loops[c3][ex_br_pos]
                        if ex_br_dir=="forward":
                            new_br = []
                            for c5 in range(len(branch_params[c2])-1):
                                new_br.append(branch_params[c2][c5])
                            new_br.append("reverse")
                            system_loops[c3].append(new_br)

                        else:
                            new_br = []
                            for c5 in range(len(branch_params[c2])-1):
                                new_br.append(branch_params[c2][c5])
                            new_br.append("forward")
                            system_loops[c3].append(new_br)

                # Delete the latest branch because it is a reverse
                del branch_params[c1]
            c2 += 1

    return [system_loops, branch_params]



def delete_empty_branches(system_loops, branch_params, node_list, component_objects):
    """
    Deletes the empty branches from branch params and brings the nodes connected by
    empty branches together as short nodes.
    """

    shortnode_list = []
    shortbranch_list = []

    for c1 in range(len(branch_params)):
        # If any element of a branch is a component in the library list,
        # the branch is not a short branch.
        branch_short="yes"
        for c2 in range(len(branch_params[c1])):
            try:
                comp_pos = csv_element(branch_params[c1][c2])
                component_objects[comp_pos]
            except:
                pass
            else:
                branch_short="no"

        # For every short branch, append the nodes to the shortnode list
        # and the branches to the short branch list.
        if branch_short=="yes":
            start_node = node_list.index(branch_params[c1][0])
            end_node = node_list.index(branch_params[c1][-2])

            if not (([start_node, end_node] in shortnode_list) or ([end_node, start_node] in shortnode_list)):
                shortnode_list.append([start_node, end_node])

            if c1 not in shortbranch_list:
                shortbranch_list.append(c1)


    # The idea is make shortnode_list a list of groups of nodes connected
    # by empty branches.
    any_node_found = "yes"
    while any_node_found=="yes":
        any_node_found = "no"
        c1 = 0
        while c1 < len(shortnode_list):
            for c2 in range(len(shortnode_list)-1, -1, -1):
                if not c1==c2:
                    node_found = "no"
                    for c3 in range(len(shortnode_list[c2])):
                        if c1<len(shortnode_list):
                            if shortnode_list[c2][c3] in shortnode_list[c1]:
                                node_found = "yes"
                                any_node_found = "yes"

                    if node_found=="yes":
                        for c3 in range(len(shortnode_list[c2])):
                            if shortnode_list[c2][c3] not in shortnode_list[c1]:
                                shortnode_list[c1].append(shortnode_list[c2][c3])

                        del shortnode_list[c2]
            c1 += 1


    for c1 in range(len(shortnode_list)):
        shortnode_list[c1].sort()

    shortbranch_list.sort()

    # Delete the short branches from the list of
    # branches because they do not contain
    # any components. Also, delete the branches
    # from the system loops.
    for c1 in range(len(shortbranch_list)-1, -1, -1):
        branch_pos = shortbranch_list[c1]
        for c2 in range(len(system_loops)):
            for c3 in range(len(system_loops[c2])-1, -1, -1):
                if branch_params[branch_pos][:-1]==system_loops[c2][c3][:-1]:
                    del system_loops[c2][c3]

        del branch_params[branch_pos]

    return [shortnode_list, shortbranch_list]



def delete_empty_branches_old(system_loops,  branch_params,  node_list,  component_objects):
    """
    This function determines which branches are empty branches
    and do not contain components but are only wire segments.
    """

    # Finding the shortnodes in the system
    # shortnodes are essentially those nodes that
    # have a zero impedance branch connected to them
    # These branches do NOT have a voltage source.
    # Essentially these are "wire"s.
    # When there is a shortnode, KCL continues to the other node
    # of the zero impedance branch. So the two end
    # nodes of a zero impedance branch have their KCL equations
    # added but their node voltages are not expressed by an equation.
    # The voltages are equated later.

    shortbranch_list = []

    # The complete list of shortnodes
    shortnode_list = []
    for c1 in range(len(node_list)):
        # Each small segment of shortnodes
        current_shortnode = []

        # Check if the node has been found as a shortnode before
        node_found = "no"
        for c2 in range(len(shortnode_list)):
            if c1 in shortnode_list[c2]:
                node_found = "yes"

        # If not add it as a shortnode
        # This is the first node in the current
        # running list. If no other nodes are found,
        # it will be deleted at the next iteration
        # as the node is not a shortnode in that case.
        if node_found=="no":
            current_shortnode.append(c1)

        # Iterate through the remaining nodes
        for c2 in range(len(node_list)):
            # Look for the nodes in both the
            # current list and the complete list
            node_found = "no"
            if c2 in current_shortnode:
                node_found=="yes"

            if node_found=="no":
                for c3 in range(len(shortnode_list)):
                    if c2 in shortnode_list[c3]:
                        node_found = "yes"

            # If the node has not been found, check if it is connected
            # to any of the existing nodes in the current list
            # by branches with zero impedance.
            if node_found=="no":
                for c3 in range(len(branch_params)):

                    branch_short = "yes"
                    for c4 in range(len(branch_params[c3])):
                        try:
                            comp_pos = csv_element(branch_params[c3][c4])
                            component_objects[comp_pos]
                        except:
                            pass
                        else:
                            branch_short = "no"

                    # Check if a branch has zero impedance and no voltage.

                    if branch_short=="yes":
                        if c3 not in shortbranch_list:
                            shortbranch_list.append(c3)

                        # If the current node is the first node in the current
                        # branch being examined, check if any of the nodes
                        # in the current shortnode list are the ending nodes.
                        # If so append the current node to the current super node list
                        if (node_list[c2]==branch_params[c3][0]):
                            for c4 in current_shortnode:
                                if node_list[c4]==branch_params[c3][-2]:
                                    current_shortnode.append(c2)

                        # If the current node is the ending node in the current
                        # branch being examined, check if any of the nodes
                        # in the current shortnode list are the starting nodes.
                        # If so append the current node to the current super node list
                        if (node_list[c2]==branch_params[c3][-2]):
                            for c4 in current_shortnode:
                                if node_list[c4]==branch_params[c3][0]:
                                    current_shortnode.append(c2)


        # There is another possibility
        # A node could be a shortnode, but is connected only
        # to another node which appears later in the node list
        # So, the above calculation will not work as it looks
        # for a node connected to existing shortnodes by zero
        # impedance branches.
        # So essentially it is a rerun to pickup any nodes
        # that were missed the first time.

        # Iterate through existing list of current shortnodes.
        for c2 in current_shortnode:
            # Then look through the entire list of nodes.
            for c3 in range(len(node_list)):
                # Check it is has been found as a shortnode
                # in the current list
                node_found = "no"
                if c3 in current_shortnode:
                    node_found = "yes"

                # Check it has been found elsewhere.
                if node_found=="no":
                    for c4 in range(len(shortnode_list)):
                        if c3 in shortnode_list[c4]:
                            node_found = "yes"


                # Check if the current node is connected to any of the nodes
                # in the current shortnode list by a short branch.
                if node_found=="no":
                    for c5 in range(len(branch_params)):

                        branch_short = "yes"
                        for c6 in range(len(branch_params[c5])):
                            try:
                                comp_pos = csv_element(branch_params[c5][c6])
                                component_objects[comp_pos]
                            except:
                                pass
                            else:
                                branch_short = "no"


                        if branch_short=="yes":
                            if c5 not in shortbranch_list:
                                shortbranch_list.append(c5)

                            # If current node is start node of branch and
                            # end node is an existing shortnode
                            if (node_list[c3]==branch_params[c5][0]):
                                for c6 in current_shortnode:
                                    if (node_list[c6]==branch_params[c5][-2]):
                                        current_shortnode.append(c3)

                            # and vice versa
                            if (node_list[c3]==branch_params[c5][-2]):
                                for c6 in current_shortnode:
                                    if (node_list[c6]==branch_params[c5][0]):
                                        current_shortnode.append(c3)


        # Sort the list of current shortnodes
        # The reason is so that the KCL equations can be added
        # and the first node will contain the sum.
        current_shortnode.sort()

        # If the current super node list has more than
        # one node, there is a zero impedance branch
        # and so it is super node list.
        if len(current_shortnode)>1:
            shortnode_list.append(current_shortnode)

    shortbranch_list.sort()

    # Delete the short branches from the list of
    # branches because they do not contain
    # any components. Also, delete the branches
    # from the system loops.
    for c1 in range(len(shortbranch_list)-1, -1, -1):
        branch_pos = shortbranch_list[c1]
        for c2 in range(len(system_loops)):
            for c3 in range(len(system_loops[c2])-1, -1, -1):
                if branch_params[branch_pos][:-1]==system_loops[c2][c3][:-1]:
                    del system_loops[c2][c3]

        del branch_params[branch_pos]


    return [shortnode_list, shortbranch_list]



def classify_branches(branch_params, component_objects):
    """
    Make lists of branches that have nonlinear elements that can freewheel,
    branches that have inductors, and branches that have voltmeters.
    """

    # The list to be reurned.
    bundled_list_of_branches = []

    # Make a list of the branches that contain
    # nonlinear elements that need to be checked for freewheeling.
    # The list is in circuit_elements.
    nonlinear_freewheel_branches = []
    for c1 in range(len(branch_params)):
        for c2 in range(len(branch_params[c1])):
            try:
                comp_pos = csv_element(branch_params[c1][c2])
                component_objects[comp_pos]
            except:
                pass
            else:
                if component_objects[comp_pos].type in CktElem.nonlinear_freewheel_components:
                    nonlinear_freewheel_branches.append(c1)

    bundled_list_of_branches.append(nonlinear_freewheel_branches)

    # A list of the branches having inductors.
    inductor_list = []
    inductor_stiffness = []
    for c1 in range(len(branch_params)):
        for c2 in range(len(branch_params[c1])):
            try:
                comp_pos = csv_element(branch_params[c1][c2])
                component_objects[comp_pos]
            except:
                pass
            else:
                if component_objects[comp_pos].type=="Inductor":
                    inductor_list.append(c1)
                    inductor_stiffness.append("yes")

    bundled_list_of_branches.append([inductor_list,  inductor_stiffness])

    # Voltage measurement is a little different from
    # the normal loop analysis. Therefore, a separate
    # list for the branches that contain voltmeters
    voltmeter_branches = []
    voltmeter_voltages = []
    for c1 in range(len(branch_params)):
        for c2 in range(len(branch_params[c1])):
            try:
                comp_pos = csv_element(branch_params[c1][c2])
                component_objects[comp_pos]
            except:
                pass
            else:
                if component_objects[comp_pos].type=="Voltmeter":
                    voltmeter_branches.append(c1)
                    voltmeter_voltages.append(0.0)

    bundled_list_of_branches.append([voltmeter_branches, voltmeter_voltages])

    return bundled_list_of_branches



def human_branch_names(branch_params, component_objects):
    """
    This function represents a branch by the components in it
    which makes it easy to read off while debugging loops.
    """

    # This is for convenience is checking loops.
    # This lists out the components in loops by
    # their branch tags.
    branch_tags_in_loops = []
    for c1 in range(len(branch_params)):
        row_string = []
        for c2 in range(len(branch_params[c1])):
            try:
                comp_pos = csv_element(branch_params[c1][c2])
                component_objects[comp_pos]
            except:
                pass
            else:
                row_string.append(component_objects[comp_pos].type + "_"+ component_objects[comp_pos].tag)

        branch_tags_in_loops.append(row_string)

    return branch_tags_in_loops



def determine_kcl_parameters(branch_params,  node_list,  shortnode_list):
    """
    This function determines the matrices need to perform nodal analysis,
    list of nodes for KCL that exclude the short nodes,
    """

    # This list is of those nodes that are used
    # in KCL. All short nodes are consolidated into
    # one node.
    kcl_node_list = []
    for c1 in range(len(node_list)):
        kcl_node_list.append(node_list[c1])

    for c1 in range(len(kcl_node_list)-1, -1, -1):
        extra_node = "no"
        for c2 in range(len(shortnode_list)):
            if c1 in shortnode_list[c2]:
                if c1==shortnode_list[c2][0]:
                    pass
                else:
                    extra_node = "yes"

        if extra_node=="yes":
            del kcl_node_list[c1]


    # Node voltages for nodal analysis
    # corresponding to KCL nodes.
    abridged_node_voltage = []
    for c1 in range(len(kcl_node_list)):
        abridged_node_voltage.append(0.0)


    # A map of all the branches that are incident at
    # every KCL node along with the direction at
    # that node.
    kcl_branch_map = []
    for c1 in range(len(kcl_node_list)):
        row_vector = []
        for c2 in range(len(kcl_node_list)):
            row_vector.append([])
        kcl_branch_map.append(row_vector)


    # A list of all the KCL nodes and the
    # branches incident at every node.
    branches_in_kcl_nodes = []
    for c1 in range(len(kcl_node_list)):
        branches_in_kcl_nodes.append([])


    # Iterate through every branch. Check if the start and end
    # nodes are KCL nodes. If not, the KCL nodes will the first nodes
    # in the short node group that contains the branch terminal nodes.
    # Add the branch number to the map corresponding to the
    # start and end node and add the direction of +1 for the
    # start_node, end_node element and -1 for the end_node, start_node
    # element. Finally, add that branch number to the list of branches
    # in every KCL node.
    for c1 in range(len(branch_params)):
        start_node_pos = node_list.index(branch_params[c1][0])
        if node_list[start_node_pos] not in kcl_node_list:
            start_node_found = "no"
            c2 = 0
            #for c2 in range(len(shortnode_list)):
            while (c2<len(shortnode_list) and start_node_found=="no"):
                if start_node_pos in shortnode_list[c2]:
                    start_node_pos = kcl_node_list.index(node_list[shortnode_list[c2][0]])
                    start_node_found = "yes"
                c2 += 1
        else:
            start_node_pos=kcl_node_list.index(node_list[start_node_pos])

        end_node_pos = node_list.index(branch_params[c1][-2])
        if node_list[end_node_pos] not in kcl_node_list:
            end_node_found = "no"
            c2 = 0
            while (c2<len(shortnode_list) and end_node_found=="no"):
            #for c2 in range(len(shortnode_list)):
                if end_node_pos in shortnode_list[c2]:
                    end_node_pos = kcl_node_list.index(node_list[shortnode_list[c2][0]])
                    end_node_found = "yes"
                c2 += 1
        else:
            end_node_pos = kcl_node_list.index(node_list[end_node_pos])


        if not kcl_branch_map[start_node_pos][end_node_pos]:
            kcl_branch_map[start_node_pos][end_node_pos].append([])
            kcl_branch_map[start_node_pos][end_node_pos].append([])

        kcl_branch_map[start_node_pos][end_node_pos][0].append(c1)
        kcl_branch_map[start_node_pos][end_node_pos][1].append(1.0)

        if not kcl_branch_map[end_node_pos][start_node_pos]:
            kcl_branch_map[end_node_pos][start_node_pos].append([])
            kcl_branch_map[end_node_pos][start_node_pos].append([])

        kcl_branch_map[end_node_pos][start_node_pos][0].append(c1)
        kcl_branch_map[end_node_pos][start_node_pos][1].append(-1.0)


        if c1 not in branches_in_kcl_nodes[start_node_pos]:
            branches_in_kcl_nodes[start_node_pos].append(c1)

        if c1 not in branches_in_kcl_nodes[end_node_pos]:
            branches_in_kcl_nodes[end_node_pos].append(c1)


    # Admittance matrix for nodal analysis
    admittance_matrix = []
    for c1 in range(len(kcl_node_list)):
        row_vector = []
        for c2 in range(len(kcl_node_list)):
            row_vector.append(0.0)
        admittance_matrix.append(row_vector)


    # Source vector used for nodal analysis
    source_vector = []
    for c1 in range(len(kcl_node_list)):
        source_vector.append(0.0)


    return [kcl_node_list, abridged_node_voltage, kcl_branch_map,  \
            branches_in_kcl_nodes, admittance_matrix, source_vector]



def read_circuit_parameters(nw_input, conn_matrix, branch_params, component_objects,  components_found):
    """
    This function reads the parameters of the circuit components by
    using the member function of the component objects.
    """

    parameters_file = []
    for c1 in range(len(nw_input)):
        parameters_file.append(nw_input[c1] + "_params.csv")


    for sheet in range(len(parameters_file)):

        # Check if the *_params.csv file exists.
        try:
            csv_check_values = open(parameters_file[sheet], "r")

        # If not, it has to be created and filled
        # with default values.
        except:
            #param_flag = "no"
            pass

        # Check if any of the components with the same
        # tags are present in nw_params.csv. If so, take
        # those parameters from nw_params.csv and replace
        # the default parameters in the component objects.
        else:
            params_from_file = reading_params(csv_check_values)

            for c1 in range(len(params_from_file)):
                # Remove leading spaces if any
                # The first column is the type of element
                if params_from_file[c1][0][0]==" ":
                    params_from_file[c1][0] = params_from_file[c1][0][1:]

                name_from_file = params_from_file[c1][0].lower()

                # Check if the component type
                # exists in the new circuit
                try:
                    components_found[name_from_file]
                except:
                    # If the component doesn't exist, just don't
                    # try to read the parameters.
                    pass
                else:
                    # If it exists, check for the tag.
                    for c2 in range(len(components_found[name_from_file])):
                        # Remove leading spaces if any
                        if params_from_file[c1][1][0]==" ":
                            params_from_file[c1][1] = params_from_file[c1][1][1:]
                        # Check if the component tag exists in
                        # components found so far
                        if params_from_file[c1][1]==components_found[name_from_file][c2][1]:
                            if csv_element_extract(components_found[name_from_file][c2][0])==sheet:
                                # If so take the parameters and move them into the object
                                # having of that type and having the new cell position
                                component_objects[components_found[name_from_file][c2][0]].get_values(params_from_file[c1][3:], conn_matrix)

            csv_check_values.close()


    values_to_file = []
    for sheet in range(len(parameters_file)):
        values_to_sheet = []
        for items in component_objects.keys():
            if component_objects[items].sheet==sheet:
                # Each component object has a method
                # ask_values that prints in the csv file
                # default values for parameters.
                component_objects[items].ask_values(values_to_sheet, conn_matrix, branch_params)
        values_to_file.append(values_to_sheet)


    for sheet in range(len(parameters_file)):
        csv_ask_values = open(parameters_file[sheet],"w")

        for c1 in range(len(values_to_file[sheet])):
            for c2 in range(len(values_to_file[sheet][c1])):
                csv_ask_values.write("%s" %values_to_file[sheet][c1][c2])
                csv_ask_values.write(", ")
            csv_ask_values.write("\n")

        csv_ask_values.close()


    # Wait for the user to enter parameters before
    # reading the nw_params.csv file.
    if gv.c == 0:
        cont_ans="n"
    if gv.c == 1:  # here too automation of user input has been done to stop repetition of user input
        cont_ans="y"
    #cont_ans="y"
    print("The following circuit schematics have the corresponding parameter files:")
    for c1 in range(len(nw_input)):
        print("{} ---> {}".format(nw_input[c1]+".csv", parameters_file[c1]))

    while cont_ans.lower()!="y":
        cont_ans = input("Enter parameters in files above. When done, \
close the files and press y and enter to continue -> " %parameters_file)

    print()

    for sheet in range(len(parameters_file)):
        csv_get_values = open(parameters_file[sheet],"r")
        params_from_file = reading_params(csv_get_values)
        csv_get_values.close()

        for c1 in range(len(params_from_file)):
            # Getting rid of the beginning spaces
            # in the component keys
            while params_from_file[c1][2][0]==" ":
                params_from_file[c1][2] = params_from_file[c1][2][1:]
            params_from_file[c1][2] = params_from_file[c1][2] + str(sheet)
            component_objects[params_from_file[c1][2]].get_values(params_from_file[c1][3:], conn_matrix)


    return



def blank_control_descriptor(control_descs, control_desc_handles, component_objects, meter_list, controlled_elements, c1):
    """
    This function generates a blank descriptor file for every control file
    the user wants to enter. The control file is filled with default parameters.
    """

    control_desc_handles.append(open(control_descs[c1],"w"))

    # Input template
    control_desc_handles[c1].write("Input")
    control_desc_handles[c1].write(", ")
    # Default input is the first available meter.
    control_desc_handles[c1].write("Element name in \
circuit spreadsheet = %s" %(component_objects[meter_list[0]].type+"_"+component_objects[meter_list[0]].tag))
    control_desc_handles[c1].write(", ")
    # Default name of the meter in the control code is the
    # meter name_meter tag.
    control_desc_handles[c1].write("Desired variable \
name in control code = %s" %(component_objects[meter_list[0]].type+"_"+component_objects[meter_list[0]].tag))
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("\n")


    if controlled_elements:
        # Output template. Create a line for every
        # control input a particular controlled
        # element has.
        for c2 in range(len(component_objects[controlled_elements[0]].control_tag)):
            control_desc_handles[c1].write("Output")
            control_desc_handles[c1].write(", ")
            control_desc_handles[c1].write("Element name in circuit spreadsheet = \
    %s" %(component_objects[controlled_elements[0]].type+"_"+component_objects[controlled_elements[0]].tag))
            control_desc_handles[c1].write(", ")
            control_desc_handles[c1].write("Control tag defined in parameters spreadsheet \
    = %s" %(component_objects[controlled_elements[0]].control_tag[c2]))
            control_desc_handles[c1].write(", ")
            control_desc_handles[c1].write("Desired variable name in control code = \
    %s" %(component_objects[controlled_elements[0]].control_tag[c2]))
            control_desc_handles[c1].write(", ")
            control_desc_handles[c1].write("Initial output value = \
    %s" %(component_objects[controlled_elements[0]].control_values[c2]))
            control_desc_handles[c1].write(", ")
            control_desc_handles[c1].write("\n")


    # Static variable template
    control_desc_handles[c1].write("StaticVariable")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("Desired variable name in control code = Var1")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("Initial value of variable = 0.0")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("\n")

    # Time event template
    control_desc_handles[c1].write("TimeEvent")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("Desired variable name in control code = t1")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("First time event = 0.0")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("\n")

    # Variable storage template
    control_desc_handles[c1].write("VariableStorage")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("Desired variable name in control code = VarStor1")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("Initial value of variable = 0.0")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("Plot variable in output file = no")
    control_desc_handles[c1].write(", ")
    control_desc_handles[c1].write("\n")

    control_desc_handles[c1].close()

    return




def update_control_code(component_objects, components_found, controlled_elements, meter_list, control_files):
    """
    This function reads the control code in the user defined
    control programs and writes them into a single .py file
    that will be called in the main program.
    """

    # This is the main control program
    # It will contain the individual control
    # codes as functions.
    complete_control = open("__control.py","w")


    # These are spreadsheets that contain the variables
    # that each control file needs to access from the simulation.
    control_descs = []
    for c1 in range(len(control_files)):
        control_descs.append(control_files[c1]+"_desc.csv")

    # Each control code written by user will be embedded in
    # a control function.
    control_functions = []
    for c1 in range(len(control_files)):
        control_functions.append(control_files[c1]+"_func")

    # The .py files that contain the control code.
    for c1 in range(len(control_files)):
        control_files[c1] = control_files[c1]+".py"


    # These lists will contain separate dictionaries
    # for every control file.

    # Input variables for the control codes
    control_file_inputs = []
    # Output variables generated by the control codes.
    control_file_outputs = []
    # Static variables used by the control codes.
    control_file_staticvars = []
    # Time events generated by the control codes
    control_file_timeevents = []
    # Variables stored/plotted by the control codes.
    # Only one dictionary exists for all the control codes.
    # So these variables are like global variables.
    control_file_variablestorage = {}
    # Events generated in each control file.
    # These events are set when the output of the
    # control file changes.
    control_file_events = []


    # List of the opened control descriptor csv files.
    control_desc_handles = []
    for c1 in range(len(control_files)):
        # Adding an empty dictionary for a control file.
        control_file_inputs.append({})
        control_file_outputs.append({})
        control_file_staticvars.append({})
        control_file_timeevents.append({})

        # Check if the descriptor exists.
        try:
            control_desc_handles.append(open(control_descs[c1],"r"))

        except:
            # If it doesn't create a blank template.
            blank_control_descriptor(control_descs, control_desc_handles, \
                                     component_objects, meter_list, controlled_elements, c1)


    # Wait for the user to enter parameters before
    # reading the *_desc.csv file.
    if control_files:
        cont_ans = "n"
        while cont_ans.lower()!="y":
            print("Enter control parameters in the following files --> ")
            for c1 in range(len(control_descs)):
                print("{} ".format(control_descs[c1]))
            cont_ans = input("When ready press y and enter to continue -> ")


    # Read the parameters from the descriptor spreadsheet.
    control_desc_handles = []
    for c1 in range(len(control_files)):
        control_desc_handles.append(open(control_descs[c1],"r"))

        params_from_file = reading_params(control_desc_handles[c1])

        for c2 in range(len(params_from_file)):
            # Scrubbing blank spaces from the beginning
            # and the end of the first cell.
            while params_from_file[c2][0][0]==" ":
                params_from_file[c2][0] = params_from_file[c2][0][1:]
            while params_from_file[c2][0][-1]==" ":
                params_from_file[c2][0] = params_from_file[c2][0][:-1]

            if params_from_file[c2][0].lower()=="input":
                input_type = params_from_file[c2][1].split("=")[1]

                if len(input_type.split("."))==1:
                # If the input source has a single element,
                #  it will be a meter.
                    meter_type = params_from_file[c2][1].split("=")[1]
                    while meter_type[0]==" ":
                        meter_type = meter_type[1:]
                    while meter_type[-1]==" ":
                        meter_type = meter_type[:-1]

                    # Look for the meter in components_found
                    # and get the cell position from the meter tag.
                    # The cell position which is unique will be the
                    # dictionary key for control_file_inputs.
                    for c3 in range(len(components_found[meter_type.split("_")[0].lower()])):
                        if components_found[meter_type.split("_")[0].lower()][c3][1]==meter_type.split("_")[1]:
                            meter_type_ref = meter_type.split("_")[0].lower()
                            control_file_inputs[c1][components_found[meter_type_ref][c3][0]]=[components_found[meter_type_ref][c3][1]]

                            var_name = params_from_file[c2][2].split("=")[1]
                            while var_name[0]==" ":
                                var_name = var_name[1:]
                            while var_name[-1]==" ":
                                var_name = var_name[:-1]

                            control_file_inputs[c1][components_found[meter_type_ref][c3][0]].append(var_name)

                # If the input source has a . it means it is another
                # object - either another control block or an element.
                #    - TO DO LATER
                else:
                    input_object = input_type.split(".")[0]
                    while input_object[0]==" ":
                        input_object = input_object[1:]
                    while input_object[-1]==" ":
                        input_object = input_object[:-1]




            if params_from_file[c2][0].lower()=="output":
                # If it is an output, it is a controlled element
                element_type=params_from_file[c2][1].split("=")[1]
                while element_type[0]==" ":
                    element_type = element_type[1:]
                while element_type[-1]==" ":
                    element_type = element_type[:-1]

                # Look for the controlled element in components_found
                # and get the cell position from the device tag.
                # The cell position will be the unique dictionary key
                for c3 in range(len(components_found[element_type.split("_")[0].lower()])):
                    if components_found[element_type.split("_")[0].lower()][c3][1]==element_type.split("_")[1]:
                        element_type_ref = element_type.split("_")[0].lower()
                        # Since a controlled element can have more than one control input
                        # Check if it has been found before.
                        if not components_found[element_type_ref][c3][0] in control_file_outputs[c1].keys():
                            control_file_outputs[c1][components_found[element_type_ref][c3][0]] = [components_found[element_type_ref][c3][1]]

                        control_tag_name = params_from_file[c2][2].split("=")[1]
                        control_var_name = params_from_file[c2][3].split("=")[1]
                        control_init_value = params_from_file[c2][4].split("=")[1]

                        while control_tag_name[0]==" ":
                            control_tag_name = control_tag_name[1:]
                        while control_tag_name[-1]==" ":
                            control_tag_name = control_tag_name[:-1]

                        while control_var_name[0]==" ":
                            control_var_name = control_var_name[1:]
                        while control_var_name[-1]==" ":
                            control_var_name = control_var_name[:-1]

                        while control_init_value[0]==" ":
                            control_init_value = control_init_value[1:]
                        while control_init_value[-1]==" ":
                            control_init_value = control_init_value[:-1]

                        control_file_outputs[c1][components_found[element_type_ref][c3][0]].append([control_tag_name, control_var_name, \
                                            float(control_init_value)])



            if params_from_file[c2][0].lower()=="staticvariable":
                # If it is a staticvariable, the dictionary key
                # will be the variable name.
                staticvar_type = params_from_file[c2][1].split("=")[1]
                while staticvar_type[0]==" ":
                    staticvar_type = staticvar_type[1:]
                while staticvar_type[-1]==" ":
                    staticvar_type = staticvar_type[:-1]

                staticvar_val = params_from_file[c2][2].split("=")[1]
                while staticvar_val[0]==" ":
                    staticvar_val = staticvar_val[1:]
                while staticvar_val[-1]==" ":
                    staticvar_val = staticvar_val[:-1]

                control_file_staticvars[c1][staticvar_type]=float(staticvar_val)


            if params_from_file[c2][0].lower()=="timeevent":
                # If it is a timeevent, the dictionary key
                # will be the variable name.
                timeevent_type = params_from_file[c2][1].split("=")[1]
                while timeevent_type[0]==" ":
                    timeevent_type = timeevent_type[1:]
                while timeevent_type[-1]==" ":
                    timeevent_type = timeevent_type[:-1]

                timeevent_val = params_from_file[c2][2].split("=")[1]
                while timeevent_val[0]==" ":
                    timeevent_val = timeevent_val[1:]
                while timeevent_val[-1]==" ":
                    timeevent_val = timeevent_val[:-1]

                control_file_timeevents[c1][timeevent_type] = float(timeevent_val)



            if params_from_file[c2][0].lower()=="variablestorage":
                # If it is a variable storage, the dictionary key
                # will be the variable name.
                varstore_name = params_from_file[c2][1].split("=")[1]
                while varstore_name[0]==" ":
                    varstore_name = varstore_name[1:]
                while varstore_name[-1]==" ":
                    varstore_name = varstore_name[:-1]

                varstore_val = params_from_file[c2][2].split("=")[1]
                while varstore_val[0]==" ":
                    varstore_val = varstore_val[1:]
                while varstore_val[-1]==" ":
                    varstore_val = varstore_val[:-1]

                try:
                    float(varstore_val)
                except:
                    pass
                else:
                    varstore_val = float(varstore_val)


                varstore_plot = params_from_file[c2][3].split("=")[1]
                while varstore_plot[0]==" ":
                    varstore_plot = varstore_plot[1:]
                while varstore_plot[-1]==" ":
                    varstore_plot = varstore_plot[:-1]


                if varstore_name not in control_file_variablestorage.keys():
                    control_file_variablestorage[varstore_name]=[varstore_val, varstore_plot]
                else:
                    print("Multiple definitions of variable storage {}".format(varstore_name))


        # Each control file has one event appended.
        # As a default, it is made to 0.
        control_file_events.append(0)
        control_desc_handles[c1].close()



    # Wait for use to update the control code.
    if control_files:
        cont_ans = "n"
        #cont_ans = "y"
        while cont_ans.lower()!="y":
            print("Enter control code in the following files --> ")
            for c1 in range(len(control_files)):
                print("{} ".format(control_files[c1]))
            cont_ans = input("When ready press y and enter to continue -> ")


    # This list will contain the control
    # code as lists of strings.
    control_code = []
    for c1 in range(len(control_files)):
        control_code.append([])

    control_handles = []
    for c1 in range(len(control_files)):
        control_handles.append(open(control_files[c1],"r"))

        # Add the lines in the control codes
        # to the lists.
        for line in control_handles[c1]:
            control_code[c1].append(line)

        control_handles[c1].close()

    # Check for any import statements.
    # If any of the control codes have import statements
    # add them to the main control program.
    for c1 in range(len(control_code)):
        for c2 in range(len(control_code[c1])):
            if "import" in control_code[c1][c2].split():
                complete_control.write(control_code[c1][c2])
                complete_control.write("\n")


    # Delete the import statement from the functions.
    # This is to avoid duplication
    for c1 in range(len(control_code)):
        for c2 in range(len(control_code[c1])-1, -1,  -1):
            if "import" in control_code[c1][c2].split():
                del control_code[c1][c2]


    for c1 in range(len(control_code)):
        # For each control code, define a function
        # Name of function has been defined in
        # control_functions.
        complete_control.write("def %s(interface_inputs, interface_outputs, interface_static, interface_time, interface_variablestore, \
                                interface_events, circuit_components, pos, t_clock, sys_t_events):" %control_functions[c1])
        complete_control.write("\n")
        # The remaining statements have a tab \t for indentation

        # Assign the input variables to the meter outputs
        for ip_keys in control_file_inputs[c1].keys():
            complete_control.write("\t")
            complete_control.write("%s=circuit_components['%s'].op_value" %(control_file_inputs[c1][ip_keys][1], ip_keys))
            complete_control.write("\n")

        # Assign the static variables to their latest values
        for static_keys in control_file_staticvars[c1].keys():
            complete_control.write("\t")
            complete_control.write("%s=interface_static[pos]['%s']" %(static_keys, static_keys))
            complete_control.write("\n")

        # Assign the time events variables to their latest values
        for time_keys in control_file_timeevents[c1].keys():
            complete_control.write("\t")
            complete_control.write("%s=interface_time[pos]['%s']" %(time_keys, time_keys))
            complete_control.write("\n")

        # Assign the variable storage values to their latest values
        for varstore_keys in control_file_variablestorage.keys():
            complete_control.write("\t")
            complete_control.write("%s=interface_variablestore['%s'][0]" %(varstore_keys, varstore_keys))
            complete_control.write("\n")


        # Assign the variables to the output controlled
        # elements. Additionally, check each control element
        # for multiple control inputs.
        for op_keys in control_file_outputs[c1].keys():
            for c3 in range(1, len(control_file_outputs[c1][op_keys])):
                control_pos = component_objects[op_keys].control_tag.index(control_file_outputs[c1][op_keys][c3][0])
                complete_control.write("\t")
                # Extract the dictionary values
                complete_control.write("%s=interface_outputs[pos]['%s'][%d][2]" %(control_file_outputs[c1][op_keys][c3][1], op_keys, c3))
                complete_control.write("\n")

        # Include the control code.
        for c2 in range(len(control_code[c1])):
            complete_control.write("\t")
            complete_control.write(control_code[c1][c2])

        # Intialize the event generated by the function
        # to be zero. This will be changed below.
        complete_control.write("\n")
        complete_control.write("\t")
        complete_control.write("interface_events[pos] = 0")
        complete_control.write("\n")
        complete_control.write("\n")


        # Check if there has been a change in any of the output
        # variables. This is a event generator to run the
        # ode solver even if the ode time step has not been reached.
        for op_keys in control_file_outputs[c1].keys():
            for c3 in range(1, len(control_file_outputs[c1][op_keys])):
                control_pos = component_objects[op_keys].control_tag.index(control_file_outputs[c1][op_keys][c3][0])
                complete_control.write("\t")
                # Update the dictionary values
                complete_control.write("if not interface_outputs[pos]['%s'][%d][2]==%s:" %(op_keys, c3, control_file_outputs[c1][op_keys][c3][1]))
                complete_control.write("\n")
                complete_control.write("\t")
                complete_control.write("\t")
                complete_control.write("interface_events[pos] = 1")
                complete_control.write("\n")
                complete_control.write("\n")

        # Assign the output controlled elements to the
        # variables. Additionally, check each control element
        # for multiple control inputs.
        for op_keys in control_file_outputs[c1].keys():
            for c3 in range(1, len(control_file_outputs[c1][op_keys])):
                control_pos = component_objects[op_keys].control_tag.index(control_file_outputs[c1][op_keys][c3][0])
                complete_control.write("\t")
                # Update the object control values
                complete_control.write("circuit_components['%s'].control_values[%d]=%s" %(op_keys, control_pos, \
                                        control_file_outputs[c1][op_keys][c3][1]))
                complete_control.write("\n")
                complete_control.write("\t")
                # Update the dictionary values
                complete_control.write("interface_outputs[pos]['%s'][%d][2]=%s" %(op_keys, c3, control_file_outputs[c1][op_keys][c3][1]))
                complete_control.write("\n")

        # Store the static variables in the dictionary
        for static_keys in control_file_staticvars[c1].keys():
            complete_control.write("\t")
            complete_control.write("interface_static[pos]['%s']=%s" %(static_keys, static_keys))
            complete_control.write("\n")


        # Store the time events in the dictionary
        for time_keys in control_file_timeevents[c1].keys():
            complete_control.write("\t")
            complete_control.write("interface_time[pos]['%s']=%s" %(time_keys, time_keys))
            complete_control.write("\n")
            complete_control.write("\t")
            complete_control.write("sys_t_events.append(%s)" %time_keys)
            complete_control.write("\n")

        # Store the variable storage values in the dictionary
        for varstore_keys in control_file_variablestorage.keys():
            complete_control.write("\t")
            complete_control.write("interface_variablestore['%s'][0]=%s" %(varstore_keys, varstore_keys))
            complete_control.write("\n")

        # end the function
        complete_control.write("\t")
        complete_control.write("return")
        complete_control.write("\n")
        complete_control.write("\n")

    complete_control.close()

    return [control_files, control_functions, control_file_inputs, control_file_outputs, control_file_staticvars, \
            control_file_timeevents, control_file_variablestorage,  control_file_events]



def initialize_branch_params(branch_params,  branch_events,  component_objects, source_list,  sys_mat_u, components_in_branch):
    """
    To initialiize the parameters in branch_params list.
    Take every element in a branch and check
    if that is a valid object identifier
    If not, i.e if it is a wire, an exception will
    be raised in which case nothing will happen.
    If no exception is raised, initialize the parameters
    - resistance, inductance, voltages.
    """

    for c1 in range(len(branch_params)):
        if branch_events[c1]=="yes" or branch_events[c1]=="hard":
            branch_params[c1][-1][0][0] = 0.0
            branch_params[c1][-1][0][1] = 0.0
            for c2 in range(len(source_list)):
                branch_params[c1][-1][1][c2] = 0.0

            for c2 in range(len(components_in_branch[c1])):
                component_objects[components_in_branch[c1][c2]].transfer_to_branch(branch_params[c1], source_list,  sys_mat_u)

    return



def inductor_volt_calc(inductor_list, system_loop_map, branch_params, ode_var, dt):
    """
    Calculates the voltages across the inductors in the circuit.
    """

    inductor_voltages = []
    for c1 in inductor_list:
        inductor_dibydt = 0.0
        for c2 in range(len(system_loop_map)):
            if system_loop_map[c2][c1]=="forward":
                inductor_dibydt += ode_var[4].data[c2][0]

            if system_loop_map[c2][c1]=="reverse":
                inductor_dibydt -= ode_var[4].data[c2][0]

        inductor_dibydt = inductor_dibydt/dt
        inductor_voltages.append(inductor_dibydt*branch_params[c1][-1][0][1])

    return inductor_voltages
