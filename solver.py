#! /usr/bin/env python

import network_reader as NwRdr
import sys
import math
import matrix as Mtrx



def generate_system_loops(sys_loops, branch_info, sys_loop_map, branch_stiff, dt):
    """
    Generates a map of the system loops in terms of presence
    of branches in the loops, their direction and whether
    they are stiff or not. This is for loop manipulation.
    """

    # Calculate the maximum resistance in the system
    # This is used for determining later whether
    # branches are stiff
    max_res = abs(branch_info[0][-1][0][0])
    for c1 in range(1, len(branch_info)):
        if branch_info[c1][-1][0][0]>max_res:
            max_res = branch_info[c1][-1][0][0]

    # Calculates the time constants of the loops
    # from the diagonal elements as L/R ratios.
    # A branch is stiff if it has a non-zero resistor,
    # the L/R ratio is less that 0.1 times the simulation time step
    # and if the ratio of resistance to maximum resistance
    # is greater than dt.

    # All these values are arbitrary and will HAVE to be changed later
    for c1 in range(len(branch_info)):
        branch_stiff[c1] = "no"
        if branch_info[c1][-1][0][0]:
            if abs(branch_info[c1][-1][0][1]/branch_info[c1][-1][0][0])<0.1*dt:
                if branch_info[c1][-1][0][0]/max_res > 0.0001:
                    branch_stiff[c1] = "yes"
#                    branch_info[c1][-1][0][1] = 0.0


    # Additionally, even if a branch does not have a huge
    # resitance, if the L/R ratio is smaller that 0.1dt, the
    # inductance is set to zero to make it a resistive branch.

    # All these values are arbitrary and will HAVE to be changed later
    for c1 in range(len(branch_info)):
        if branch_info[c1][-1][0][0]:
            if abs(branch_info[c1][-1][0][1]/branch_info[c1][-1][0][0])<0.1*dt:
                branch_info[c1][-1][0][1] = 0.0


    # Generate the system loop map from the list
    # stiff_ratio for every branch.
    for c1 in range(len(sys_loops)):
        for c3 in range(len(branch_info)):
            # Initialize the system map value to "no"
            sys_loop_map[c1][c3] = "no"
            for c2 in range(len(sys_loops[c1])):
                # Check if branch exists in loop
                if branch_info[c3][:-1]==sys_loops[c1][c2][:-1]:
                    # Check the branch direction
                    if sys_loops[c1][c2][-1]=="forward":
                        # Check if the branch is stiff.
                        if branch_stiff[c3]=="yes":
                            sys_loop_map[c1][c3] = "stiff_forward"
                        else:
                            sys_loop_map[c1][c3] = "forward"
                    else:
                        if branch_stiff[c3]=="yes":
                            sys_loop_map[c1][c3] = "stiff_reverse"
                        else:
                            sys_loop_map[c1][c3] = "reverse"


    return




def update_system_loop_map(branch_info, sys_loop_map, branch_stiff, dt):
    """
    Generates a map of the system loops in terms of presence
    of branches in the loops, their direction and whether
    they are stiff or not. This is for loop manipulation.
    """

    # Calculate the maximum resistance in the system
    # This is used for determining later whether
    # branches are stiff
    max_res = abs(branch_info[0][-1][0][0])
    for c1 in range(1, len(branch_info)):
        if branch_info[c1][-1][0][0]>max_res:
            max_res = branch_info[c1][-1][0][0]


    # Calculates the time constants of the loops
    # from the diagonal elements as L/R ratios.
    # A branch is stiff it has a non-zero resistor,
    # the L/R ratio is less that 0.1 times the simulation time step
    # and if the ratio of resistance to maximum resistance
    # is greater than dt.

    # All these values are arbitrary and will HAVE to be changed later
    for c1 in range(len(branch_info)):
        branch_stiff[c1] = "no"
        if branch_info[c1][-1][0][0]:
            if abs(branch_info[c1][-1][0][1]/branch_info[c1][-1][0][0])<0.1*dt:
                if branch_info[c1][-1][0][0]/max_res > 0.0001:
                    branch_stiff[c1] = "yes"
#                    branch_info[c1][-1][0][1] = 0.0


    # Additionally, even if a branch does not have a huge
    # resitance, if the L/R ratio is smaller that 0.1dt, the
    # inductance is set to zero to make it a resistive branch.

    # All these values are arbitrary and will HAVE to be changed later
    for c1 in range(len(branch_info)):
        if branch_info[c1][-1][0][0]:
            if abs(branch_info[c1][-1][0][1]/branch_info[c1][-1][0][0])<0.1*dt:
                branch_info[c1][-1][0][1] = 0.0


    # Only updates the values in the system loop map
    # The loops have not changed. So a stiff branch
    # may become nonstiff and vice versa.
    for c1 in range(len(sys_loop_map)):
        for c2 in range(len(branch_info)):
            if branch_stiff[c2]=="no":
                if sys_loop_map[c1][c2]=="stiff_forward":
                    sys_loop_map[c1][c2] = "forward"
                elif sys_loop_map[c1][c2]=="stiff_reverse":
                    sys_loop_map[c1][c2] = "reverse"

            else:
                if sys_loop_map[c1][c2]=="forward":
                    sys_loop_map[c1][c2] = "stiff_forward"
                elif sys_loop_map[c1][c2]=="reverse":
                    sys_loop_map[c1][c2] = "stiff_reverse"

    return


def admittance_normalization(mho_matrix):
    """
    This function determines if any non-diagonal element
    of the admittance matrix is significantly smaller than the
    diagonal element. The idea was to eliminate the effect of
    stiff branches.
    This function is not used as it is an approximation.
    """

    diag_elem_mho = []
    for c1 in range(len(mho_matrix)):
        diag_elem_mho.append(mho_matrix[c1][c1])

    for c1 in range(len(mho_matrix)):
        if abs(mho_matrix[c1][c1])<diag_elem_mho[c1]/1000.0:
            for c2 in range(len(mho_matrix[c1])):
                mho_matrix[c1][c2] = 0.0

    return



def determine_nodal_matrices(branch_info, branch_stiff, sys_inputs, mho_matrix, src_vector, inductor_list, inductor_stiffness, \
                            br_pos, br_direct, c1, c2, func_purpose):
    """
    This function populates the admittance and source matrices
    for nodal analysis from branch information and topology
    """

    if br_pos in inductor_list:
        if branch_stiff[br_pos]=="no":
            if func_purpose=="det_state":
                if inductor_stiffness[inductor_list.index(br_pos)]=="no":
                    src_vector[c1] -= br_direct*branch_info[br_pos][-1][2]
                else:
                    mho_matrix[c1][c1] += 1/branch_info[br_pos][-1][0][0]
                    mho_matrix[c1][c2] -= 1/branch_info[br_pos][-1][0][0]

                    for c4 in range(len(branch_info[br_pos][-1][1])):
                        src_vector[c1] -= br_direct*branch_info[br_pos][-1][1][c4]*sys_inputs.data[c4][0]/branch_info[br_pos][-1][0][0]

            if func_purpose=="calc_currents":
                src_vector[c1] -= br_direct*branch_info[br_pos][-1][2]

        else:
            mho_matrix[c1][c1] += 1/branch_info[br_pos][-1][0][0]
            mho_matrix[c1][c2] -= 1/branch_info[br_pos][-1][0][0]

            for c4 in range(len(branch_info[br_pos][-1][1])):
                src_vector[c1] -= br_direct*branch_info[br_pos][-1][1][c4]*sys_inputs.data[c4][0]/branch_info[br_pos][-1][0][0]


    else:
        mho_matrix[c1][c1] += 1/branch_info[br_pos][-1][0][0]
        mho_matrix[c1][c2] -= 1/branch_info[br_pos][-1][0][0]

        for c4 in range(len(branch_info[br_pos][-1][1])):
            src_vector[c1] -= br_direct*branch_info[br_pos][-1][1][c4]*sys_inputs.data[c4][0]/branch_info[br_pos][-1][0][0]

    return



def test_current_continuity(mho_matrix, src_vector):
    """
    Testing the function. Not being used.
    """

    nd_voltage = []
    # Node voltages. There will be one reference node
    for c1 in range(len(mho_matrix)):
        nd_voltage.append(0.0)


    # Look for diagonal elements - check if they are zero
    # If so, look in that same column in subsequent rows
    # if there is a non zero element and exchange them
    # Later, make the matrix upper triangular.
    # Using row manipulations, make all the elements
    # below a diagonal row zero.
    for c1 in range(len(mho_matrix)):
        if not mho_matrix[c1][c1]:
            c2 = c1+1
            diag_elem_inter = "no"
            while c2<len(mho_matrix) and diag_elem_inter=="no":
                if mho_matrix[c2][c1]:
                    diag_elem_inter = "yes"
                    src_vector[c1], src_vector[c2] = src_vector[c2], src_vector[c1]
                    for c3 in range(len(mho_matrix[c1])):
                        mho_matrix[c1][c3], mho_matrix[c2][c3] = mho_matrix[c2][c3], mho_matrix[c1][c3]
                c2 += 1

        if mho_matrix[c1][c1]:
            diag_elem = c1
            elem_found = "yes"
        else:
            c2 = c1
            elem_found = "no"
            while elem_found=="no" and c2<len(mho_matrix):
                if mho_matrix[c1][c2]:
                    elem_found = "yes"
                    diag_elem = c2
                c2 += 1

        if elem_found=="yes":
            for c2 in range(c1+1, len(mho_matrix)):
                if mho_matrix[c2][diag_elem]:

                    mho_factor = mho_matrix[c2][diag_elem]
                    src_vector[c2] -= src_vector[c1]*mho_factor/mho_matrix[c1][diag_elem]
                    for c3 in range(len(mho_matrix[c1])):
                        mho_matrix[c2][c3] -= mho_matrix[c1][c3]*mho_factor/mho_matrix[c1][diag_elem]
#                        if abs(mho_matrix[c2][c3])<1.0e-15:
#                            mho_matrix[c2][c3] = 0.0


    # Removes the effect of stiff branches from
    # the admittance matrix. Should not be used.
    #admiitance_normalization(mho_matrix)

    # Continue to solve the equation AX=B

    # The last row of the manipulated admittance matrix will
    # be zero as it is the reference node. So taking this
    # voltage to be zero, calculate all the other node voltages
    # from second last to first.
    for c1 in range(len(mho_matrix)-1, -1, -1):
        if mho_matrix[c1][c1]:
            diag_elem = c1
            elem_found = "yes"
        else:
            c2 = c1
            elem_found = "no"
            while elem_found=="no" and c2<len(mho_matrix[c1]):
                if mho_matrix[c1][c2]:
                    elem_found = "yes"
                    diag_elem = c2
                c2 += 1

        if elem_found=="yes":
            nd_voltage[diag_elem] = src_vector[c1]
            for c2 in range(diag_elem+1, len(mho_matrix[c1])):
                nd_voltage[diag_elem] -= mho_matrix[c1][c2]*nd_voltage[c2]

            nd_voltage[diag_elem] = nd_voltage[diag_elem]/mho_matrix[c1][diag_elem]
#            if abs(nd_voltage[diag_elem])>1.0e+10:
#                nd_voltage[diag_elem] = 0.0

    return



def current_continuity(kcl_branch_lookup, mho_matrix, src_vector, nd_voltage, all_nd_voltage, kcl_list_of_nodes, list_of_nodes, \
                        shortnode_list, branch_info, freewheel_nonlinear_br, br_currents, func_purpose, time_check, debug_mode):
    """
    Following an event, to find the branch currents through nodal analysis.
    The objective is to determine if certain devices must change their status
    to maintain continuity of inductor currents.
    """

    # Node voltages. There will be one reference node
    for c1 in range(len(nd_voltage)):
        nd_voltage[c1] = 0.0

    # Node voltages. There will be one reference node
    for c1 in range(len(all_nd_voltage)):
        all_nd_voltage[c1] = 0.0

    # The admittance matrix. As it is more or less
    # a dc analysis of a snapshot of the circuit
    # only resistances are considered.
    for c1 in range(len(mho_matrix)):
        for c2 in range(len(mho_matrix)):
            mho_matrix[c1][c2] = 0.0

    # The source vector. This will contain
    # currents sources - inductor currents,
    # currents through branches with voltages.
    for c1 in range(len(src_vector)):
        src_vector[c1] = 0.0

    # Use the lookup table to generate the admittance matrix and
    # source vectors for KCL.
    for c1 in range(len(kcl_branch_lookup)):
        coord_row = kcl_branch_lookup[c1][1][0]
        coord_col = kcl_branch_lookup[c1][1][1]
        if kcl_branch_lookup[c1][3]==1:
            br_admittance = 1.0/kcl_branch_lookup[c1][5]
            mho_matrix[coord_row][coord_row] += br_admittance
            mho_matrix[coord_col][coord_col] += br_admittance
            mho_matrix[coord_row][coord_col] -= br_admittance
            mho_matrix[coord_col][coord_row] -= br_admittance
            br_volt = -kcl_branch_lookup[c1][2]*kcl_branch_lookup[c1][4]/kcl_branch_lookup[c1][5]
            src_vector[coord_row] += br_volt
            src_vector[coord_col] -= br_volt
        else:
            br_current = -kcl_branch_lookup[c1][2]*kcl_branch_lookup[c1][6]
            src_vector[coord_row] += br_current
            src_vector[coord_col] -= br_current


    # Now to solve the equation AX=B

    # Look for diagonal elements - check if they are zero
    # If so, look in that same column in subsequent rows
    # if there is a non zero element and exchange them
    # Later, make the matrix upper triangular.
    # Using row manipulations, make all the elements
    # below a diagonal row zero.
    for c1 in range(len(mho_matrix)):
        if not mho_matrix[c1][c1]:
            c2 = c1+1
            diag_elem_inter = "no"
            while c2<len(mho_matrix) and diag_elem_inter=="no":
                if mho_matrix[c2][c1]:
                    diag_elem_inter = "yes"
                    src_vector[c1], src_vector[c2] = src_vector[c2], src_vector[c1]
                    for c3 in range(len(mho_matrix[c1])):
                        mho_matrix[c1][c3], mho_matrix[c2][c3] = mho_matrix[c2][c3], mho_matrix[c1][c3]
                c2 += 1

        if mho_matrix[c1][c1]:
            diag_elem = c1
            elem_found = "yes"
        else:
            c2 = c1
            elem_found = "no"
            while elem_found=="no" and c2<len(mho_matrix):
                if mho_matrix[c1][c2]:
                    elem_found = "yes"
                    diag_elem = c2
                c2 += 1

        if elem_found=="yes":
            for c2 in range(c1+1, len(mho_matrix)):
                if mho_matrix[c2][diag_elem]:
                    mho_factor = mho_matrix[c2][diag_elem]
                    src_vector[c2] -= src_vector[c1]*mho_factor/mho_matrix[c1][diag_elem]
                    for c3 in range(len(mho_matrix[c1])):
                        mho_matrix[c2][c3] -= mho_matrix[c1][c3]*mho_factor/mho_matrix[c1][diag_elem]
#                        if abs(mho_matrix[c2][c3])<1.0e-15:
#                            mho_matrix[c2][c3] = 0.0


    # Removes the effect of stiff branches from
    # the admittance matrix. Should not be used.
    #admiitance_normalization(mho_matrix)

    # Continue to solve the equation AX=B

    # The last row of the manipulated admittance matrix will
    # be zero as it is the reference node. So taking this
    # voltage to be zero, calculate all the other node voltages
    # from second last to first.
    for c1 in range(len(mho_matrix)-1, -1, -1):
        if mho_matrix[c1][c1]:
            diag_elem = c1
            elem_found = "yes"
        else:
            c2 = c1
            elem_found = "no"
            while elem_found=="no" and c2<len(mho_matrix[c1]):
                if mho_matrix[c1][c2]:
                    elem_found = "yes"
                    diag_elem = c2
                c2 += 1

        if elem_found=="yes":
            nd_voltage[diag_elem] = src_vector[c1]
            for c2 in range(diag_elem+1, len(mho_matrix[c1])):
                nd_voltage[diag_elem] -= mho_matrix[c1][c2]*nd_voltage[c2]

            nd_voltage[diag_elem] = nd_voltage[diag_elem]/mho_matrix[c1][diag_elem]
#            if abs(nd_voltage[diag_elem])>1.0e+10:
#                nd_voltage[diag_elem] = 0.0


    for c1 in kcl_list_of_nodes:
        all_nd_voltage[list_of_nodes.index(c1)] = nd_voltage[kcl_list_of_nodes.index(c1)]


    # Iterate through the shortnode lists
    # and equate the node voltages that are
    # in the short node list as they are connected
    # by shorts.
    for c1 in range(len(shortnode_list)):
        # In every shortnode list, take a shortnode
        # and express its voltage with respect to every
        # other shortnode in that list
        for c2 in range(1, len(shortnode_list[c1])):
            all_nd_voltage[shortnode_list[c1][c2]] = all_nd_voltage[shortnode_list[c1][0]]


    # Calculate the branch currents
    if func_purpose=="det_state":
        freewheel_branches = []

        for c1 in range(len(branch_info)):
            if c1 in freewheel_nonlinear_br:
                freewheel_branches.append(c1)

        # Calculate the branch currents as I = (Vnode1-Vnode2-Vsource)/Rbranch
        for c1 in range(len(branch_info)):
            if c1 in freewheel_branches:
                start_node = list_of_nodes.index(branch_info[c1][0])
                end_node = list_of_nodes.index(branch_info[c1][-2])

                br_currents[c1] = (all_nd_voltage[start_node] + kcl_branch_lookup[c1][4] - all_nd_voltage[end_node])/branch_info[c1][-1][0][0]

    else:

    # this is if func_purpose is calc_currents
        freewheel_branches = []

        for c1 in range(len(branch_info)):
            freewheel_branches.append(c1)

        # Calculate the branch currents as I = (Vnode1-Vnode2-Vsource)/Rbranch
        for c1 in range(len(branch_info)):
            if c1 in freewheel_branches:

                if kcl_branch_lookup[c1][3]==2:
                    br_currents[c1] = branch_info[c1][-1][2]

                else:
                    start_node = list_of_nodes.index(branch_info[c1][0])
                    end_node = list_of_nodes.index(branch_info[c1][-2])

                    br_currents[c1] = (all_nd_voltage[start_node] + kcl_branch_lookup[c1][4] - all_nd_voltage[end_node])/branch_info[c1][-1][0][0]

    return



def splitting_loops(resultant_loop, branches_in_kcl_nodes, kcl_branch_map, branch_params, branch_tags_in_loops):
    """
    This function takes a loop which is the result of a loop manipulation.
    the result of a loop manipulation will be at least one loop. This
    function splits the loop up into multiple loops if these are present.
    """

    branches_in_loop = []
    nodes_in_loop = []
    all_branches_in_loop = []
    node_pairs_in_loop = []
    for c2 in range(len(resultant_loop)):
        if not resultant_loop[c2]=="no":
            branch_nodes = []
            for c3 in range(len(branches_in_kcl_nodes)):
                if c2 in branches_in_kcl_nodes[c3]:
                    if c3 not in branch_nodes:
                        branch_nodes.append(c3)

            # For every branch that is found, the branch is
            # added to all branches found. And the KCL nodes
            # that are the end nodes of the branch are added
            # as a node pair.
            node_pairs_in_loop.append(branch_nodes)
            all_branches_in_loop.append(c2)
            branches_in_loop.append(c2)
            nodes_in_loop.append(branch_nodes)


    list_of_loops_node_pairs = []
    list_of_loops_branches = []
    while all_branches_in_loop:
        # To check for more than one loop, start with the
        # first node pair and loop the node pairs together.
        extra_loop_check = []
        current_branches = []
        extra_loop_check.append(node_pairs_in_loop[0])
        current_branches.append(all_branches_in_loop[0])
        origin_node = node_pairs_in_loop[0][0]
        next_node = node_pairs_in_loop[0][1]
        del node_pairs_in_loop[0]
        del all_branches_in_loop[0]
        loop_closed = "no"
        loop_changed = "no"
        c2 = 0
        # The search algorithm will keep adding node pairs (branches)
        # such that continuity is maintained. The end condition
        # is when one of the nodes in a branch is the same as the origin node.
        while c2<len(node_pairs_in_loop) and loop_closed=="no":
            # If the start node in a branch is the next node expected
            # by the search algorithm, add this branch. Also, the next
            # node will the end node of this branch. When a branch is
            # added, delete the branch from the node pair list.
            if node_pairs_in_loop[c2][0]==next_node:
                next_node = node_pairs_in_loop[c2][1]
                extra_loop_check.append(node_pairs_in_loop[c2])
                current_branches.append(all_branches_in_loop[c2])
                loop_changed = "yes"
                if node_pairs_in_loop[c2][1]==origin_node:
                    loop_closed = "yes"
                del node_pairs_in_loop[c2]
                del all_branches_in_loop[c2]
            elif node_pairs_in_loop[c2][1]==next_node:
                next_node = node_pairs_in_loop[c2][0]
                extra_loop_check.append([node_pairs_in_loop[c2][1], node_pairs_in_loop[c2][0]])
                current_branches.append(all_branches_in_loop[c2])
                loop_changed = "yes"
                if node_pairs_in_loop[c2][0]==origin_node:
                    loop_closed = "yes"
                del node_pairs_in_loop[c2]
                del all_branches_in_loop[c2]

            c2 += 1
            # In an iteration if a branch is added, it means the loop
            # has changed and the algorithm should continue. So the
            # branch counter is rewound if the last branch has been reached.
            # If no branch has been added, the branch count will stop
            # at the last branch and terminate the search.
            if c2>=len(node_pairs_in_loop) and loop_changed=="yes":
                c2 = 0
                loop_changed = "no"

        list_of_loops_node_pairs.append(extra_loop_check)
        list_of_loops_branches.append(current_branches)


    # The code block below is to remove a sub-loop from a loop. This may
    # happen when small loop exists along the nodes of the main loop. Typically,
    # they are parallel branches but there may be larger loops.
    for c1 in range(len(list_of_loops_node_pairs)):
        # Collect all the nodes in the loop
        all_nodes_in_loop = []
        for c2 in range(len(list_of_loops_node_pairs[c1])):
            if not list_of_loops_node_pairs[c1][c2][0] in all_nodes_in_loop:
                all_nodes_in_loop.append(list_of_loops_node_pairs[c1][c2][0])
            if not list_of_loops_node_pairs[c1][c2][1] in all_nodes_in_loop:
                all_nodes_in_loop.append(list_of_loops_node_pairs[c1][c2][1])

        # Count the occurance of each node in the loop.
        for c2 in range(len(all_nodes_in_loop)):
            node_count = 0
            for c3 in range(len(list_of_loops_node_pairs[c1])):
                if all_nodes_in_loop[c2] in list_of_loops_node_pairs[c1][c3]:
                    node_count += 1

            # A node should occur twice. Anything more is the sign of a sub-loop.
            if node_count>2:
                node_positions = []
                for c3 in range(len(list_of_loops_node_pairs[c1])):
                    if all_nodes_in_loop[c2] in list_of_loops_node_pairs[c1][c3]:
                        node_positions.append(c3)

                # Slice the nodes between two additional appearances of the node
                # and perform the same slice for the branches.
                node_coll_vector = []
                branch_coll_vector = []
                for c3 in range(node_positions[1], node_positions[2]+1):
                    node_coll_vector.append(list_of_loops_node_pairs[c1][c3])
                    branch_coll_vector.append(list_of_loops_branches[c1][c3])

                # Add this slice which is a sub-loop to the list of loops.
                list_of_loops_node_pairs.append(node_coll_vector)
                list_of_loops_branches.append(branch_coll_vector)
                for c3 in range(node_positions[2], node_positions[1]-1, -1):
                    del list_of_loops_node_pairs[c1][c3]
                    del list_of_loops_branches[c1][c3]


    # List of loops found in this resultant loop.
    new_resultant_loop = []
    for c1 in range(len(list_of_loops_node_pairs)):
        current_loop = []
        for c2 in range(len(resultant_loop)):
            current_loop.append("no")
        new_resultant_loop.append(current_loop)


    # Assign branches and directions to each loop
    for c1 in range(len(list_of_loops_node_pairs)):
        for c2 in range(len(list_of_loops_node_pairs[c1])):
            branch_pos = list_of_loops_branches[c1][c2]
            original_branch_pos = branches_in_loop.index(branch_pos)
            if not nodes_in_loop[original_branch_pos]==list_of_loops_node_pairs[c1][c2]:
                if resultant_loop[branch_pos]=="reverse":
                    new_resultant_loop[c1][branch_pos] = "forward"
                if resultant_loop[branch_pos]=="forward":
                    new_resultant_loop[c1][branch_pos] = "reverse"
                if resultant_loop[branch_pos]=="stiff_reverse":
                    new_resultant_loop[c1][branch_pos] = "stiff_forward"
                if resultant_loop[branch_pos]=="stiff_forward":
                    new_resultant_loop[c1][branch_pos] = "stiff_reverse"
            else:
                new_resultant_loop[c1][branch_pos] = resultant_loop[branch_pos]


    # Make sure the directions are correct and the loop is valid.
    for c1 in range(len(new_resultant_loop)):
        loop_valid_result = loop_validity_checking(new_resultant_loop[c1], branches_in_kcl_nodes, kcl_branch_map)
        if loop_valid_result=="no":
            for c2 in range(len(new_resultant_loop[c1])):
                new_resultant_loop[c1][c2] = "no"

    return new_resultant_loop




def debug_loops(sys_loop_map, branches_in_kcl_nodes, branch_params, branch_tags_in_loops, nonstiff_loops):
    """
    This function will list out the loops for checking the simulation.
    """

    for loop_index in nonstiff_loops:
        resultant_loop = sys_loop_map[loop_index]
        all_branches_in_loop = []
        branches_in_loop = []
        nodes_in_loop = []
        node_pairs_in_loop = []
        for c2 in range(len(resultant_loop)):
            if not resultant_loop[c2]=="no":
                branch_nodes = []
                for c3 in range(len(branches_in_kcl_nodes)):
                    if c2 in branches_in_kcl_nodes[c3]:
                        if c3 not in branch_nodes:
                            branch_nodes.append(c3)

                # For every branch that is found, the branch is
                # added to all branches found. And the KCL nodes
                # that are the end nodes of the branch are added
                # as a node pair.
                node_pairs_in_loop.append(branch_nodes)
                all_branches_in_loop.append(c2)


        collection_of_branches = []

        nodes_matching = "yes"
        if all_branches_in_loop:
            # Starting with the first branch found in the
            # loop, trace the loop :
            # This means - origin node is the first node
            # of the first branch. The "next" node is the
            # second node of the branch.
#            branches_in_loop.append(all_branches_in_loop[0])
            next_node = node_pairs_in_loop[0][1]
            nodes_in_loop.append(next_node)

            # First check is if all nodes in the loop
            # occur as node pairs. If that fails, it is
            # not a loop and the entire check can exit.
            for c2 in range(len(node_pairs_in_loop)):
                for c3 in range(len(node_pairs_in_loop[c2])):
                    node_occur = 1
                    for c4 in range(len(node_pairs_in_loop)):
                        if not c4==c2:
                            if node_pairs_in_loop[c4][0]==node_pairs_in_loop[c2][c3]:
                                node_occur += 1
                            if node_pairs_in_loop[c4][1]==node_pairs_in_loop[c2][c3]:
                                node_occur += 1

                    if not node_occur==2:
                        nodes_matching = "no"


            copy_of_node_pairs = []
            for c1 in node_pairs_in_loop:
                copy_of_node_pairs.append(c1)

            copy_of_all_branches = []
            for c1 in all_branches_in_loop:
                copy_of_all_branches.append(c1)

            # If the loop branches are valid, check if the direction
            # of the branches in the loop are correct. Also check if
            # two completely separate loops with common nodes are not
            # present in a single loop.
            if nodes_matching=="yes":
                # To check for more than one loop, start with the
                # first node pair and loop the node pairs together.
                extra_loop_check = []
                extra_loop_check.append(node_pairs_in_loop[0])
                collection_of_branches = [copy_of_all_branches[0]]
                del copy_of_all_branches[0]
                origin_node = node_pairs_in_loop[0][0]
                next_node = node_pairs_in_loop[0][1]
                del node_pairs_in_loop[0]
                loop_closed = "no"
                loop_changed = "no"
                c2 = 0
                # The search algorithm will keep adding node pairs (branches)
                # such that continuity is maintained. The end condition
                # is when one of the nodes in a branch is the same as the origin node.
                while c2<len(node_pairs_in_loop) and loop_closed=="no":
                    # If the start node in a branch is the next node expected
                    # by the search algorithm, add this branch. Also, the next
                    # node will the end node of this branch. When a branch is
                    # added, delete the branch from the node pair list.
                    if node_pairs_in_loop[c2][0]==next_node:
                        next_node = node_pairs_in_loop[c2][1]
                        extra_loop_check.append(node_pairs_in_loop[c2])
                        collection_of_branches.append(copy_of_all_branches[c2])
                        loop_changed = "yes"
                        if node_pairs_in_loop[c2][1]==origin_node:
                            loop_closed = "yes"
                        del node_pairs_in_loop[c2]
                        del copy_of_all_branches[c2]
                    elif node_pairs_in_loop[c2][1]==next_node:
                        next_node = node_pairs_in_loop[c2][0]
                        extra_loop_check.append([node_pairs_in_loop[c2][1], node_pairs_in_loop[c2][0]])
                        collection_of_branches.append(copy_of_all_branches[c2])
                        loop_changed = "yes"
                        if node_pairs_in_loop[c2][0]==origin_node:
                            loop_closed = "yes"
                        del node_pairs_in_loop[c2]
                        del copy_of_all_branches[c2]

                    c2 += 1
                    # In an iteration if a branch is added, it means the loop
                    # has changed and the algorithm should continue. So the
                    # branch counter is rewound if the last branch has been reached.
                    # If no branch has been added, the branch count will stop
                    # at the last branch and terminate the search.
                    if c2>=len(node_pairs_in_loop) and loop_changed=="yes":
                        c2 = 0
                        loop_changed = "no"

        print(loop_index, end=" ")
        for c2 in collection_of_branches:
            if not resultant_loop[c2]=="no":
                print(branch_tags_in_loops[c2], end=" ")
        print()


        for c2 in collection_of_branches:
            if resultant_loop[c2]=="forward" or resultant_loop[c2]=="stiff_forward":
                print(NwRdr.human_loop(branch_params[c2][:-1]), end=" ")
            if resultant_loop[c2]=="reverse" or resultant_loop[c2]=="stiff_reverse":
                print(NwRdr.human_loop(branch_params[c2][:-1][::-1]), end=" ")
        print()
        print()

    return




def loop_validity_checking(resultant_loop, branches_in_kcl_nodes, kcl_branch_map):
    """
    This part of the function is to check if the loop is a genuine loop.
    A loop is genuine only if every node in the loop occurs exactly twice,
    the loop closes with the end node being the same as the beginning node
    while progressing through branches along the loop.
    Finally there should be no additional branches besides those inside
    the closed loop.
    """

    all_branches_in_loop = []
    branches_in_loop = []
    nodes_in_loop = []
    node_pairs_in_loop = []
    for c2 in range(len(resultant_loop)):
        if not resultant_loop[c2]=="no":
            branch_nodes = []
            for c3 in range(len(branches_in_kcl_nodes)):
                if c2 in branches_in_kcl_nodes[c3]:
                    if c3 not in branch_nodes:
                        branch_nodes.append(c3)

            # For every branch that is found, the branch is
            # added to all branches found. And the KCL nodes
            # that are the end nodes of the branch are added
            # as a node pair.
            node_pairs_in_loop.append(branch_nodes)
            all_branches_in_loop.append(c2)


    nodes_matching = "yes"
    if all_branches_in_loop:
        # Starting with the first branch found in the
        # loop, trace the loop :
        # This means - origin node is the first node
        # of the first branch. The "next" node is the
        # second node of the branch.
        branches_in_loop.append(all_branches_in_loop[0])
        next_node = node_pairs_in_loop[0][1]
        nodes_in_loop.append(next_node)

        # First check is if all nodes in the loop
        # occur as node pairs. If that fails, it is
        # not a loop and the entire check can exit.
        for c2 in range(len(node_pairs_in_loop)):
            for c3 in range(len(node_pairs_in_loop[c2])):
                node_occur = 1
                for c4 in range(len(node_pairs_in_loop)):
                    if not c4==c2:
                        if node_pairs_in_loop[c4][0]==node_pairs_in_loop[c2][c3]:
                            node_occur += 1
                        if node_pairs_in_loop[c4][1]==node_pairs_in_loop[c2][c3]:
                            node_occur += 1

                if not node_occur==2:
                    nodes_matching = "no"


        copy_of_node_pairs = []
        for c1 in node_pairs_in_loop:
            copy_of_node_pairs.append(c1)

        # If the loop branches are valid, check if the direction
        # of the branches in the loop are correct. Also check if
        # two completely separate loops with common nodes are not
        # present in a single loop.
        if nodes_matching=="yes":
            # To check for more than one loop, start with the
            # first node pair and loop the node pairs together.
            extra_loop_check = []
            extra_loop_check.append(node_pairs_in_loop[0])
            origin_node = node_pairs_in_loop[0][0]
            next_node = node_pairs_in_loop[0][1]
            del node_pairs_in_loop[0]
            loop_closed = "no"
            loop_changed = "no"
            c2 = 0
            # The search algorithm will keep adding node pairs (branches)
            # such that continuity is maintained. The end condition
            # is when one of the nodes in a branch is the same as the origin node.
            while c2<len(node_pairs_in_loop) and loop_closed=="no":
                # If the start node in a branch is the next node expected
                # by the search algorithm, add this branch. Also, the next
                # node will the end node of this branch. When a branch is
                # added, delete the branch from the node pair list.
                if node_pairs_in_loop[c2][0]==next_node:
                    next_node = node_pairs_in_loop[c2][1]
                    extra_loop_check.append(node_pairs_in_loop[c2])
                    loop_changed = "yes"
                    if node_pairs_in_loop[c2][1]==origin_node:
                        loop_closed = "yes"
                    del node_pairs_in_loop[c2]
                elif node_pairs_in_loop[c2][1]==next_node:
                    next_node = node_pairs_in_loop[c2][0]
                    extra_loop_check.append([node_pairs_in_loop[c2][1], node_pairs_in_loop[c2][0]])
                    loop_changed = "yes"
                    if node_pairs_in_loop[c2][0]==origin_node:
                        loop_closed = "yes"
                    del node_pairs_in_loop[c2]

                c2 += 1
                # In an iteration if a branch is added, it means the loop
                # has changed and the algorithm should continue. So the
                # branch counter is rewound if the last branch has been reached.
                # If no branch has been added, the branch count will stop
                # at the last branch and terminate the search.
                if c2>=len(node_pairs_in_loop) and loop_changed=="yes":
                    c2 = 0
                    loop_changed = "no"


            # If a single loop was found above, the node pair list
            # should be empty as all the branches have been added to
            # the loop. If multiple loops have been found, there
            # will be a difference between the number of branches
            # found in the above search and the number of branches
            # in the original loop.
            if not len(copy_of_node_pairs)==len(extra_loop_check):
                nodes_matching = "no"
            else:
                # Checking for directions.
                # If there are only 2 branches in a loop, it is
                # a special case, as it is a parallel loop between
                # a pair of nodes. Iterate through the two branches
                # check if the node pair between which the branches
                # appear is in the same direction as the direction in the
                # KCL branch map. If not, reverse the direction in the loop.
                if len(extra_loop_check)==2:
                    for c2 in range(len(extra_loop_check)):
                        branch_pos = all_branches_in_loop[c2]
                        if kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]]:
                            for c3 in range(len(kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]][0])):
                                if kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]][0][c3]==branch_pos:
                                    if kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]][1][c3]==1.0:
                                        if resultant_loop[branch_pos]=="reverse":
                                            resultant_loop[branch_pos] = "forward"
                                        if resultant_loop[branch_pos]=="stiff_reverse":
                                            resultant_loop[branch_pos] = "stiff_forward"
                                    elif kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]][1][c3]==-1.0:
                                        if resultant_loop[branch_pos]=="stiff_forward":
                                            resultant_loop[branch_pos] = "stiff_reverse"
                                        if resultant_loop[branch_pos]=="forward":
                                            resultant_loop[branch_pos] = "reverse"
                else:
                    # If there are more than 2 branches, iterate through
                    # all the branches. For a branch, check if the direction
                    # of the branch in the loop for a given node pair is the
                    # same as the direction of the branch between that node
                    # pair in KCL branch map. If not, reverse the direction in the loop.
                    for c2 in range(len(extra_loop_check)):
                        if extra_loop_check[c2] in copy_of_node_pairs:
                            branch_pos = all_branches_in_loop[copy_of_node_pairs.index(extra_loop_check[c2])]
                        elif [extra_loop_check[c2][1], extra_loop_check[c2][0]] in copy_of_node_pairs:
                            branch_pos = all_branches_in_loop[copy_of_node_pairs.index([extra_loop_check[c2][1], extra_loop_check[c2][0]])]

                        if kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]]:
                            for c3 in range(len(kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]][0])):
                                if kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]][0][c3]==branch_pos:
                                    if kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]][1][c3]==1.0:
                                        if resultant_loop[branch_pos]=="reverse":
                                            resultant_loop[branch_pos] = "forward"
                                        if resultant_loop[branch_pos]=="stiff_reverse":
                                            resultant_loop[branch_pos] = "stiff_forward"
                                    elif kcl_branch_map[extra_loop_check[c2][0]][extra_loop_check[c2][1]][1][c3]==-1.0:
                                        if resultant_loop[branch_pos]=="stiff_forward":
                                            resultant_loop[branch_pos] = "stiff_reverse"
                                        if resultant_loop[branch_pos]=="forward":
                                            resultant_loop[branch_pos] = "reverse"


    if nodes_matching=="no":
        is_valid_loop = "no"
    else:
        is_valid_loop = "yes"

    return is_valid_loop





def nonstiff_loop_manipulations(sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, row1, row2, manip_sense):
    """
    This function manipulates one loop with respect to another loop.
    This operation is similar to the row operations on matrices except
    that the operation is performed on the KVL loops.
    """

    resultant_loop = []
    for c3 in range(len(sys_loop_map[0])):
        resultant_loop.append(sys_loop_map[row2][c3])


    if manip_sense == "difference":
        for c2 in range(len(sys_loop_map[0])):
            if sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "forward"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "reverse"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_forward"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_reverse"

    else:
        for c2 in range(len(sys_loop_map[0])):
            if sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "reverse"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "forward"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_reverse"


            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_forward"


    # Checking loop validity
    is_valid_loop = loop_validity_checking(resultant_loop, branches_in_kcl_nodes, kcl_branch_map)
    # Only if the loop is valid will the loop manipulation be
    # added to the system loop map.
    if is_valid_loop=="no":
        resultant_loop = []

    return resultant_loop




def loop_manipulations(sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, row1, row2, manip_sense, branch_params, branch_tags_in_loops, stiff_info):
    """
    This function manipulates one loop with respect to another loop.
    This operation is similar to the row operations on matrices except
    that the operation is performed on the KVL loops.
    """

    resultant_loop = []
    for c3 in range(len(sys_loop_map[0])):
        resultant_loop.append(sys_loop_map[row2][c3])


    if manip_sense == "difference":
        for c2 in range(len(sys_loop_map[0])):
            if sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "forward"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "reverse"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_forward"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_reverse"

    else:

        for c2 in range(len(sys_loop_map[0])):
            if sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "reverse"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "forward"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_reverse"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_forward"


    # The resultant loop may have more than one loop so split these loops.
    new_resultant_loop = splitting_loops(resultant_loop, branches_in_kcl_nodes, kcl_branch_map, branch_params, branch_tags_in_loops)


    # If at least one loop is found, the first loop becomes the second
    # loop in the function argument. The additional loops are added to the
    # system loop map as extras.
    if new_resultant_loop:
        loop_exists = "no"
        for c2 in range(len(new_resultant_loop)):
            for c3 in range(len(new_resultant_loop[c2])):
                if not new_resultant_loop[c2][c3]=="no":
                    loop_exists = "yes"

        if loop_exists=="yes":
            for c2 in range(len(new_resultant_loop[0])):
                sys_loop_map[row2][c2] = new_resultant_loop[0][c2]
            # Check if the resultant is a nonstiff loop.
            # If so, make sure it follows path of least resistance.
            # Check if every branch in loop is the lowest resistance
            # if that branch has parallel branches.
            loop_is_nonstiff = True
            for c2 in range(len(sys_loop_map[row2])):
                if sys_loop_map[row2][c2]=="stiff_forward" or sys_loop_map[row2][c2]=="stiff_reverse":
                    loop_is_nonstiff = False
            if loop_is_nonstiff:
                loop_min_res_path(sys_loop_map, kcl_branch_map, stiff_info, branch_params, row2)
    else:
        for c2 in range(len(sys_loop_map[row2])):
            sys_loop_map[row2][c2] = "no"

    if len(new_resultant_loop)>1:
        for c2 in range(1, len(new_resultant_loop)):
            sys_loop_map.append([])
            for c3 in range(len(new_resultant_loop[c2])):
                sys_loop_map[-1].append(new_resultant_loop[c2][c3])
            # Check if resultants are nonstiff loops.
            # If so, make sure it follows path of least resistance.
            # Check if every branch in loop is the lowest resistance
            # if that branch has parallel branches.
            loop_is_nonstiff = True
            for c2 in range(len(sys_loop_map[-1])):
                if sys_loop_map[-1][c2]=="stiff_forward" or sys_loop_map[-1][c2]=="stiff_reverse":
                    loop_is_nonstiff = False
            if loop_is_nonstiff:
                loop_min_res_path(sys_loop_map, kcl_branch_map, stiff_info, branch_params, len(sys_loop_map)-1)

    return



def traditional_loop_manipulations(sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, row1, row2, manip_sense):
    """
    This function manipulates one loop with respect to another loop.
    This operation is similar to the row operations on matrices except
    that the operation is performed on the KVL loops.
    """

    resultant_loop = []
    for c3 in range(len(sys_loop_map[0])):
        resultant_loop.append(sys_loop_map[row2][c3])


    if manip_sense == "difference":
        for c2 in range(len(sys_loop_map[0])):
            if sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "forward"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "reverse"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_forward"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_reverse"

    else:

        for c2 in range(len(sys_loop_map[0])):
            if sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "reverse"

            elif sys_loop_map[row1][c2]=="forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "forward"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_forward":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="stiff_reverse":
                resultant_loop[c2] = "no"

            elif sys_loop_map[row1][c2]=="stiff_reverse" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_reverse"

            elif sys_loop_map[row1][c2]=="stiff_forward" and sys_loop_map[row2][c2]=="no":
                resultant_loop[c2] = "stiff_forward"


    is_loop_valid = loop_validity_checking(resultant_loop, branches_in_kcl_nodes, kcl_branch_map)

    if is_loop_valid=="yes":
        for c2 in range(len(resultant_loop)):
            sys_loop_map[row2][c2] = resultant_loop[c2]

    return





def recalculate_sys_matrices(sys_loop_map, nonstiff_loops, branch_info, matrix_a, matrix_e, matrix_b, dt):
    """
    Recalculate the system matrices after loop manipulation.
    """

    for c1 in range(len(nonstiff_loops)):
        for c2 in range(c1, len(nonstiff_loops)):
            loop1 = nonstiff_loops[c1]
            loop2 = nonstiff_loops[c2]
            # Diagonal elements are special
            # For A,E matrices, only addition takes place.
            if c1==c2:
                for c3 in range(len(branch_info)):
                    # Check if branch exists in loop
                    if not sys_loop_map[loop1][c3]=="no":
                        matrix_a.data[c1][c2] += branch_info[c3][-1][0][0]
                        matrix_e.data[c1][c2] += branch_info[c3][-1][0][1]
                        # Check direction before adding voltages.
                        if sys_loop_map[loop1][c3]=="forward" or sys_loop_map[loop1][c3]=="stiff_forward":
                            for c5 in range(matrix_b.columns):
                                matrix_b.data[c1][c5] += branch_info[c3][-1][1][c5]
                        elif sys_loop_map[loop1][c3]=="reverse" or sys_loop_map[loop1][c3]=="stiff_reverse":
                            for c5 in range(matrix_b.columns):
                                matrix_b.data[c1][c5] -= branch_info[c3][-1][1][c5]

            # For off-diagonal elements, interaction between loops
            else:
                for c3 in range(len(branch_info)):
                    if sys_loop_map[loop1][c3]=="forward" or sys_loop_map[loop1][c3]=="stiff_forward":
                        if sys_loop_map[loop2][c3]=="forward" or sys_loop_map[loop2][c3]=="stiff_forward":
                            matrix_a.data[c1][c2] += branch_info[c3][-1][0][0]
                            matrix_e.data[c1][c2] += branch_info[c3][-1][0][1]

                        elif sys_loop_map[loop2][c3]=="reverse" or sys_loop_map[loop2][c3]=="stiff_reverse":
                            matrix_a.data[c1][c2] -= branch_info[c3][-1][0][0]
                            matrix_e.data[c1][c2] -= branch_info[c3][-1][0][1]

                    elif sys_loop_map[loop1][c3]=="reverse" or sys_loop_map[loop1][c3]=="stiff_reverse":
                        if sys_loop_map[loop2][c3]=="reverse" or sys_loop_map[loop2][c3]=="stiff_reverse":
                            matrix_a.data[c1][c2] += branch_info[c3][-1][0][0]
                            matrix_e.data[c1][c2] += branch_info[c3][-1][0][1]

                        elif sys_loop_map[loop2][c3]=="forward" or sys_loop_map[loop2][c3]=="stiff_forward":
                            matrix_a.data[c1][c2] -= branch_info[c3][-1][0][0]
                            matrix_e.data[c1][c2] -= branch_info[c3][-1][0][1]


    # Matrices A and E are symmetrical.
    for c1 in range(len(nonstiff_loops)):
        for c2 in range(c1):
            if not c1==c2:
                matrix_a.data[c1][c2] = matrix_a.data[c2][c1]
                matrix_e.data[c1][c2] = matrix_e.data[c2][c1]


    for c1 in range(matrix_e.rows):
        if abs(matrix_e.data[c1][c1]/matrix_a.data[c1][c1])<10.0*dt:
            matrix_e.data[c1][c1] = 0.0

    # Approximate very small numbers to zero.
    for c1 in range(matrix_a.rows):
        for c2 in range(matrix_a.columns):
            if abs(matrix_a.data[c1][c2])<1.0e-10:
                matrix_a.data[c1][c2] = 0.0

    for c1 in range(matrix_e.rows):
        for c2 in range(matrix_e.columns):
            if abs(matrix_e.data[c1][c2])<1.0e-10:
                matrix_e.data[c1][c2] = 0.0

    for c1 in range(matrix_b.rows):
        for c2 in range(matrix_b.columns):
            if abs(matrix_b.data[c1][c2])<1.0e-10:
                matrix_b.data[c1][c2] = 0.0

    return



def remove_stiffness_old(sys_loop_map, state_vectors, loop_stiff_info, branches_in_kcl_nodes, kcl_branch_map):
    """
    Reduces the stiffness of the ODE by limiting the
    appearance of stiff branches in the loops.
    """

    # First to find the stiff loops by locating the first branch
    # that is stiff. After that make all the loops below that loop
    # have no element for that stiff branch.

    # To first arrange the loops such that the first branch
    # that is stiff occurs in the first loop and so on.

    loop_manip_event_occurred = "yes"

    while loop_manip_event_occurred=="yes":
        loop_manip_event_occurred = "no"

        map_loop_count = 0
        map_branch_count = 0
        # Start with the first branch of the first loop.
        while map_loop_count<len(sys_loop_map):

            if map_branch_count<len(sys_loop_map[0]):
                if sys_loop_map[map_loop_count][map_branch_count]=="stiff_forward" or \
                            sys_loop_map[map_loop_count][map_branch_count]=="stiff_reverse":

                    loop_found = "yes"
                else:
                    loop_found = "no"

            # If a loop is not found and the branches are not exhausted.
            while loop_found=="no" and map_branch_count<len(sys_loop_map[0]):
                # Check if the branch is stiff in the loop.
                if sys_loop_map[map_loop_count][map_branch_count]=="stiff_forward" or \
                            sys_loop_map[map_loop_count][map_branch_count]=="stiff_reverse":
                    loop_found = "yes"

                # If not, look at all the remaining loops corresponding to that branch.
                # The idea is that if a branch is stiff, it will appear in at least
                # one loop and so need to look through all loops to make sure it is
                # not missed.
                c1 = map_loop_count+1
                while loop_found=="no" and c1<len(sys_loop_map):
                    if sys_loop_map[c1][map_branch_count]=="stiff_forward" or \
                                sys_loop_map[c1][map_branch_count]=="stiff_reverse":

                        for c2 in range(len(sys_loop_map[0])):
                            # If a subsequenct loop is found to have the branch as stiff,
                            # interchange the rows.
                            sys_loop_map[c1][c2], sys_loop_map[map_loop_count][c2] = \
                                        sys_loop_map[map_loop_count][c2], sys_loop_map[c1][c2]

                        state_vectors[0].data[c1][0], state_vectors[0].data[map_loop_count][0] = \
                                    state_vectors[0].data[map_loop_count][0], state_vectors[0].data[c1][0]
                        state_vectors[1].data[c1][0], state_vectors[1].data[map_loop_count][0] = \
                                    state_vectors[1].data[map_loop_count][0], state_vectors[1].data[c1][0]
                        loop_stiff_info[c1], loop_stiff_info[map_loop_count] = loop_stiff_info[map_loop_count], loop_stiff_info[c1]
                        loop_found = "yes"

                    c1 += 1
                # If all loops are exhausted and no element is found as stiff
                # for the branch, it means the branch is not stiff
                # or has been accounted in a previous loop.
                # So move on to the next branch.
                if loop_found=="no":
                    map_branch_count += 1


            # If a loop has been found, the loops need to be made as upper triangular
            # So all stiff branches in the loops subsequent to the loop will have to eliminated.
            if loop_found=="yes":

                for c1 in range(len(sys_loop_map)):
                    if not c1==map_loop_count:
                        if sys_loop_map[c1][map_branch_count]=="stiff_forward" or \
                                    sys_loop_map[c1][map_branch_count]=="stiff_reverse":

                            # This is simply row operation of loops.
                            if sys_loop_map[map_loop_count][map_branch_count]==sys_loop_map[c1][map_branch_count]:
                                manip_result = loop_manipulations(sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, \
                                            c1, "difference")
                            else:
                                manip_result = loop_manipulations(sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, \
                                            c1, "addition")

                            if manip_result:
                                loop_manip_event_occurred = "yes"


            # Increment the loop count and make the branch count equal that
            # So the default is a diagonal stiff element.
            map_loop_count += 1
            map_branch_count = map_loop_count


    # Get rid of repeating loops by setting all branches "no"
    for c1 in range(len(sys_loop_map)-1):
        for c2 in range(c1+1, len(sys_loop_map)):
            loop_repeats = "yes"
            for c3 in range(len(sys_loop_map[c1])):
                if not sys_loop_map[c1][c3]==sys_loop_map[c2][c3]:
                    loop_repeats = "no"

            if loop_repeats=="yes":
                for c3 in range(len(sys_loop_map[c2])):
                    sys_loop_map[c2][c3] = "no"


    for c1 in range(len(sys_loop_map)-1,  -1,  -1):
        if "forward" in sys_loop_map[c1] or "reverse" in sys_loop_map[c1] or "stiff_forward" in sys_loop_map[c1] or \
                    "stiff_reverse" in sys_loop_map[c1]:
            pass
        else:
            del sys_loop_map[c1]

    return


def connected_networks(sys_loop_map, branches_in_kcl_nodes):
    """
    This function takes the branch and node information and
    splits the circuit up into connected parts. This is essential
    when a circuit is magnetically coupled using transformers or
    other machines but have no electrical coupling. Usually the
    number of loops is equal to B-N+1. Here 1 indicates the number
    of connected parts. Therefore, if the number of connected parts
    is greater than 1 due to a transformer, the number of loops
    expected has to change to B-N+C where C is the number of
    connected sub-circuits.
    """

    # All branches in the circuit.
    sys_branches = list(range(len(sys_loop_map[0])))

    list_of_branches_in_maps = []
    connected_branch_map = []
    while sys_branches:
        connected_branch_map.append([])
        list_of_branches_in_maps.append([])
        for c1 in range(len(branches_in_kcl_nodes)):
            connected_branch_map[-1].append([])

        # A given sub-crcuit starts with the first branch
        # remaining in the list of branches.
        for c1 in range(len(branches_in_kcl_nodes)):
            if sys_branches[0] in branches_in_kcl_nodes[c1]:
                connected_branch_map[-1][c1].append(sys_branches[0])
                if sys_branches[0] not in list_of_branches_in_maps[-1]:
                    list_of_branches_in_maps[-1].append(sys_branches[0])
        del sys_branches[0]

        # Keep adding branches to this sub-circuit until
        # the search algorithm can't find any other branches.
        any_branch_found = "yes"
        while any_branch_found=="yes":
            any_branch_found = "no"
            for c1 in range(len(sys_branches)-1, -1, -1):
                branch_found = "no"
                no_of_findings = 0
                for c2 in range(len(branches_in_kcl_nodes)):
                    # If the current non-stiff branch is incident at a node
                    # where the current sub-circuit has already added a branch,
                    # then the branch is added. This way, the sub-circuit grows.
                    if sys_branches[c1] in branches_in_kcl_nodes[c2]:
                        if connected_branch_map[-1][c2]:
                            connected_branch_map[-1][c2].append(sys_branches[c1])
                            no_of_findings += 1
                            branch_found = "yes"
                            any_branch_found = "yes"

                if branch_found=="yes":
                    if no_of_findings<2:
                        for c3 in range(len(branches_in_kcl_nodes)):
                            if sys_branches[c1] in branches_in_kcl_nodes[c3]:
                                if sys_branches[c1] not in connected_branch_map[-1][c3]:
                                    connected_branch_map[-1][c3].append(sys_branches[c1])

                    if sys_branches[c1] not in list_of_branches_in_maps[-1]:
                        list_of_branches_in_maps[-1].append(sys_branches[c1])
                    del sys_branches[c1]

    return len(connected_branch_map)


def remove_stiffness(sys_loop_map, state_vectors, loop_stiff_info, branches_in_kcl_nodes, kcl_branch_map, branch_params, branch_tags_in_loops, stiff_info):
    """
    Reduces the stiffness of the ODE by limiting the
    appearance of stiff branches in the loops.
    """

    # First to find the stiff loops by locating the first branch
    # that is stiff. After that make all the loops below that loop
    # have no element for that stiff branch.

    # To first arrange the loops such that the first branch
    # that is stiff occurs in the first loop and so on.

    # Make a list of the non-stiff branches.
    nonstiff_branches = []
    list_of_nonstiff_branches = []
    for c1 in range(len(sys_loop_map[0])):
        for c2 in range(len(sys_loop_map)):
            if sys_loop_map[c2][c1]=="forward" or sys_loop_map[c2][c1]=="reverse":
                if c1 not in nonstiff_branches:
                    nonstiff_branches.append(c1)
                    list_of_nonstiff_branches.append(c1)


    # The branches in the circuit are divided into
    # separate connected circuits. A branch is added
    # to the sub-circuit only if one of the nodes
    # of the branch are already present in the circuit
    # and have been added previously by another branch.

    # Connected branch map is basically the branches_in_kcl_nodes
    # list broken up into separate sub-circuits
    list_of_branches_in_maps = []
    connected_branch_map = []
    while nonstiff_branches:
        connected_branch_map.append([])
        list_of_branches_in_maps.append([])
        for c1 in range(len(branches_in_kcl_nodes)):
            connected_branch_map[-1].append([])

        # A given sub-crcuit starts with the first non-stiff branch
        # remaining in the list of non-stiff branches.
        for c1 in range(len(branches_in_kcl_nodes)):
            if nonstiff_branches[0] in branches_in_kcl_nodes[c1]:
                connected_branch_map[-1][c1].append(nonstiff_branches[0])
                if nonstiff_branches[0] not in list_of_branches_in_maps[-1]:
                    list_of_branches_in_maps[-1].append(nonstiff_branches[0])
        del nonstiff_branches[0]

        # Keep adding branches to this sub-circuit until
        # the search algorithm can't find any other branches.
        any_branch_found = "yes"
        while any_branch_found=="yes":
            any_branch_found = "no"
            for c1 in range(len(nonstiff_branches)-1, -1, -1):
                branch_found = "no"
                no_of_findings = 0
                for c2 in range(len(branches_in_kcl_nodes)):
                    # If the current non-stiff branch is incident at a node
                    # where the current sub-circuit has already added a branch,
                    # then the branch is added. This way, the sub-circuit grows.
                    if nonstiff_branches[c1] in branches_in_kcl_nodes[c2]:
                        if connected_branch_map[-1][c2]:
                            connected_branch_map[-1][c2].append(nonstiff_branches[c1])
                            no_of_findings += 1
                            branch_found = "yes"
                            any_branch_found = "yes"

                if branch_found=="yes":
                    if no_of_findings<2:
                        for c3 in range(len(branches_in_kcl_nodes)):
                            if nonstiff_branches[c1] in branches_in_kcl_nodes[c3]:
                                if nonstiff_branches[c1] not in connected_branch_map[-1][c3]:
                                    connected_branch_map[-1][c3].append(nonstiff_branches[c1])

                    if nonstiff_branches[c1] not in list_of_branches_in_maps[-1]:
                        list_of_branches_in_maps[-1].append(nonstiff_branches[c1])
                    del nonstiff_branches[c1]


    # Calculate the number of non-stiff loops.
    no_of_nonstiff_loops = 0
    if connected_branch_map:
        for c1 in range(len(connected_branch_map)):
            if connected_branch_map[c1]:
                no_of_nodes = 0
                no_of_branches = len(list_of_branches_in_maps[c1])
                for c2 in range(len(connected_branch_map[c1])):
                    if connected_branch_map[c1][c2]:
                        no_of_nodes += 1

                no_of_nonstiff_loops += no_of_branches - no_of_nodes + 1

    # Calculate the number of stiff loops expected
    no_of_loops = len(sys_loop_map[0]) - len(branches_in_kcl_nodes) + connected_networks(sys_loop_map, branches_in_kcl_nodes)
#    no_of_stiff_loops = no_of_loops - no_of_nonstiff_loops - 1
    no_of_stiff_loops = no_of_loops - no_of_nonstiff_loops


    # Create two loop maps - one for stiff lops and the other
    # for non-stiff loops.
    stiff_sys_loop_map = []
    nonstiff_sys_loop_map = []

    # Now add loops with only two branches. Check for all branches
    # connected in parallel from kcl_branch_map. As before, find
    # out the branch with minimum resistance. All loops between
    # these parallel branches will have the branch with minimum
    # resistance a common branch. This again ensures the concept
    # of loops choosing the path of least resistance.
    for c1 in range(len(kcl_branch_map)):
        for c2 in range(c1+1, len(kcl_branch_map)):
            if kcl_branch_map[c1][c2]:
                if len(kcl_branch_map[c1][c2][0])>1:
                    min_res_branch_found = "no"
                    for c3 in range(len(kcl_branch_map[c1][c2][0])):
                        if stiff_info[kcl_branch_map[c1][c2][0][c3]]=="no":
                            min_res_branch = kcl_branch_map[c1][c2][0][c3]
                            min_res_branch_found = "yes"

                    if min_res_branch_found=="yes":
                        for c3 in range(1, len(kcl_branch_map[c1][c2][0])):
                            if stiff_info[kcl_branch_map[c1][c2][0][c3]]=="no":
                                if branch_params[min_res_branch][-1][0][0]>branch_params[kcl_branch_map[c1][c2][0][c3]][-1][0][0]:
                                    min_res_branch = kcl_branch_map[c1][c2][0][c3]

                        for c3 in range(len(kcl_branch_map[c1][c2][0])):
                            if stiff_info[kcl_branch_map[c1][c2][0][c3]]=="no":
                                if not kcl_branch_map[c1][c2][0][c3]==min_res_branch:
                                    row_vector = []
                                    for c4 in range(len(branch_params)):
                                        row_vector.append("no")
                                    min_res_branch_pos = kcl_branch_map[c1][c2][0].index(min_res_branch)
                                    if kcl_branch_map[c1][c2][1][min_res_branch_pos]==1:
                                        row_vector[min_res_branch] = "forward"
                                    else:
                                        row_vector[min_res_branch] = "reverse"

                                    if kcl_branch_map[c1][c2][1][c3]==1:
                                        row_vector[kcl_branch_map[c1][c2][0][c3]] = "reverse"
                                    else:
                                        row_vector[kcl_branch_map[c1][c2][0][c3]] = "forward"

                                    nonstiff_sys_loop_map.append(row_vector)

    # This variable keeps track of the number of non-stiff
    # parallel branches added as non-stiff loops.
    parallel_nonstiff_branches = len(nonstiff_sys_loop_map)

    # Split the loops already in sys_loop_map into
    # stiff and non-stiff lists.
    for c1 in range(len(sys_loop_map)):
        first_loop_nonstiff = "yes"
        for c2 in range(len(sys_loop_map[c1])):
            if sys_loop_map[c1][c2]=="stiff_forward" or sys_loop_map[c1][c2]=="stiff_reverse":
                first_loop_nonstiff = "no"

        if first_loop_nonstiff=="no":
            row_vector = []
            for c2 in range(len(sys_loop_map[c1])):
                row_vector.append(sys_loop_map[c1][c2])
            stiff_sys_loop_map.append(row_vector)
        else:
            loop_min_res_path(sys_loop_map, kcl_branch_map, stiff_info, branch_params, c1)
            row_vector = []
            for c2 in range(len(sys_loop_map[c1])):
                row_vector.append(sys_loop_map[c1][c2])
            nonstiff_sys_loop_map.append(row_vector)


    # Delete the loops with two branches as these have
    # been added already with minimum resistance branch.
    for c1 in range(len(nonstiff_sys_loop_map)-1, parallel_nonstiff_branches-1, -1):
        number_of_branches = 0
        for c2 in range(len(nonstiff_sys_loop_map[c1])):
            if not nonstiff_sys_loop_map[c1][c2]=="no":
                number_of_branches += 1
        if number_of_branches==2:
            del nonstiff_sys_loop_map[c1]


    # First manipulate the stiff loops. The objective is
    # to make the stiff loop map upper triangular. The loop
    # manipulations for stiff loops are different from the
    # loop manipulations for non-stiff loops. Two stiff loops
    # when manipulated will result in at least one loop. There
    # is no concept of compatible loops.
    loop_stiff_extracted = "no"
    while loop_stiff_extracted=="no":

        map_loop_count = 0
        map_branch_count = 0
        # Start with the first branch of the first loop.
        while map_loop_count<len(stiff_sys_loop_map):

            if map_branch_count<len(stiff_sys_loop_map[0]):
                if stiff_sys_loop_map[map_loop_count][map_branch_count]=="stiff_forward" or \
                            stiff_sys_loop_map[map_loop_count][map_branch_count]=="stiff_reverse":

                    loop_found = "yes"
                else:
                    loop_found = "no"

            # If a loop is not found and the branches are not exhausted.
            while loop_found=="no" and map_branch_count<len(stiff_sys_loop_map[0]):
                # Check if the branch is stiff in the loop.
                if stiff_sys_loop_map[map_loop_count][map_branch_count]=="stiff_forward" or \
                            stiff_sys_loop_map[map_loop_count][map_branch_count]=="stiff_reverse":
                    loop_found = "yes"

                # If not, look at all the remaining loops corresponding to that branch.
                # The idea is that if a branch is stiff, it will appear in at least
                # one loop and so need to look through all loops to make sure it is
                # not missed.
                c1 = map_loop_count+1
                while loop_found=="no" and c1<len(stiff_sys_loop_map):
                    if stiff_sys_loop_map[c1][map_branch_count]=="stiff_forward" or \
                                stiff_sys_loop_map[c1][map_branch_count]=="stiff_reverse":

                        for c2 in range(len(stiff_sys_loop_map[0])):
                            # If a subsequenct loop is found to have the branch as stiff,
                            # interchange the rows.
                            stiff_sys_loop_map[c1][c2], stiff_sys_loop_map[map_loop_count][c2] = \
                                        stiff_sys_loop_map[map_loop_count][c2], stiff_sys_loop_map[c1][c2]

                        loop_found = "yes"

                    c1 += 1
                # If all loops are exhausted and no element is found as stiff
                # for the branch, it means the branch is not stiff
                # or has been accounted in a previous loop.
                # So move on to the next branch.
                if loop_found=="no":
                    map_branch_count += 1


            # If a loop has been found, the loops need to be made as upper triangular
            # So all stiff branches in the loops subsequent to the loop will have to eliminated.
            if loop_found=="yes":
                # No need to attempt to make the stiff loop map diagonal.
                for c1 in range(len(stiff_sys_loop_map)):
#                for c1 in range(map_loop_count+1, len(stiff_sys_loop_map)):
                    if not c1==map_loop_count:
                        if stiff_sys_loop_map[c1][map_branch_count]=="stiff_forward" or \
                                    stiff_sys_loop_map[c1][map_branch_count]=="stiff_reverse":

                            # This is simply row operation of loops.
                            if stiff_sys_loop_map[map_loop_count][map_branch_count]==stiff_sys_loop_map[c1][map_branch_count]:
                                loop_manipulations(stiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, c1, \
                                            "difference", branch_params, branch_tags_in_loops, stiff_info)
                            else:
                                loop_manipulations(stiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, c1, \
                                            "addition", branch_params, branch_tags_in_loops, stiff_info)


            # Increment the loop count and make the branch count equal that
            # So the default is a diagonal stiff element.
            map_loop_count += 1
            map_branch_count = map_loop_count


        # Check if there are any non-stiff loops in the stiff
        # loop map. Move these to the non-stiff loop map.
        for c1 in range(len(stiff_sys_loop_map)-1, -1, -1):
            loop_is_nonstiff = "yes"
            for c2 in range(len(stiff_sys_loop_map[c1])):
                if stiff_sys_loop_map[c1][c2]=="stiff_forward" or stiff_sys_loop_map[c1][c2]=="stiff_reverse":
                    loop_is_nonstiff = "no"

            if loop_is_nonstiff=="yes":
                row_vector = []
                for c2 in range(len(stiff_sys_loop_map[c1])):
                    row_vector.append(stiff_sys_loop_map[c1][c2])
                nonstiff_sys_loop_map.append(row_vector)
                del stiff_sys_loop_map[c1]


        # If the number of stiff loops has exceeded the expected number
        # after a round of loop manipulations, these excess loops
        # can be deleted.
        if len(stiff_sys_loop_map)>=no_of_stiff_loops:
            for c1 in range(len(stiff_sys_loop_map)-1, no_of_stiff_loops-1, -1):
                del stiff_sys_loop_map[c1]
            loop_stiff_extracted = "yes"


    # Attempt to triangularize the non-stiff loop map. This may not
    # be possible as here compatibility of loops are checked.
    # The objective is to remove redundant loops that are a linear
    # combination of other loops.
#    map_loop_count = parallel_nonstiff_branches
    map_loop_count = 0
    map_branch_count = 0
    # Start with the first branch of the first loop.
    while map_loop_count<len(nonstiff_sys_loop_map):

        if map_branch_count<len(nonstiff_sys_loop_map[0]):
            if nonstiff_sys_loop_map[map_loop_count][map_branch_count]=="forward" or \
                        nonstiff_sys_loop_map[map_loop_count][map_branch_count]=="reverse":

                loop_found = "yes"
            else:
                loop_found = "no"

        # If a loop is not found and the branches are not exhausted.
        while loop_found=="no" and map_branch_count<len(nonstiff_sys_loop_map[0]):
            # Check if the branch is nonstiff in the loop.
            if nonstiff_sys_loop_map[map_loop_count][map_branch_count]=="forward" or \
                        nonstiff_sys_loop_map[map_loop_count][map_branch_count]=="reverse":
                loop_found = "yes"

            # If not, look at all the remaining loops corresponding to that branch.
            # The idea is that if a branch is stiff, it will appear in at least
            # one loop and so need to look through all loops to make sure it is
            # not missed.
            c1 = map_loop_count+1
            while loop_found=="no" and c1<len(nonstiff_sys_loop_map):
                if nonstiff_sys_loop_map[c1][map_branch_count]=="forward" or \
                            nonstiff_sys_loop_map[c1][map_branch_count]=="reverse":

                    for c2 in range(len(nonstiff_sys_loop_map[0])):
                        # If a subsequenct loop is found to have the branch as stiff,
                        # interchange the rows.
                        nonstiff_sys_loop_map[c1][c2], nonstiff_sys_loop_map[map_loop_count][c2] = \
                                    nonstiff_sys_loop_map[map_loop_count][c2], nonstiff_sys_loop_map[c1][c2]

                    loop_found = "yes"

                c1 += 1
            # If all loops are exhausted and no element is found as stiff
            # for the branch, it means the branch is not stiff
            # or has been accounted in a previous loop.
            # So move on to the next branch.
            if loop_found=="no":
                map_branch_count += 1


        # If a loop has been found, the loops need to be made as upper triangular
        # So all stiff branches in the loops subsequent to the loop will have to eliminated.
        if loop_found=="yes":
#           for c1 in range(len(sys_loop_map)):
            for c1 in range(map_loop_count+1, len(nonstiff_sys_loop_map)):
                if not c1==map_loop_count:
                    if nonstiff_sys_loop_map[c1][map_branch_count]=="forward" or \
                                nonstiff_sys_loop_map[c1][map_branch_count]=="reverse":

                        # This is simply row operation of loops.
                        if nonstiff_sys_loop_map[map_loop_count][map_branch_count]==nonstiff_sys_loop_map[c1][map_branch_count]:
#                            traditional_loop_manipulations(nonstiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, \
#                                            c1, "difference")
                            loop_manipulations(nonstiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, c1, \
                                            "difference", branch_params, branch_tags_in_loops, stiff_info)
#                            loop_min_res_path(nonstiff_sys_loop_map, kcl_branch_map, stiff_info, branch_params, c1)
                        else:
#                            traditional_loop_manipulations(nonstiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, \
#                                            c1, "addition")
                            loop_manipulations(nonstiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, c1, \
                                            "addition", branch_params, branch_tags_in_loops, stiff_info)
#                            loop_min_res_path(nonstiff_sys_loop_map, kcl_branch_map, stiff_info, branch_params, c1)


        # Increment the loop count and make the branch count equal that
        # So the default is a diagonal stiff element.
        map_loop_count += 1
        map_branch_count = map_loop_count


#    loop_nonstiff_extracted = "no"
#    while loop_nonstiff_extracted=="no":
#
#        map_loop_count = 0
#        map_branch_count = 0
#        # Start with the first branch of the first loop.
#        while map_loop_count<len(nonstiff_sys_loop_map):
#
#            if map_branch_count<len(nonstiff_sys_loop_map[0]):
#                if nonstiff_sys_loop_map[map_loop_count][map_branch_count]=="forward" or \
#                            nonstiff_sys_loop_map[map_loop_count][map_branch_count]=="reverse":
#
#                    loop_found = "yes"
#                else:
#                    loop_found = "no"
#
#            # If a loop is not found and the branches are not exhausted.
#            while loop_found=="no" and map_branch_count<len(nonstiff_sys_loop_map[0]):
#                # Check if the branch is nonstiff in the loop.
#                if nonstiff_sys_loop_map[map_loop_count][map_branch_count]=="forward" or \
#                            nonstiff_sys_loop_map[map_loop_count][map_branch_count]=="reverse":
#                    loop_found = "yes"
#
#                # If not, look at all the remaining loops corresponding to that branch.
#                # The idea is that if a branch is stiff, it will appear in at least
#                # one loop and so need to look through all loops to make sure it is
#                # not missed.
#                c1 = map_loop_count+1
#                while loop_found=="no" and c1<len(nonstiff_sys_loop_map):
#                    if nonstiff_sys_loop_map[c1][map_branch_count]=="forward" or \
#                                nonstiff_sys_loop_map[c1][map_branch_count]=="reverse":
#
#                        for c2 in range(len(nonstiff_sys_loop_map[0])):
#                            # If a subsequenct loop is found to have the branch as stiff,
#                            # interchange the rows.
#                            nonstiff_sys_loop_map[c1][c2], nonstiff_sys_loop_map[map_loop_count][c2] = \
#                                        nonstiff_sys_loop_map[map_loop_count][c2], nonstiff_sys_loop_map[c1][c2]
#
#                        loop_found = "yes"
#
#                    c1 += 1
#                # If all loops are exhausted and no element is found as stiff
#                # for the branch, it means the branch is not stiff
#                # or has been accounted in a previous loop.
#                # So move on to the next branch.
#                if loop_found=="no":
#                    map_branch_count += 1
#
#
#            # If a loop has been found, the loops need to be made as upper triangular
#            # So all stiff branches in the loops subsequent to the loop will have to eliminated.
#            if loop_found=="yes":
##                for c1 in range(len(sys_loop_map)):
#                for c1 in range(map_loop_count+1, len(nonstiff_sys_loop_map)):
#                    if not c1==map_loop_count:
#                        if nonstiff_sys_loop_map[c1][map_branch_count]=="forward" or \
#                                    nonstiff_sys_loop_map[c1][map_branch_count]=="reverse":
#
#                            # This is simply row operation of loops.
#                            if nonstiff_sys_loop_map[map_loop_count][map_branch_count]==nonstiff_sys_loop_map[c1][map_branch_count]:
#                                traditional_loop_manipulations(nonstiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, \
#                                                map_loop_count, c1, "difference")
##                                loop_manipulations(nonstiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, c1, "difference")
#                                loop_min_res_path(nonstiff_sys_loop_map, kcl_branch_map, stiff_info, branch_params, c1)
#                            else:
#                                traditional_loop_manipulations(nonstiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, \
#                                                map_loop_count, c1, "addition")
##                                loop_manipulations(nonstiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, map_loop_count, c1, "addition")
#                                loop_min_res_path(nonstiff_sys_loop_map, kcl_branch_map, stiff_info, branch_params, c1)
#
#
#            # Increment the loop count and make the branch count equal that
#            # So the default is a diagonal stiff element.
#            map_loop_count += 1
#            map_branch_count = map_loop_count
#
#        # Delete additional non-stiff loops.
#        if len(nonstiff_sys_loop_map)>=no_of_nonstiff_loops:
#            for c1 in range(len(nonstiff_sys_loop_map)-1, no_of_nonstiff_loops-1, -1):
#                del nonstiff_sys_loop_map[c1]
#            loop_nonstiff_extracted = "yes"


#    for c1 in range(len(nonstiff_sys_loop_map)):
#        loop_min_res_path(nonstiff_sys_loop_map, kcl_branch_map, stiff_info, branch_params, c1)

    # Combine the stiff loops and the non-stiff loops
    # back into a single loop map.
    row_index = 0
    for c1 in range(len(stiff_sys_loop_map)):
        if row_index>len(sys_loop_map)-1:
            row_vector = []
            for c2 in range(len(stiff_sys_loop_map[c1])):
                row_vector.append("no")
            sys_loop_map.append(row_vector)
        for c2 in range(len(stiff_sys_loop_map[c1])):
            sys_loop_map[row_index][c2] = stiff_sys_loop_map[c1][c2]
        row_index += 1

    for c1 in range(len(nonstiff_sys_loop_map)):
        if row_index>len(sys_loop_map)-1:
            row_vector = []
            for c2 in range(len(nonstiff_sys_loop_map[c1])):
                row_vector.append("no")
            sys_loop_map.append(row_vector)
        for c2 in range(len(nonstiff_sys_loop_map[c1])):
            sys_loop_map[row_index][c2] = nonstiff_sys_loop_map[c1][c2]
        row_index += 1

    if len(sys_loop_map)>(no_of_nonstiff_loops+no_of_stiff_loops):
        for c1 in range(len(sys_loop_map)-1, no_of_nonstiff_loops+no_of_stiff_loops-1, -1):
            del sys_loop_map[c1]


    # Get rid of repeating loops by setting all branches "no"
    for c1 in range(len(sys_loop_map)-1):
        for c2 in range(c1+1, len(sys_loop_map)):
            loop_repeats = "yes"
            for c3 in range(len(sys_loop_map[c1])):
                if not sys_loop_map[c1][c3]==sys_loop_map[c2][c3]:
                    loop_repeats = "no"

            if loop_repeats=="yes":
                for c3 in range(len(sys_loop_map[c2])):
                    sys_loop_map[c2][c3] = "no"


    for c1 in range(len(sys_loop_map)-1,  -1,  -1):
        if "forward" in sys_loop_map[c1] or "reverse" in sys_loop_map[c1] or "stiff_forward" in sys_loop_map[c1] or \
                        "stiff_reverse" in sys_loop_map[c1]:
            pass
        else:
            del sys_loop_map[c1]


    return


def stiff_equation_solver(matrix_e, matrix_a, matrix_b, state_vector, input_vector, dt, ode_row):
    """
    Solving stiff loops that are algebraic equations only
    """

    if not (matrix_a.data[ode_row][ode_row]):
        #The variable has no dynamics and can't even be calculated statically!
        # May be due to a redundant loop.
#        ode_vectors[4].data[ode_row][0] = 0.0
        state_vector[0].data[ode_row][0] = 0.0
        state_vector[1].data[ode_row][0] = 0.0
    else:

#        ode_vectors[4].data[ode_row][0] = 0.0
        state_vector[0].data[ode_row][0] = 0.0
        state_vector[1].data[ode_row][0] = 0.0
        try:
            if input_vector.rows:
                pass
        except:
            if not (matrix_b.columns==1):
                print("Input signal has to be a real number and not a vector.")
            else:
                state_vector[0].data[ode_row][0] += matrix_b.data[ode_row][0]*input_vector
                state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]
        else:
            if not (matrix_b.columns==input_vector.rows):
                print("Dimension of input vector incorrect.")
            else:
                for c2 in range(matrix_b.columns):
                    state_vector[0].data[ode_row][0] += matrix_b.data[ode_row][c2]*input_vector.data[c2][0]
                    state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]

        for c2 in range(matrix_a.columns):
            if not (ode_row==c2):
                state_vector[0].data[ode_row][0] -= matrix_a.data[ode_row][c2]*state_vector[1].data[c2][0]
                state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]


#        for c2 in range(matrix_e.columns):
#            state_vector[0].data[ode_row][0] -= matrix_e.data[ode_row][c2]*ode_vectors[4].data[c2][0]/dt
#            state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]


        state_vector[0].data[ode_row][0] = state_vector[0].data[ode_row][0]/matrix_a.data[ode_row][ode_row]
        state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]

    return



def listing_nonstiff_loops(sys_loop_map, branch_info):
    """
    Make a list of the nonstiff loops
    Because stiff loops will essentially have a negligible
    current.
    """

    nonstiff_loops = []
    for c1 in range(len(sys_loop_map)):
        # Check if loop c1 has a stiff branch
        is_loop_stiff = "no"
        for c2 in range(len(branch_info)):
            if sys_loop_map[c1][c2]=="stiff_forward" or sys_loop_map[c1][c2]=="stiff_reverse":
                is_loop_stiff = "yes"

        if is_loop_stiff=="no":
            nonstiff_loops.append(c1)

    return nonstiff_loops




def arrange_nonstiff_loops(matrix_e, matrix_a, matrix_b, matrix_u,  dt, branch_info, stiff_info, sys_loop_map, state_vector,  br_events):
    """
    Calculates the loop currents after an event from branch currents.
    """

    # Make a list of the nonstiff loops
    # Because stiff loops will essentially have a negligible
    # current.
    nonstiff_loops = listing_nonstiff_loops(sys_loop_map, branch_info)

    # Calculate the total inductance and the
    # total voltage in each loop.
    voltage_loop = []
    inductance_loop = []
    for c1 in nonstiff_loops:
        voltage_loop.append(0.0)
        inductance_loop.append(0.0)


    for c1 in nonstiff_loops:
        total_voltage = 0.0
        total_inductance = 0.0
        for c2 in range(len(sys_loop_map[c1])):

            if sys_loop_map[c1][c2]=="forward":
                total_inductance += branch_info[c2][-1][0][1]
                for c3 in range(len(branch_info[c2][-1][1])):
                    total_voltage += branch_info[c2][-1][1][c3]*matrix_u.data[c3][0]

            if sys_loop_map[c1][c2]=="reverse":
                total_inductance += branch_info[c2][-1][0][1]
                for c3 in range(len(branch_info[c2][-1][1])):
                    total_voltage -= branch_info[c2][-1][1][c3]*matrix_u.data[c3][0]

        voltage_loop[nonstiff_loops.index(c1)] = total_voltage
        inductance_loop[nonstiff_loops.index(c1)] = total_inductance


    # Arrange the loops in the following order.
    # The ODE will solve the equations from the last backwards.
    # So the non stiff loops need to be arranged in increasing order
    # of the voltage/inductance (di/dt) in the loop.
    # In case, the loop is static, the static loops will come first
    # and will be arranged in increasing order of the voltage in
    # the loop.
    for c1 in range(len(nonstiff_loops)-1):
        for c2 in range(c1+1,  len(nonstiff_loops)):
            if not inductance_loop[c1] and inductance_loop[c2]:
                first_loop = nonstiff_loops[c1]
                second_loop = nonstiff_loops[c2]
                voltage_loop[c1],  voltage_loop[c2] = voltage_loop[c2],  voltage_loop[c1]
                inductance_loop[c1],  inductance_loop[c2] = inductance_loop[c2],  inductance_loop[c1]

                for c3 in range(len(sys_loop_map[first_loop])):
                    sys_loop_map[first_loop][c3],  sys_loop_map[second_loop][c3] = sys_loop_map[second_loop][c3],  sys_loop_map[first_loop][c3]

            elif inductance_loop[c1]==0.0 and inductance_loop[c2]==0.0:
                if abs(voltage_loop[c1])>abs(voltage_loop[c2]):
                    first_loop = nonstiff_loops[c1]
                    second_loop = nonstiff_loops[c2]
                    voltage_loop[c1],  voltage_loop[c2] = voltage_loop[c2],  voltage_loop[c1]
                    inductance_loop[c1],  inductance_loop[c2] = inductance_loop[c2],  inductance_loop[c1]

                    for c3 in range(len(sys_loop_map[first_loop])):
                        sys_loop_map[first_loop][c3],  sys_loop_map[second_loop][c3] = sys_loop_map[second_loop][c3],  sys_loop_map[first_loop][c3]

            elif inductance_loop[c1] and inductance_loop[c2]:
                if abs(voltage_loop[c2]/inductance_loop[c2])<abs(voltage_loop[c1]/inductance_loop[c1]):
                    first_loop = nonstiff_loops[c1]
                    second_loop = nonstiff_loops[c2]
                    voltage_loop[c1],  voltage_loop[c2] = voltage_loop[c2],  voltage_loop[c1]
                    inductance_loop[c1],  inductance_loop[c2] = inductance_loop[c2],  inductance_loop[c1]

                    for c3 in range(len(sys_loop_map[first_loop])):
                        sys_loop_map[first_loop][c3],  sys_loop_map[second_loop][c3] = sys_loop_map[second_loop][c3],  sys_loop_map[first_loop][c3]

    return




def new_stiff_branch_adjustment(sys_loop_map, branch_info, br_events, stiff_info, state_vector, matrix_e, matrix_a, matrix_b, matrix_u, dt):
    """
    This function sets the newly turned stiff branches to have zero current along
    with the newly turned stiff loops. The purpose of this is to make sure that
    inductors have zero currents when they are incident to nodes that have
    branches that have turned stiff naturally. The inductor currents are set to
    zero when the change current direction in two successive simulation time
    iterations.
    """

    for c1 in range(len(branch_info)):
        if branch_info[c1][-1][0][1] and stiff_info[c1]=="no":
            if branch_info[c1][-1][5]>1:
                branch_info[c1][-1][2] = 0.0
#                branch_info[c1][-1][5] -= 1

    return




def new_stiff_loop_adjustment(sys_loop_map, branch_info, br_events, stiff_info, state_vector,  matrix_e, matrix_a, matrix_b, matrix_u, dt):
    """
    This function sets the currents of loops that have turned stiff naturally. The purpose
    is to be able to recalculate the branch currents to make the newly turned stiff
    branch currents to negligible values.
    """

    nonstiff_loops = []
    for c1 in range(len(sys_loop_map)):
        # Check if loop c1 has a stiff branch
        is_loop_stiff = "no"
        for c2 in range(len(branch_info)):
            if sys_loop_map[c1][c2]=="stiff_forward" or sys_loop_map[c1][c2]=="stiff_reverse":
                is_loop_stiff = "yes"
            if not sys_loop_map[c1][c2] == "no":
                if br_events[c2] == "yes" or br_events[c2] == "hard":
                    is_loop_stiff = "yes"

        if is_loop_stiff=="no":
            nonstiff_loops.append(c1)


    branches_turned_stiff = []
    for c1 in range(len(br_events)):
        if br_events[c1]=="yes":
            # THE STATEMENT BELOW IS A BUG.
#        if br_events[c1]=="hard" or br_events[c1]=="yes":
            if stiff_info[c1]=="yes":
                branches_turned_stiff.append(c1)


    loops_turned_stiff = []

    # This computation is to set the initial values of loop currents
    # for stiff loops. Since the stiff loops have been made upper triangular
    # the first occurrance of a stiff branch will mean the loop current is
    # equal to the stiff branch.
    for c1 in range(len(sys_loop_map)):
        # Go through all the stiff loops.
        if c1 not in nonstiff_loops:
            stiff_branch_found = "no"
            c2 = 0
            # Check if a branch is stiff.
            while stiff_branch_found=="no" and c2<len(sys_loop_map[c1]):
                if sys_loop_map[c1][c2]=="stiff_forward" or sys_loop_map[c1][c2]=="stiff_reverse":

                    if c2 in branches_turned_stiff:
                        if c1 not in loops_turned_stiff:
                            loops_turned_stiff.append(c1)

                    stiff_branch_found = "yes"

                c2 += 1


    # The way this is done is to save the currents of the loops that have
    # turned stiff by saving the currents of the branches in them that
    # have turned stiff. These saved currents are used to readjust the
    # other loops that are associated with these newly turned stiff loops.
    # This is to avoid the error in the currents in these newly turned stiff
    # loops by ajusting them in other nonstiff loops.
    previous_curr_stiff_loops = []
    for c1 in loops_turned_stiff:
        for c2 in range(len(sys_loop_map[c1])):
            if c2 in branches_turned_stiff:
                if not sys_loop_map[c1][c2]=="no":
                    if sys_loop_map[c1][c2]=="forward" or sys_loop_map[c1][c2]=="stiff_forward":
                        previous_curr_stiff_loops.append(branch_info[c2][-1][2])
                    if sys_loop_map[c1][c2]=="reverse" or sys_loop_map[c1][c2]=="stiff_reverse":
                        previous_curr_stiff_loops.append(-branch_info[c2][-1][2])
        state_vector[0].data[c1][0] = 0.0
        state_vector[1].data[c1][0] = 0.0


    # Re-initialize the matrices A, B, and E
    matrix_a.zeros(len(sys_loop_map),len(sys_loop_map))
    matrix_e.zeros(len(sys_loop_map),len(sys_loop_map))
    matrix_b.zeros(len(sys_loop_map),matrix_b.columns)

    # Recalculate the system matrices for the new loops.
    recalculate_sys_matrices(sys_loop_map, branch_info, matrix_a, matrix_e, matrix_b)

    # Calculating the currents in the newly turned stiff loops.
    for c1 in range(len(loops_turned_stiff)-1,  -1,  -1):
        stiff_equation_solver(matrix_e, matrix_a, matrix_b, state_vector, matrix_u, dt, loops_turned_stiff[c1])

    # Finding out which of the nonstiff loops are associated with
    # the newly turned stiff loops and offsetting their currents
    # by the currents of the branches that are being recalculated
    # as stiff branches.
    for c1 in loops_turned_stiff:
        previous_curr_stiff_loops[loops_turned_stiff.index(c1)] -= state_vector[1].data[c1][0]

        for c2 in nonstiff_loops:
            if not c1==c2:
                c3 = 0
                branch_found = "no"
                while c3<len(sys_loop_map[c2]) and branch_found=="no":
                    if not sys_loop_map[c2][c3]=="no":
                        if (sys_loop_map[c2][c3]=="forward" and sys_loop_map[c1][c3]=="forward") or \
                                    (sys_loop_map[c2][c3]=="reverse" and sys_loop_map[c1][c3]=="reverse"):
                            branch_found = "yes"
                            branch_dir = 1.0
                        if (sys_loop_map[c2][c3]=="forward" and sys_loop_map[c1][c3]=="reverse") or \
                                    (sys_loop_map[c2][c3]=="reverse" and sys_loop_map[c1][c3]=="forward"):
                            branch_found = "yes"
                            branch_dir = -1.0
                    c3 += 1

                if branch_found=="yes":
                    state_vector[0].data[c2][0] += branch_dir*previous_curr_stiff_loops[loops_turned_stiff.index(c1)]
                    state_vector[1].data[c2][0] = state_vector[0].data[c2][0]

    return


def loop_min_res_path(sys_loop_map, kcl_branch_map, stiff_info, branch_info, c1):
    number_of_branches = 0
    for c2 in range(len(sys_loop_map[c1])):
        if not sys_loop_map[c1][c2]=="no":
            number_of_branches += 1

    if number_of_branches>2:
        # For loops with more than two branches, iterate through every
        # branch and check from kcl_branch_map if it has branches
        # in parallel across it. If so, find out which branch has
        # minimum resistance. That branch replaces the current branch.
        for c2 in range(len(sys_loop_map[c1])):
            if not sys_loop_map[c1][c2]=="no":
                for c3 in range(len(kcl_branch_map)):
                    for c4 in range(c3+1, len(kcl_branch_map)):
                        if kcl_branch_map[c3][c4]:
                            if c2 in kcl_branch_map[c3][c4][0]:
                                if len(kcl_branch_map[c3][c4][0])>1:
                                    min_res_branch = c2
                                    for c5 in kcl_branch_map[c3][c4][0]:
                                        if not c5==c2:
                                            if stiff_info[c5]=="no":
                                                if branch_info[c5][-1][0][0]<branch_info[min_res_branch][-1][0][0]:
                                                    min_res_branch = c5

                                    if not min_res_branch==c2:
                                        old_branch_pos = kcl_branch_map[c3][c4][0].index(c2)
                                        new_branch_pos = kcl_branch_map[c3][c4][0].index(min_res_branch)
                                        # The new loop is created separately and then checked
                                        # if this loop already exists. If so, don't add it to
                                        # sys_loop_map as it will be a repeat loop.
                                        new_min_branch_loop = []
                                        for c6 in range(len(sys_loop_map[c1])):
                                            new_min_branch_loop.append(sys_loop_map[c1][c6])

                                        if sys_loop_map[c1][c2]=="forward":
                                            if kcl_branch_map[c3][c4][1][old_branch_pos]== \
                                                       kcl_branch_map[c3][c4][1][new_branch_pos]:
                                                new_min_branch_loop[c2] = "no"
                                                new_min_branch_loop[min_res_branch] = "forward"
                                            else:
                                                new_min_branch_loop[c2] = "no"
                                                new_min_branch_loop[min_res_branch] = "reverse"
                                        else:
                                            if kcl_branch_map[c3][c4][1][old_branch_pos]== \
                                                       kcl_branch_map[c3][c4][1][new_branch_pos]:
                                                new_min_branch_loop[c2] = "no"
                                                new_min_branch_loop[min_res_branch] = "reverse"
                                            else:
                                                new_min_branch_loop[c2] = "no"
                                                new_min_branch_loop[min_res_branch] = "forward"
#                                        this_new_loop_found = False
#                                        for c6 in range(len(sys_loop_map)):
#                                            if not c6==c1:
#                                                if sys_loop_map[c6]==new_min_branch_loop:
#                                                    this_new_loop_found = True

#                                        if not this_new_loop_found:
                                        for c6 in range(len(sys_loop_map[c1])):
                                            sys_loop_map[c1][c6] = new_min_branch_loop[c6]

    return


def approximate_nonstiff_loops(branch_info, stiff_info, sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, branch_tags_in_loops):
    """
    The purpose of this function is to arrange the non stiff
    loops in order of their L/R time constants. This is because
    when inductances in loops are ignored and the loops are
    treated as static loops, the minimum number of non-stiff
    loops should be approximated in such a manner. The concept is
    that each loop should choose the path of minimum resistance
    while ensuring all branches are included. Therefore, for
    loops with more than two branches, it is checked whether each
    branch has a parallel branch with lower resistance.
    """

    # Make a list of the nonstiff loops
    # Because stiff loops will essentially have a negligible
    # current.
    nonstiff_loops = listing_nonstiff_loops(sys_loop_map, branch_info)


#    for c1 in nonstiff_loops:
#        # Distinguish between loops with two branches and more.
#        # Loops with only two branches are branches that are connected
#        # in parallel and hence treated differently.
#        number_of_branches = 0
#        for c2 in range(len(sys_loop_map[c1])):
#            if not sys_loop_map[c1][c2]=="no":
#                number_of_branches += 1
#
#        if number_of_branches>2:
#            # For loops with more than two branches, iterate through every
#            # branch and check from kcl_branch_map if it has branches
#            # in parallel across it. If so, find out which branch has
#            # minimum resistance. That branch replaces the current branch.
#            for c2 in range(len(sys_loop_map[c1])):
#                if not sys_loop_map[c1][c2]=="no":
#                    for c3 in range(len(kcl_branch_map)):
#                        for c4 in range(c3+1, len(kcl_branch_map)):
#                            if kcl_branch_map[c3][c4]:
#                                if c2 in kcl_branch_map[c3][c4][0]:
#                                    if len(kcl_branch_map[c3][c4][0])>1:
#                                        min_res_branch = c2
#                                        for c5 in kcl_branch_map[c3][c4][0]:
#                                            if not c5==c2:
#                                                if stiff_info[c5]=="no":
#                                                    if branch_info[c5][-1][0][0]<branch_info[min_res_branch][-1][0][0]:
#                                                        min_res_branch = c5
#
#                                        if not min_res_branch==c2:
#                                            old_branch_pos = kcl_branch_map[c3][c4][0].index(c2)
#                                            new_branch_pos = kcl_branch_map[c3][c4][0].index(min_res_branch)
#                                            # The new loop is created separately and then checked
#                                            # if this loop already exists. If so, don't add it to
#                                            # sys_loop_map as it will be a repeat loop.
#                                            new_min_branch_loop = []
#                                            for c6 in range(len(sys_loop_map[c1])):
#                                                new_min_branch_loop.append(sys_loop_map[c1][c6])
#
#                                            if sys_loop_map[c1][c2]=="forward":
#                                                if kcl_branch_map[c3][c4][1][old_branch_pos]== \
#                                                           kcl_branch_map[c3][c4][1][new_branch_pos]:
#                                                    new_min_branch_loop[c2] = "no"
#                                                    new_min_branch_loop[min_res_branch] = "forward"
#                                                else:
#                                                    new_min_branch_loop[c2] = "no"
#                                                    new_min_branch_loop[min_res_branch] = "reverse"
#                                            else:
#                                                if kcl_branch_map[c3][c4][1][old_branch_pos]== \
#                                                           kcl_branch_map[c3][c4][1][new_branch_pos]:
#                                                    new_min_branch_loop[c2] = "no"
#                                                    new_min_branch_loop[min_res_branch] = "reverse"
#                                                else:
#                                                    new_min_branch_loop[c2] = "no"
#                                                    new_min_branch_loop[min_res_branch] = "forward"
#                                            this_new_loop_found = False
#                                            for c6 in range(len(sys_loop_map)):
#                                                if not c6==c1:
#                                                    if sys_loop_map[c6]==new_min_branch_loop:
#                                                        this_new_loop_found = True
#
#                                            if not this_new_loop_found:
#                                                for c6 in range(len(sys_loop_map[c1])):
#                                                    sys_loop_map[c1][c6] = new_min_branch_loop[c6]

    # Delete any loops that may have become duplicates because
    # of the above manipulation.
#    for c1 in range(len(nonstiff_loops)-1):
#        for c2 in range(len(nonstiff_loops)-1, c1, -1):
#            loops_same = "yes"
#            for c3 in range(len(sys_loop_map[nonstiff_loops[c1]])):
#                if not sys_loop_map[nonstiff_loops[c1]][c3]==sys_loop_map[nonstiff_loops[c2]][c3]:
#                    loops_same = "no"
#
#            if loops_same=="yes":
#                del sys_loop_map[nonstiff_loops[c2]]


    # Delete all loops with only two branches.
#    for c1 in range(len(nonstiff_loops)-1, -1, -1):
#        number_of_branches = 0
#        for c2 in range(len(sys_loop_map[c1])):
#            if not sys_loop_map[nonstiff_loops[c1]][c2]=="no":
#                number_of_branches += 1
#
#        if number_of_branches==2:
#            del sys_loop_map[nonstiff_loops[c1]]
#
#
#    # Now add loops with only two branches. Check for all branches
#    # connected in parallel from kcl_branch_map. As before, find
#    # out the branch with minimum resistance. All loops between
#    # these parallel branches will have the branch with minimum
#    # resistance a common branch. This again ensures the concept
#    # of loops choosing the path of least resistance.
#    for c1 in range(len(kcl_branch_map)):
#        for c2 in range(c1+1, len(kcl_branch_map)):
#            if kcl_branch_map[c1][c2]:
#                if len(kcl_branch_map[c1][c2][0])>1:
#                    min_res_branch_found = "no"
#                    for c3 in range(len(kcl_branch_map[c1][c2][0])):
#                        if stiff_info[kcl_branch_map[c1][c2][0][c3]]=="no":
#                            min_res_branch = kcl_branch_map[c1][c2][0][c3]
#                            min_res_branch_found = "yes"
#
#                    if min_res_branch_found=="yes":
#                        for c3 in range(1, len(kcl_branch_map[c1][c2][0])):
#                            if stiff_info[kcl_branch_map[c1][c2][0][c3]]=="no":
#                                if branch_info[min_res_branch][-1][0][0]>branch_info[kcl_branch_map[c1][c2][0][c3]][-1][0][0]:
#                                    min_res_branch = kcl_branch_map[c1][c2][0][c3]
#
#                        for c3 in range(len(kcl_branch_map[c1][c2][0])):
#                            if stiff_info[kcl_branch_map[c1][c2][0][c3]]=="no":
#                                if not kcl_branch_map[c1][c2][0][c3]==min_res_branch:
#                                    row_vector = []
#                                    for c4 in range(len(branch_info)):
#                                        row_vector.append("no")
#                                    min_res_branch_pos = kcl_branch_map[c1][c2][0].index(min_res_branch)
#                                    if kcl_branch_map[c1][c2][1][min_res_branch_pos]==1:
#                                        row_vector[min_res_branch] = "forward"
#                                    else:
#                                        row_vector[min_res_branch] = "reverse"
#
#                                    if kcl_branch_map[c1][c2][1][c3]==1:
#                                        row_vector[kcl_branch_map[c1][c2][0][c3]] = "reverse"
#                                    else:
#                                        row_vector[kcl_branch_map[c1][c2][0][c3]] = "forward"
#
#                                    sys_loop_map.append(row_vector)


    # Calculate the L/R ratio in each loop
    l_by_r_ratio = []
    for c1 in nonstiff_loops:
        total_resistance = 0.0
        total_inductance = 0.0
        for c2 in range(len(sys_loop_map[c1])):
            if not sys_loop_map[c1][c2]=="no":
                total_resistance += branch_info[c2][-1][0][0]
                total_inductance += branch_info[c2][-1][0][1]

        l_by_r_ratio.append(total_inductance/total_resistance)


    # Arrange the loops according to their L/R ratio
    for c1 in range(len(nonstiff_loops)-1):
        for c2 in range(c1+1, len(nonstiff_loops)):
            if l_by_r_ratio[c1]>l_by_r_ratio[c2]:
                l_by_r_ratio[c1], l_by_r_ratio[c2] = l_by_r_ratio[c2], l_by_r_ratio[c1]
                sys_loop_map[nonstiff_loops[c1]], sys_loop_map[nonstiff_loops[c2]] = \
                                sys_loop_map[nonstiff_loops[c2]], sys_loop_map[nonstiff_loops[c1]]


    return



def test_approximate_nonstiff_loops(branch_info, stiff_info, sys_loop_map, branches_in_kcl_nodes, kcl_branch_map):
    """
    The purpose of this function is to arrange the non stiff
    loops in order of their L/R time constants. This is because
    when inductances in loops are ignored and the loops are
    treated as static loops, the minimum number of non-stiff
    loops should be approximated in such a manner.
    This function is no longer used.
    """

    # Make a list of the nonstiff loops
    # Because stiff loops will essentially have a negligible
    # current.
    nonstiff_loops = listing_nonstiff_loops(sys_loop_map, branch_info)

    nonstiff_sys_loop_map = []
    for c1 in range(len(kcl_branch_map)):
        for c2 in range(c1+1, len(kcl_branch_map)):
            if len(kcl_branch_map[c1][c2])>1:
                for c3 in range(len(kcl_branch_map[c1][c2][0])-1):
                    branch_pos1 = kcl_branch_map[c1][c2][0][c3]
                    if stiff_info[branch_pos1]=="no":
                        branch_dir1 = kcl_branch_map[c1][c2][1][c3]
                        for c4 in range(c3+1, len(kcl_branch_map[c1][c2][0])):
                            branch_pos2 = kcl_branch_map[c1][c2][0][c4]
                            if stiff_info[branch_pos2]=="no":
                                branch_dir2 = kcl_branch_map[c1][c2][1][c4]
                                row_vector = []
                                for c5 in range(len(branch_info)):
                                    if c5==branch_pos1:
                                        if branch_dir1==1:
                                            row_vector.append("forward")
                                        else:
                                            row_vector.append("reverse")
                                    elif c5==branch_pos2:
                                        if branch_dir2==-1:
                                            row_vector.append("forward")
                                        else:
                                            row_vector.append("reverse")
                                    else:
                                        row_vector.append("no")

                                nonstiff_sys_loop_map.append(row_vector)

    for c1 in nonstiff_loops:
        row_vector = []
        for c2 in range(len(sys_loop_map[c1])):
            row_vector.append(sys_loop_map[c1][c2])
        nonstiff_sys_loop_map.append(row_vector)


    # Calculate the L/R ratio in each loop
    l_by_r_ratio = []
    for c1 in range(len(nonstiff_sys_loop_map)):
        total_resistance = 0.0
        total_inductance = 0.0
        for c2 in range(len(nonstiff_sys_loop_map[c1])):
            if not nonstiff_sys_loop_map[c1][c2]=="no":
                total_resistance += branch_info[c2][-1][0][0]
                total_inductance += branch_info[c2][-1][0][1]

        l_by_r_ratio.append(total_inductance/total_resistance)


    # Arrange the loops according to their L/R ratio
    for c1 in range(len(nonstiff_sys_loop_map)-1):
        for c2 in range(c1+1, len(nonstiff_sys_loop_map)):
            if l_by_r_ratio[c1]<l_by_r_ratio[c2]:
                l_by_r_ratio[c1], l_by_r_ratio[c2] = l_by_r_ratio[c2], l_by_r_ratio[c1]
                nonstiff_sys_loop_map[c1], nonstiff_sys_loop_map[c2] = nonstiff_sys_loop_map[c2], \
                                nonstiff_sys_loop_map[c1]


    # Try manipulating each loop with a loop of lower L/R
    # and checking if the resultant loop has higher L/R.
    # This means a resistive branch has been eliminated.
    for c1 in range(len(nonstiff_sys_loop_map)-1):
        for c2 in range(c1+1, len(nonstiff_sys_loop_map)):
            c3 = 0
            common_branch_found = "yes"
            while c3 < len(nonstiff_sys_loop_map[c1]) and common_branch_found=="no":
                if not nonstiff_sys_loop_map[c1][c3]=="no":
                    if not nonstiff_sys_loop_map[c2][c3]=="no":
                        common_branch_found = "yes"

                c3 += 1

            if common_branch_found=="yes":
                c3 -= 1
                if nonstiff_sys_loop_map[c1][c3]==nonstiff_sys_loop_map[c2][c3]:
                    manip_sense = "difference"
                else:
                    manip_sense = "addition"
                resultant_loop = nonstiff_loop_manipulations(nonstiff_sys_loop_map, branches_in_kcl_nodes, kcl_branch_map, \
                                            c1, c2, manip_sense)

                print("first loop")
                print(nonstiff_sys_loop_map[c1])
                print("second")
                print(nonstiff_sys_loop_map[c2])

                print("result")
                print(resultant_loop)

                if resultant_loop:
                    new_total_resistance = 0.0
                    new_total_inductance = 0.0
                    for c4 in range(len(branch_info)):
                        if not resultant_loop[c4]=="no":
                            new_total_resistance += branch_info[c4][-1][0][0]
                            new_total_inductance += branch_info[c4][-1][0][1]
                    print(new_total_inductance, new_total_resistance)
                    if new_total_resistance:
                        print(new_total_inductance/new_total_resistance)

                    if new_total_resistance:
                        if new_total_inductance/new_total_resistance > l_by_r_ratio[c2]:
                            for c4 in range(len(resultant_loop)):
                                nonstiff_sys_loop_map[c2][c4] = resultant_loop[c4]

                            l_by_r_ratio[c2] = new_total_inductance/new_total_resistance
                    else:
                        for c4 in range(len(resultant_loop)):
                            nonstiff_sys_loop_map[c2][c4] = resultant_loop[c4]

                        l_by_r_ratio[c2] = 0.0

                print()
                print()



    print()
    print()
    for c1 in range(len(nonstiff_sys_loop_map)):
        print(nonstiff_sys_loop_map[c1], l_by_r_ratio[c1])
    print()
    print()

    # Arrange the loops according to their L/R ratio
    for c1 in range(len(nonstiff_sys_loop_map)-1):
        for c2 in range(c1+1, len(nonstiff_sys_loop_map)):
            if l_by_r_ratio[c1]<l_by_r_ratio[c2]:
                l_by_r_ratio[c1], l_by_r_ratio[c2] = l_by_r_ratio[c2], l_by_r_ratio[c1]
                nonstiff_sys_loop_map[c1], nonstiff_sys_loop_map[c2] = nonstiff_sys_loop_map[c2], \
                                nonstiff_sys_loop_map[c1]


    for c1 in range(len(nonstiff_sys_loop_map)-1):
        for c2 in range(len(nonstiff_sys_loop_map)-1, c1, -1):
            loops_same = "yes"
            for c3 in range(len(nonstiff_sys_loop_map[c1])):
                if not nonstiff_sys_loop_map[c1][c3]==nonstiff_sys_loop_map[c2][c3]:
                    loops_same = "no"

            if loops_same=="yes":
                del nonstiff_sys_loop_map[c2]


    print("lbyr")
    print(l_by_r_ratio)
    for c1 in range(len(nonstiff_sys_loop_map)-1, len(nonstiff_loops)-1, -1):
        del nonstiff_sys_loop_map[c1]

    nonstiff_sys_loop_map.reverse()

    for c1 in range(len(nonstiff_loops)):
        sys_loop_map[nonstiff_loops[c1]] = []
        for c2 in range(len(branch_info)):
            sys_loop_map[nonstiff_loops[c1]].append(nonstiff_sys_loop_map[c1][c2])

    return



def compute_nonstiff_loops_generate(sys_loop_map, nonstiff_loops, branch_info):
    """
    This function generates the info for nonstiff loops.
    """

    # To begin with find out which of the branches
    # occur only in one loop. This will make
    # computations easier as those branch currents
    # will automatically become the initial values
    # for the loop currents in the next loop analysis.

    # A list of loops and branches with this info
    # It is a corresponding mapping.
    single_loops = []
    single_branches = []

    # Iterate through the nonstiff loops.
    for c1 in nonstiff_loops:
        # Iterate through the branches
        for c2 in range(len(branch_info)):
            # Check if the corresponding system map is a "yes"
            # Which means branch exixts.
            if sys_loop_map[c1][c2]=="forward" or sys_loop_map[c1][c2]=="reverse":
#            if sys_loop_map[c1][c2]=="forward" or sys_loop_map[c1][c2]=="reverse" and branch_info[c2][-1][0][1]==0.0:
#            if (sys_loop_map[c1][c2]=="forward" or sys_loop_map[c1][c2]=="reverse") and \
#                        (1.0 not in branch_info[c2][-1][1] and -1.0 not in branch_info[c2][-1][1]):

                # Look for the branch in all other nonstiff loops
                # A single occurance elsewhere will mean loop exists
                # So start with the default "no"
                does_branch_occur="no"
                for c3 in nonstiff_loops:
                    if not c1==c3:
                        if sys_loop_map[c3][c2]=="forward" or sys_loop_map[c3][c2]=="reverse":
                            does_branch_occur = "yes"

                if does_branch_occur=="no":
                    # Next check is both the loop and the branch have not been
                    # found before to prevent clashes.
                    if ((c1 not in single_loops) and (c2 not in single_branches)):
                        single_loops.append(c1)
                        single_branches.append(c2)


    single_directions = []
    # Now to set the loop currents equal to branch currents.
    # Take every loop and branch in the single_loop and single_branch lists
    # Since they are a one-to-one mapping, just equate the state vectors to
    # to the branch currents.
    for c1 in range(len(single_loops)):
        loop_row = single_loops[c1]
        if sys_loop_map[loop_row][single_branches[c1]]=="forward":
            single_directions.append(1.0)
        else:
            single_directions.append(-1.0)


    single_collection = [single_loops, single_branches, single_directions]


    # Compute the currents of the remaining loops
    # which do not have a single branch that exists only
    # in that loop.
    # This is done by solving a set of equations as each branch
    # current is the sum of all the loop currents.
    compute_loops_nonstiff = []
    compute_branches_nonstiff = []

    # Which are the loops whose currents need to be calculated.
    if len(single_loops)<len(nonstiff_loops):
        for c1 in nonstiff_loops:
            if c1 not in single_loops:
                if c1 not in compute_loops_nonstiff:
                    compute_loops_nonstiff.append(c1)



    # Which are the branch currents in these loops that could
    # be considered - the branch must not have a voltage.
    possible_compute_branches = []
    if compute_loops_nonstiff:
        for c1 in compute_loops_nonstiff:
            row_vector = []
            for c2 in range(len(sys_loop_map[c1])):
                if sys_loop_map[c1][c2]=="forward" or sys_loop_map[c1][c2]=="reverse":
#                if sys_loop_map[c1][c2]=="forward" or sys_loop_map[c1][c2]=="reverse" and branch_info[c2][-1][0][1]==0.0:
#                    if c2 not in single_branches and ((1.0 not in branch_info[c2][-1][1]) and (-1.0 not in branch_info[c2][-1][1])):
                    if c2 not in single_branches:
                        row_vector.append(c2)

            possible_compute_branches.append(row_vector)


        # Arrange the loops in increasing order of the length of
        # possible branches in the loops.
        for c1 in range(len(compute_loops_nonstiff)-1):
            for c2 in range(c1+1, len(compute_loops_nonstiff)):
                if len(possible_compute_branches[c2])<len(possible_compute_branches[c1]):
                    possible_compute_branches[c1], possible_compute_branches[c2] = \
                                possible_compute_branches[c2], possible_compute_branches[c1]
                    compute_loops_nonstiff[c1], compute_loops_nonstiff[c2] = \
                                compute_loops_nonstiff[c2], compute_loops_nonstiff[c1]


    # Add all the branches where the loops whose currents
    # have to be computed are present. This may result
    # in linearly dependent loops which will be
    # resolved when they equations are solved.
    if compute_loops_nonstiff:
        for c1 in range(len(possible_compute_branches)):
            for c2 in range(len(possible_compute_branches[c1])):
                if possible_compute_branches[c1][c2] not in compute_branches_nonstiff:
                    compute_branches_nonstiff.append(possible_compute_branches[c1][c2])


    # This is the AX=B system that is to be solved.
    loop_conn_mat = []
    loop_src_vec = []
    loop_src_branches = []
    for c1 in range(len(compute_branches_nonstiff)):
        loop_src_vec.append(0.0)
        loop_src_branches.append([])
        row_vector = []
        for c2 in range(len(compute_loops_nonstiff)):
            row_vector.append(0.0)
        loop_conn_mat.append(row_vector)



    # Sum of all the loop current equals to the branch current
    # The equation is written with respect to the branch corresponding
    # to every nonstiff loop that needs to be computed.
    # So Y is initialized at the branch current for each of the loops
    # to be computed, the loop currents that need to computed are
    # entered in the matrix A depending on whether the branch is
    # present in the loop. The loop currents already calculated are
    # sources in Y vector depending on whether the branch is present
    # in the loop.

    for c1 in range(len(compute_branches_nonstiff)):
        branch_pos = compute_branches_nonstiff[c1]
        loop_src_branches[c1].append([branch_pos, 1.0])
        #loop_src_vec[c1] = branch_info[branch_pos][-1][2]
        for c2 in nonstiff_loops:
            if c2 in compute_loops_nonstiff:
                if sys_loop_map[c2][branch_pos]=="forward":
                    loop_conn_mat[c1][compute_loops_nonstiff.index(c2)] = 1.0
                elif sys_loop_map[c2][branch_pos]=="reverse":
                    loop_conn_mat[c1][compute_loops_nonstiff.index(c2)] = -1.0
            else:
                if sys_loop_map[c2][branch_pos]=="forward":
                    loop_src_branches[c1].append([c2, -1.0])
                elif sys_loop_map[c2][branch_pos]=="reverse":
                    loop_src_branches[c1].append([c2, 1.0])


    loop_map_collection = [loop_conn_mat, loop_src_vec, loop_src_branches]

    return [single_collection, compute_loops_nonstiff, loop_map_collection]



def compute_stiff_loops_generate(sys_loop_map, nonstiff_loops, branch_info):
    """
    This function generates the info for stiff loops.
    """

    # To begin with find out which of the branches
    # occur only in one loop. This will make
    # computations easier as those branch currents
    # will automatically become the initial values
    # for the loop currents in the next loop analysis.

    # A list of loops and branches with this info
    # It is a corresponding mapping.
    single_loops = []
    single_branches = []

    # Iterate through the nonstiff loops.
    for c1 in range(len(sys_loop_map)):
        # Make sure loop is stiff
        if not c1 in nonstiff_loops:
            # Iterate through the branches
            for c2 in range(len(branch_info)):
                # Check if the corresponding system map is a "yes"
                # Which means branch exixts.
                if sys_loop_map[c1][c2]=="stiff_forward" or sys_loop_map[c1][c2]=="stiff_reverse":
#                if sys_loop_map[c1][c2]=="forward" or sys_loop_map[c1][c2]=="reverse" and branch_info[c2][-1][0][1]==0.0:
#                if (sys_loop_map[c1][c2]=="forward" or sys_loop_map[c1][c2]=="reverse") and \
#                            (1.0 not in branch_info[c2][-1][1] and -1.0 not in branch_info[c2][-1][1]):

                    # Look for the branch in all other nonstiff loops
                    # A single occurance elsewhere will mean loop exists
                    # So start with the default "no"
                    does_branch_occur="no"
                    for c3 in range(len(sys_loop_map)):
                        if not c3 in nonstiff_loops:
                            if not c1==c3:
                                if sys_loop_map[c3][c2]=="stiff_forward" or sys_loop_map[c3][c2]=="stiff_reverse":
                                    does_branch_occur = "yes"

                    if does_branch_occur=="no":
                        # Next check is both the loop and the branch have not been
                        # found before to prevent clashes.
                        if ((c1 not in single_loops) and (c2 not in single_branches)):
                            single_loops.append(c1)
                            single_branches.append(c2)


    single_directions = []
    # Now to set the loop currents equal to branch currents.
    # Take every loop and branch in the single_loop and single_branch lists
    # Since they are a one-to-one mapping, just equate the state vectors to
    # to the branch currents.
    for c1 in range(len(single_loops)):
        loop_row = single_loops[c1]
        if sys_loop_map[loop_row][single_branches[c1]]=="stiff_forward":
            single_directions.append(1.0)
        else:
            single_directions.append(-1.0)


    single_collection = [single_loops, single_branches, single_directions]


    # Compute the currents of the remaining loops
    # which do not have a single branch that exists only
    # in that loop.
    # This is done by solving a set of equations as each branch
    # current is the sum of all the loop currents.
    compute_loops_stiff = []
    compute_branches_stiff = []

    # Which are the loops whose currents need to be calculated.
    if len(single_loops) < (len(sys_loop_map) - len(nonstiff_loops)):
        for c1 in range(len(sys_loop_map)):
            if c1 not in nonstiff_loops:
                if c1 not in single_loops:
                    if c1 not in compute_loops_stiff:
                        compute_loops_stiff.append(c1)



    # Which are the branch currents in these loops that could
    # be considered - the branch must not have a voltage.
    possible_compute_branches = []
    if compute_loops_stiff:
        for c1 in compute_loops_stiff:
            row_vector = []
            for c2 in range(len(sys_loop_map[c1])):
                if sys_loop_map[c1][c2]=="stiff_forward" or sys_loop_map[c1][c2]=="stiff_reverse":
#                if sys_loop_map[c1][c2]=="forward" or sys_loop_map[c1][c2]=="reverse" and branch_info[c2][-1][0][1]==0.0:
#                    if c2 not in single_branches and ((1.0 not in branch_info[c2][-1][1]) and (-1.0 not in branch_info[c2][-1][1])):
                    if c2 not in single_branches:
                        row_vector.append(c2)

            possible_compute_branches.append(row_vector)


        # Arrange the loops in increasing order of the length of
        # possible branches in the loops.
        for c1 in range(len(compute_loops_stiff)-1):
            for c2 in range(c1+1,  len(compute_loops_stiff)):
                if len(possible_compute_branches[c2])<len(possible_compute_branches[c1]):
                    possible_compute_branches[c1], possible_compute_branches[c2] = \
                                possible_compute_branches[c2],  possible_compute_branches[c1]
                    compute_loops_stiff[c1],  compute_loops_stiff[c2] = \
                                compute_loops_stiff[c2],  compute_loops_stiff[c1]


    # Starting from the loops with the smallest number
    # of eligible branches, pick out the branches which
    # have not be selected by previous loops. The concept
    # is that the loops with smaller number of branches will
    # have lesser options of branches and so they should be
    # chosen first. The larger loops will take up the remaining
    # branches.

    if compute_loops_stiff:
        for c1 in range(len(possible_compute_branches)):
            for c2 in range(len(possible_compute_branches[c1])):
                if possible_compute_branches[c1][c2] not in compute_branches_stiff:
                    compute_branches_stiff.append(possible_compute_branches[c1][c2])


    # This is the AX=B system that is to be solved.
    loop_conn_mat = []
    loop_src_vec = []
    loop_src_branches = []
    for c1 in range(len(compute_branches_stiff)):
        loop_src_vec.append(0.0)
        loop_src_branches.append([])
        row_vector = []
        for c2 in range(len(compute_loops_stiff)):
            row_vector.append(0.0)
        loop_conn_mat.append(row_vector)



    # Sum of all the loop current equals to the branch current
    # The equation is written with respect to the branch corresponding
    # to every nonstiff loop that needs to be computed.
    # So Y is initialized at the branch current for each of the loops
    # to be computed, the loop currents that need to computed are
    # entered in the matrix A depending on whether the branch is
    # present in the loop. The loop currents already calculated are
    # sources in Y vector depending on whether the branch is present
    # in the loop.

    for c1 in range(len(compute_branches_stiff)):
        branch_pos = compute_branches_stiff[c1]
        loop_src_branches[c1].append([branch_pos, 1.0])
        #loop_src_vec[c1] = branch_info[branch_pos][-1][2]
        for c2 in range(len(sys_loop_map)):
            if c2 not in nonstiff_loops:
                if c2 in compute_loops_stiff:
                    if sys_loop_map[c2][branch_pos]=="stiff_forward":
                        loop_conn_mat[c1][compute_loops_stiff.index(c2)] = 1.0
                    elif sys_loop_map[c2][branch_pos]=="stiff_reverse":
                        loop_conn_mat[c1][compute_loops_stiff.index(c2)] = -1.0
                else:
                    if sys_loop_map[c2][branch_pos]=="stiff_forward":
                        loop_src_branches[c1].append([c2, -1.0])
                    elif sys_loop_map[c2][branch_pos]=="stiff_reverse":
                        loop_src_branches[c1].append([c2, 1.0])


    loop_map_collection = [loop_conn_mat, loop_src_vec, loop_src_branches]

    return [single_collection, compute_loops_stiff, loop_map_collection]




def compute_loop_currents_generate(branch_info, stiff_info, sys_loop_map, br_events, branches_in_kcl_nodes):
    """
    Calculates the loop currents after an event from branch currents.
    """

    # Make a list of the nonstiff loops
    # Because stiff loops will essentially have a negligible
    # current.
    nonstiff_loops = listing_nonstiff_loops(sys_loop_map, branch_info)

    single_nonstiff_collection, compute_loops_nonstiff, loop_map_collection_nonstiff = \
                compute_nonstiff_loops_generate(sys_loop_map, nonstiff_loops, branch_info)


    single_stiff_collection, compute_loops_stiff, loop_map_collection_stiff = \
                compute_stiff_loops_generate(sys_loop_map, nonstiff_loops, branch_info)

    return [single_nonstiff_collection, compute_loops_nonstiff, loop_map_collection_nonstiff,  \
            single_stiff_collection, compute_loops_stiff, loop_map_collection_stiff, nonstiff_loops]



def calc_nonstiff_loop_currents(single_collection, compute_loops_nonstiff, loop_map_collection, branch_params, state_vector):
    """
    This function calculates the currents in the nonstiff loops
    from the branch currents.
    """

    # A branch that occurs only in a single loop,
    # sets the current for that loop.
    single_loops = single_collection[0]
    single_branches = single_collection[1]
    single_directions = single_collection[2]

    for c1 in range(len(single_loops)):
        state_vector[0].data[single_loops[c1]][0] = branch_params[single_branches[c1]][-1][2]*single_directions[c1]
        state_vector[1].data[single_loops[c1]][0] = state_vector[0].data[single_loops[c1]][0]


    loop_conn_mat = loop_map_collection[0]
    loop_src_vec = loop_map_collection[1]
    loop_src_branches = loop_map_collection[2]


    for c1 in range(len(loop_src_branches)):
        loop_src_vec[c1] = branch_params[loop_src_branches[c1][0][0]][-1][2]
        for c2 in range(1, len(loop_src_branches[c1])):
            loop_src_vec[c1] += state_vector[1].data[loop_src_branches[c1][c2][0]][0]*loop_src_branches[c1][c2][1]


    # Solve the set of equations by reducing them to upper
    # diagonal form.

    if loop_conn_mat:
        for c1 in range(len(loop_conn_mat[0])):
            if not loop_conn_mat[c1][c1]:
                for c2 in range(c1+1, len(loop_conn_mat)):
                    if loop_conn_mat[c2][c1]:
                        loop_src_vec[c1], loop_src_vec[c2] = loop_src_vec[c2], loop_src_vec[c1]
                        for c3 in range(len(loop_conn_mat[c1])):
                            loop_conn_mat[c1][c3], loop_conn_mat[c2][c3] = \
                                        loop_conn_mat[c2][c3], loop_conn_mat[c1][c3]

            if loop_conn_mat[c1][c1]:
                diag_elem = loop_conn_mat[c1][c1]
                for c3 in range(len(loop_conn_mat[c1])):
                    loop_conn_mat[c1][c3] = loop_conn_mat[c1][c3]/diag_elem
                loop_src_vec[c1] = loop_src_vec[c1]/diag_elem

                for c2 in range(c1+1, len(loop_conn_mat)):
                    if loop_conn_mat[c2][c1]:
                        diag_elem = loop_conn_mat[c2][c1]
                        for c3 in range(len(loop_conn_mat[c1])):
                            loop_conn_mat[c2][c3] -= diag_elem*loop_conn_mat[c1][c3]
                        loop_src_vec[c2] -= diag_elem*loop_src_vec[c1]



    # Calculate backwards.
    if loop_conn_mat:
        for c1 in range(len(loop_conn_mat[0])-1, -1, -1):
            if loop_conn_mat[c1][c1]:
                state_vector[0].data[compute_loops_nonstiff[c1]][0] = \
                            loop_src_vec[c1]/loop_conn_mat[c1][c1]
                for c2 in range(c1+1, len(loop_conn_mat[0])):
                    state_vector[0].data[compute_loops_nonstiff[c1]][0] -= \
                                loop_conn_mat[c1][c2]*state_vector[0].data[compute_loops_nonstiff[c2]][0]
            else:
                state_vector[0].data[compute_loops_nonstiff[c1]][0] = 0.0

            state_vector[1].data[compute_loops_nonstiff[c1]][0] = \
                        state_vector[0].data[compute_loops_nonstiff[c1]][0]

    return



def calc_stiff_loop_currents(single_collection, compute_loops_stiff, loop_map_collection, branch_params, state_vector):
    """
    This function calculates the currents in the nonstiff loops
    from the branch currents.
    """

    # A branch that occurs only in a single loop,
    # sets the current for that loop.
    single_loops = single_collection[0]
    single_branches = single_collection[1]
    single_directions = single_collection[2]


    for c1 in range(len(single_loops)):
        state_vector[0].data[single_loops[c1]][0] = branch_params[single_branches[c1]][-1][2]*single_directions[c1]
        state_vector[1].data[single_loops[c1]][0] = state_vector[0].data[single_loops[c1]][0]


    loop_conn_mat = loop_map_collection[0]
    loop_src_vec = loop_map_collection[1]
    loop_src_branches = loop_map_collection[2]


    for c1 in range(len(loop_src_branches)):
        loop_src_vec[c1] = branch_params[loop_src_branches[c1][0][0]][-1][2]
        for c2 in range(1, len(loop_src_branches[c1])):
            loop_src_vec[c1] += state_vector[1].data[loop_src_branches[c1][c2][0]][0]*loop_src_branches[c1][c2][1]


    # Solve the set of equations by reducing them to upper
    # diagonal form.


    if loop_conn_mat:
        if (len(loop_conn_mat[0])<len(loop_conn_mat)):
            loop_conn_mat_size = len(loop_conn_mat[0])
        else:
            loop_conn_mat_size = len(loop_conn_mat)

#        for c1 in range(len(loop_conn_mat[0])):
        for c1 in range(loop_conn_mat_size):
            if not loop_conn_mat[c1][c1]:
                for c2 in range(c1+1, len(loop_conn_mat)):
                    if loop_conn_mat[c2][c1]:
                        loop_src_vec[c1], loop_src_vec[c2] = loop_src_vec[c2], loop_src_vec[c1]
                        for c3 in range(len(loop_conn_mat[c1])):
                            loop_conn_mat[c1][c3], loop_conn_mat[c2][c3] = \
                                        loop_conn_mat[c2][c3], loop_conn_mat[c1][c3]

            if loop_conn_mat[c1][c1]:
                diag_elem = loop_conn_mat[c1][c1]
                for c3 in range(len(loop_conn_mat[c1])):
                    loop_conn_mat[c1][c3] = loop_conn_mat[c1][c3]/diag_elem
                loop_src_vec[c1] = loop_src_vec[c1]/diag_elem

                for c2 in range(c1+1,  len(loop_conn_mat)):
                    if loop_conn_mat[c2][c1]:
                        diag_elem = loop_conn_mat[c2][c1]
                        for c3 in range(len(loop_conn_mat[c1])):
                            loop_conn_mat[c2][c3] -= diag_elem*loop_conn_mat[c1][c3]
                        loop_src_vec[c2] -= diag_elem*loop_src_vec[c1]


    # Calculate backwards.
    if loop_conn_mat:
#        for c1 in range(len(loop_conn_mat[0])-1, -1, -1):
        for c1 in range(loop_conn_mat_size-1, -1, -1):
            if loop_conn_mat[c1][c1]:
                state_vector[0].data[compute_loops_stiff[c1]][0] = \
                            loop_src_vec[c1]/loop_conn_mat[c1][c1]
                for c2 in range(c1+1,  len(loop_conn_mat[0])):
                    state_vector[0].data[compute_loops_stiff[c1]][0] -= \
                                loop_conn_mat[c1][c2]*state_vector[0].data[compute_loops_stiff[c2]][0]
            else:
                state_vector[0].data[compute_loops_stiff[c1]][0] = 0.0

            state_vector[1].data[compute_loops_stiff[c1]][0] = \
                        state_vector[0].data[compute_loops_stiff[c1]][0]

    return




def compute_loop_currents_calc(single_collection_nonstiff, compute_loops_nonstiff, loop_map_collection_nonstiff, \
                    single_collection_stiff, compute_loops_stiff, loop_map_collection_stiff, branch_params, state_vector):

    """
    A function to calculate the loop currents from the single branch
    vector and the loop current calculation equation matrices
    generated by the compute_loop_currents_generate function.
    """

    calc_nonstiff_loop_currents(single_collection_nonstiff, compute_loops_nonstiff, loop_map_collection_nonstiff, branch_params, state_vector)

    calc_stiff_loop_currents(single_collection_stiff, compute_loops_stiff, loop_map_collection_stiff, branch_params, state_vector)

    return




def compute_stiff_loop_currents(matrix_e, matrix_a, matrix_b, matrix_u,  dt, branch_info, stiff_info, sys_loop_map, state_vector,  br_events):
    """
    Calculates the stiff loop currents after an event from branch currents.
    """

    # Make a list of the nonstiff loops
    # Because stiff loops will essentially have a negligible
    # current.
    nonstiff_loops = listing_nonstiff_loops(sys_loop_map, branch_info)

    branches_turned_stiff = []
    for c1 in range(len(br_events)):
        if br_events[c1]=="yes":
            # THE STATEMENT BELOW IS A BUG.
#        if br_events[c1]=="hard" or br_events[c1]=="yes":
            if stiff_info[c1]=="yes":
                branches_turned_stiff.append(c1)


    loops_turned_stiff = []
    # This computation is to set the initial values of loop currents
    # for stiff loops. Since the stiff loops have been made upper triangular
    # the first occurrance of a stiff branch will mean the loop current is
    # equal to the stiff branch.
    for c1 in range(len(sys_loop_map)):
        # Go through all the stiff loops.
        if c1 not in nonstiff_loops:
            stiff_branch_found = "no"
            c2 = 0
            # Check if a branch is stiff.
            while stiff_branch_found=="no" and c2<len(sys_loop_map[c1]):
                if sys_loop_map[c1][c2]=="stiff_forward" or sys_loop_map[c1][c2]=="stiff_reverse":

                    if c2 in branches_turned_stiff:
                        if c1 not in loops_turned_stiff:
                            loops_turned_stiff.append(c1)

                    stiff_branch_found = "yes"

                c2 += 1


    # This computation is to set the initial values of loop currents
    # for stiff loops. Since the stiff loops have been made upper triangular
    # the first occurrance of a stiff branch will mean the loop current is
    # equal to the stiff branch.
    for c1 in range(len(sys_loop_map)):
        # Go through all the stiff loops.
        if (c1 not in nonstiff_loops) and (c1 not in loops_turned_stiff):
            stiff_branch_found = "no"
            c2 = 0
            # Check if a branch is stiff.
            while stiff_branch_found=="no" and c2<len(sys_loop_map[c1]):
                if sys_loop_map[c1][c2]=="stiff_forward" or sys_loop_map[c1][c2]=="stiff_reverse":

                    stiff_branch_found = "yes"
                    # At the first occurrance of stiff branch, initalize
                    # the loop current equal to the stiff branch current.
                    if sys_loop_map[c1][c2]=="stiff_forward":
                        state_vector[0].data[c1][0] = branch_info[c2][-1][2]
                        state_vector[1].data[c1][0] = branch_info[c2][-1][2]
                    elif sys_loop_map[c1][c2]=="stiff_reverse":
                        state_vector[0].data[c1][0] = -branch_info[c2][-1][2]
                        state_vector[1].data[c1][0] = -branch_info[c2][-1][2]

                c2 += 1

    return




def voltmeter_determine(branch_params, branches_in_kcl_nodes, kcl_branch_map, sys_mat_u, voltmeter_branches, voltmeter_voltages):

    """
    The concept of modeling the voltmeter as a large
    resistance that does not disturb the current in the main
    circuit ignores the fact that the voltmeter has to measure the
    voltage between two nodes and not the voltage in a loop.
    So, a basic nodal analysis is performed on the nodes where
    each voltmeter is connected. For branches parallel to the voltmeter,
    an inductive non-stiff branch is considered as a current source
    while a resistive branch is modeled as an admittance. All other branches
    incident at one of the voltmeter nodes are current sources.
    With this the voltage of one of the nodes is calculated with respect to
    the other multiplying the equivalent current at the node and the equivalent
    resistance between the nodes.
    """

    for c1 in voltmeter_branches:
        c2 = 0
        voltmeter_found = "no"
        while c2<len(branches_in_kcl_nodes) and voltmeter_found=="no":
            if c1 in branches_in_kcl_nodes[c2]:
                voltmeter_found = "yes"
            else:
                c2 += 1

        eq_curr = 0.0
        for c3 in range(len(kcl_branch_map[c2])):
            if kcl_branch_map[c2][c3]:
                if c1 in kcl_branch_map[c2][c3][0]:
                    eq_res = 0.0
                    for c4 in range(len(kcl_branch_map[c2][c3][0])):
                        branch_pos = kcl_branch_map[c2][c3][0][c4]
                        branch_dir = kcl_branch_map[c2][c3][1][c4]
                        if branch_params[c1][-1][0][1] and stiff_ratio[c1]=="no":
                            eq_curr -= branch_dir*branch_params[branch_pos][-1][2]

                        elif branch_params[c1][-1][0][0]:
                            eq_res += 1/branch_params[branch_pos][-1][0][0]
                            for c5 in range(len(branch_params[branch_pos][-1][1])):
                                eq_curr -= branch_dir*branch_params[branch_pos][-1][1][c5]*sys_mat_u.data[c5][0]/branch_params[branch_pos][-1][0][0]

                else:
                    for c4 in range(len(kcl_branch_map[c2][c3][0])):
                        if kcl_branch_map[c2][c3][0][c4] not in voltmeter_branches:
                            eq_curr -= kcl_branch_map[c2][c3][1][c4]*branch_params[kcl_branch_map[c2][c3][0][c4]][-1][2]


                for c4 in range(len(kcl_branch_map[c2][c3][0])):
                    if kcl_branch_map[c2][c3][0][c4]==c1:
                        voltmeter_direction = kcl_branch_map[c2][c3][1][c4]


        voltmeter_voltages[voltmeter_branches.index(c1)] = voltmeter_direction*eq_curr/eq_res
        branch_params[c1][-1][2] = voltmeter_voltages[voltmeter_branches.index(c1)]/branch_params[c1][-1][0][0]

    return



def nonlinearvolt_determine(branch_params, branches_in_kcl_nodes, kcl_branch_map, sys_mat_u, nonlinear_branches, nonlinear_voltages):

    """
    The concept of modeling the voltmeter as a large
    resistance that does not disturb the current in the main
    circuit ignores the fact that the voltmeter has to measure the
    voltage between two nodes and not the voltage in a loop.
    So, a basic nodal analysis is performed on the nodes where
    each voltmeter is connected. For branches parallel to the voltmeter,
    an inductive non-stiff branch is considered as a current source
    while a resistive branch is modeled as an admittance. All other branches
    incident at one of the voltmeter nodes are current sources.
    With this the voltage of one of the nodes is calculated with respect to
    the other multiplying the equivalent current at the node and the equivalent
    resistance between the nodes.
    """

    for c1 in voltmeter_branches:
        c2 = 0
        voltmeter_found = "no"
        while c2<len(branches_in_kcl_nodes) and voltmeter_found=="no":
            if c1 in branches_in_kcl_nodes[c2]:
                voltmeter_found = "yes"
            else:
                c2 += 1

        eq_curr = 0.0
        for c3 in range(len(kcl_branch_map[c2])):
            if kcl_branch_map[c2][c3]:
                if c1 in kcl_branch_map[c2][c3][0]:
                    eq_res = 0.0
                    for c4 in range(len(kcl_branch_map[c2][c3][0])):
                        branch_pos = kcl_branch_map[c2][c3][0][c4]
                        branch_dir = kcl_branch_map[c2][c3][1][c4]
                        if branch_params[c1][-1][0][1] and stiff_ratio[c1]=="no":
                            eq_curr -= branch_dir*branch_params[branch_pos][-1][2]

                        elif branch_params[c1][-1][0][0]:
                            eq_res += 1/branch_params[branch_pos][-1][0][0]
                            for c5 in range(len(branch_params[branch_pos][-1][1])):
                                eq_curr -= branch_dir*branch_params[branch_pos][-1][1][c5]*sys_mat_u.data[c5][0]/branch_params[branch_pos][-1][0][0]

                else:
                    for c4 in range(len(kcl_branch_map[c2][c3][0])):
                        if kcl_branch_map[c2][c3][0][c4] not in voltmeter_branches:
                            eq_curr -= kcl_branch_map[c2][c3][1][c4]*branch_params[kcl_branch_map[c2][c3][0][c4]][-1][2]


                for c4 in range(len(kcl_branch_map[c2][c3][0])):
                    if kcl_branch_map[c2][c3][0][c4]==c1:
                        voltmeter_direction = kcl_branch_map[c2][c3][1][c4]


        voltmeter_voltages[voltmeter_branches.index(c1)] = voltmeter_direction*eq_curr/eq_res
        branch_params[c1][-1][2] = voltmeter_voltages[voltmeter_branches.index(c1)]/branch_params[c1][-1][0][0]

    return




def capacitor_rearrange(sys_loop_map, branches_in_kcl_nodes, nonstiff_loops, capacitor_list):
    """
    This function manipulates one loop with respect to another loop in order
    to increase the number of capacitors in each loop.
    This operation is similar to the row operations on matrices except
    that the operation is performed on the KVL loops.
    """

    capacitors_in_loops = []
    for c1 in nonstiff_loops:
        number_of_capacitors = 0
        for c2 in range(len(sys_loop_map[c1])):
            if not sys_loop_map[c1][c2]=="no":
                if c2 in capacitor_list:
                    number_of_capacitors += 1

        capacitors_in_loops.append(number_of_capacitors)


    for c1 in range(len(nonstiff_loops)-1):
        for c2 in range(c1+1, len(nonstiff_loops)):
            row1 = nonstiff_loops[c1]
            row2 = nonstiff_loops[c2]

            common_branch_found = "no"
            for c3 in range(len(sys_loop_map[row1])):
                if not sys_loop_map[row1][c3]=="no":
                    if not sys_loop_map[row2][c3]=="no":
                        common_branch_found = "yes"
                        if sys_loop_map[row1][c3]==sys_loop_map[row2][c3]:
                            manip_sense = "difference"
                        else:
                            manip_sense = "addition"



            if common_branch_found=="yes":

                resultant_loop = []
                for c3 in range(len(sys_loop_map[0])):
                    resultant_loop.append(sys_loop_map[row1][c3])


                if manip_sense == "difference":
                    for c3 in range(len(sys_loop_map[0])):
                        if sys_loop_map[row1][c3]=="forward" and sys_loop_map[row2][c3]=="forward":
                            resultant_loop[c3] = "no"

                        elif sys_loop_map[row1][c3]=="reverse" and sys_loop_map[row2][c3]=="reverse":
                            resultant_loop[c3] = "no"

                        elif sys_loop_map[row1][c3]=="no" and sys_loop_map[row2][c3]=="reverse":
                            resultant_loop[c3] = "forward"

                        elif sys_loop_map[row1][c3]=="no" and sys_loop_map[row2][c3]=="forward":
                            resultant_loop[c3] = "reverse"

                        elif sys_loop_map[row1][c3]=="stiff_forward" and sys_loop_map[row2][c3]=="stiff_forward":
                            resultant_loop[c3] = "no"

                        elif sys_loop_map[row1][c3]=="stiff_reverse" and sys_loop_map[row2][c3]=="stiff_reverse":
                            resultant_loop[c3] = "no"

                        elif sys_loop_map[row1][c3]=="no" and sys_loop_map[row2][c3]=="stiff_reverse":
                            resultant_loop[c3] = "stiff_forward"

                        elif sys_loop_map[row1][c3]=="no" and sys_loop_map[row2][c3]=="stiff_forward":
                            resultant_loop[c3] = "stiff_reverse"

                else:
                    for c3 in range(len(sys_loop_map[0])):
                        if sys_loop_map[row1][c3]=="forward" and sys_loop_map[row2][c3]=="reverse":
                            resultant_loop[c3] = "no"

                        elif sys_loop_map[row1][c3]=="reverse" and sys_loop_map[row2][c3]=="forward":
                            resultant_loop[c3] = "no"

                        elif sys_loop_map[row1][c3]=="no" and sys_loop_map[row2][c3]=="reverse":
                            resultant_loop[c3] = "reverse"

                        elif sys_loop_map[row1][c3]=="no" and sys_loop_map[row2][c3]=="forward":
                            resultant_loop[c3] = "forward"

                        elif sys_loop_map[row1][c3]=="stiff_forward" and sys_loop_map[row2][c3]=="stiff_reverse":
                            resultant_loop[c3] = "no"

                        elif sys_loop_map[row1][c3]=="stiff_reverse" and sys_loop_map[row2][c3]=="stiff_forward":
                            resultant_loop[c3] = "no"

                        elif sys_loop_map[row1][c3]=="no" and sys_loop_map[row2][c3]=="stiff_reverse":
                            resultant_loop[c3] = "stiff_reverse"

                        elif sys_loop_map[row1][c3]=="no" and sys_loop_map[row2][c3]=="stiff_forward":
                            resultant_loop[c3] = "stiff_forward"



                # This part of the function is to check if the loop is a genuine loop.
                # A loop is genuine only if every node in the loop occurs exactly twice,
                # the loop closes with the end node being the same as the beginning node
                # while progressing through branches along the loop.
                # Finally there should be no additional branches besides those inside
                # the closed loop.
                all_branches_in_loop = []
                branches_in_loop = []
                nodes_in_loop = []
                node_pairs_in_loop = []
                for c3 in range(len(resultant_loop)):
                    if not resultant_loop[c3]=="no":
                        branch_nodes = []
                        for c4 in range(len(branches_in_kcl_nodes)):
                            if c3 in branches_in_kcl_nodes[c4]:
                                if c4 not in branch_nodes:
                                    branch_nodes.append(c4)

                        # For every branch that is found, the branch is
                        # added to all branches found. And the KCL nodes
                        # that are the end nodes of the branch are added
                        # as a node pair.
                        node_pairs_in_loop.append(branch_nodes)
                        all_branches_in_loop.append(c3)


                if all_branches_in_loop:
                    # Starting with the first branch found in the
                    # loop, trace the loop :
                    # This means - origin node is the first node
                    # of the first branch. The "next" node is the
                    # second node of the branch.
                    origin_node = node_pairs_in_loop[0][0]
                    branches_in_loop.append(all_branches_in_loop[0])
                    next_node = node_pairs_in_loop[0][1]
                    nodes_in_loop.append(next_node)
                    loop_completed = "no"

                    # First check is if all nodes in the loop
                    # occur as node pairs. If that fails, it is
                    # not a loop and the entire check can exit.
                    for c3 in range(len(node_pairs_in_loop)):
                        for c4 in range(len(node_pairs_in_loop[c3])):
                            node_occur = 1
                            for c5 in range(len(node_pairs_in_loop)):
                                if not c5==c3:
                                    if node_pairs_in_loop[c5][0]==node_pairs_in_loop[c3][c4]:
                                        node_occur += 1
                                    if node_pairs_in_loop[c5][1]==node_pairs_in_loop[c3][c4]:
                                        node_occur += 1

                        if not node_occur==2:
                            loop_completed = "yes"


                    # Next step is look through the rest of the loop starting with
                    # with the next branch. If the branch has not been encountered,
                    # examine it. Check if the "next" node is one of the nodes in
                    # this branch. If so, this branch is the continuation of the
                    # loop. The "current" node is the other node in the node pair.
                    # Check if this node is the origin node. If so, the loop has
                    # completed. If not, check if the node has been found. If so,
                    # the loop has been completed (this loop is not valid) because
                    # it means this is a loop within a loop. Make the "next" node
                    # this "current" node so that the search can continue. If the
                    # branch counter has reached the end, reset it.
                    c3 = 1
                    while loop_completed=="no":
                        if all_branches_in_loop[c3] not in branches_in_loop:
                            if next_node in node_pairs_in_loop[c3]:
                                if next_node==node_pairs_in_loop[c3][0]:
                                    current_node = node_pairs_in_loop[c3][1]
                                else:
                                    current_node = node_pairs_in_loop[c3][0]

                                if current_node==origin_node:
                                    loop_completed = "yes"
                                else:
                                    if current_node in nodes_in_loop:
                                        loop_completed = "yes"
                                    else:
                                        nodes_in_loop.append(current_node)
                                    next_node = current_node

                                branches_in_loop.append(all_branches_in_loop[c3])

                        if c3 < len(all_branches_in_loop)-1:
                            c3 += 1
                        else:
                            c3 = 1


                    # If the loop has completed, check if any branches in the
                    # resultant loop is not in the branches that have been
                    # traced.
                    is_valid_loop = "yes"
                    if loop_completed=="yes":
                        for c3 in range(len(resultant_loop)):
                            if not resultant_loop[c3]=="no":
                                if c3 not in branches_in_loop:
                                    is_valid_loop = "no"

                else:
                    is_valid_loop = "yes"


                # Only if the loop is valid will the loop manipulation be
                # added to the system loop map.
                if is_valid_loop=="yes" and all_branches_in_loop:

                    new_capacitor_count = 0
                    for c3 in range(len(resultant_loop)):
                        if not resultant_loop[c3]=="no":
                            if c3 in capacitor_list:
                                new_capacitor_count += 1

                    if new_capacitor_count>capacitors_in_loops[c1]:

                        capacitors_in_loops[c1] = new_capacitor_count

                        for c3 in range(len(resultant_loop)):
                            sys_loop_map[row1][c3] = resultant_loop[c3]


    return




def mat_ode_rearrange(matrix_e, matrix_a, matrix_b, input_vector, state_vector, ode_vectors, sys_loop_map, nonstiff_loops, branches_in_kcl_nodes):
    """
    Function to arrange the equations of the ODE.
    """

    calc_dibydt = Mtrx.Matrix(matrix_e.rows)
    for c1 in range(matrix_e.rows):
        for c2 in range(matrix_b.columns):
            calc_dibydt.data[c1][0] += matrix_b.data[c1][c2]*input_vector.data[c2][0]

        for c2 in range(matrix_a.columns):
            calc_dibydt.data[c1][0] -= matrix_a.data[c1][c2]*state_vector[0].data[c2][0]

        for c2 in range(matrix_e.columns):
            if not c1==c2:
                calc_dibydt.data[c1][0] -= matrix_e.data[c1][c2]*ode_vectors[4].data[c2][0]

        if matrix_e.data[c1][c1]:
            calc_dibydt.data[c1][0] = calc_dibydt.data[c1][0]/matrix_e.data[c1][c1]
        else:
            calc_dibydt.data[c1][0] = 0.0


    for c1 in range(matrix_e.rows):
        if calc_dibydt.data[c1][0]:
            for c2 in range(matrix_e.rows):
                if not c1==c2:
                    loop_dir = 0
                    if matrix_e.data[c1][c2]:
                        if matrix_e.data[c1][c2]>0.0:
                            loop_dir = +1
                        else:
                            loop_dir = -1

                    if loop_dir:
                        a_row_matrix = Mtrx.Matrix(matrix_a.columns)
                        e_row_matrix = Mtrx.Matrix(matrix_e.columns)
                        b_row_matrix = Mtrx.Matrix(matrix_b.columns)

                        for c3 in range(matrix_a.columns):
                            a_row_matrix.data[c3][0] = matrix_a.data[c1][c3] - loop_dir*matrix_a.data[c2][c3]
                            e_row_matrix.data[c3][0] = matrix_e.data[c1][c3] - loop_dir*matrix_e.data[c2][c3]
                        for c3 in range(matrix_b.columns):
                            b_row_matrix.data[c3][0] = matrix_b.data[c1][c3] - loop_dir*matrix_b.data[c2][c3]

                        new_dibydt = 0.0
                        for c3 in range(matrix_b.columns):
                            new_dibydt += b_row_matrix.data[c3][0]*input_vector.data[c3][0]

                        for c3 in range(matrix_a.columns):
                            new_dibydt -= a_row_matrix.data[c3][0]*state_vector[1].data[c3][0]

                        for c3 in range(matrix_e.columns):
                            if not c3==c1:
                                new_dibydt -= e_row_matrix.data[c3][0]*ode_vectors[4].data[c3][0]

                        if e_row_matrix.data[c1][0]:
                            new_dibydt = new_dibydt/e_row_matrix.data[c1][0]


                        if (abs(new_dibydt)<abs(calc_dibydt.data[c1][0])):

                            if loop_dir > 0:
                                loop_manipulations(sys_loop_map, branches_in_kcl_nodes, nonstiff_loops[c1], nonstiff_loops[c2], "difference")

                            if loop_dir < 0:
                                loop_manipulations(sys_loop_map, branches_in_kcl_nodes, nonstiff_loops[c1], nonstiff_loops[c2], "addition")


                            for c3 in range(matrix_a.columns):
                                matrix_a.data[c1][c3] = a_row_matrix.data[c3][0]
                                matrix_e.data[c1][c3] = e_row_matrix.data[c3][0]

                            for c3 in range(matrix_b.columns):
                                matrix_b.data[c1][c3] = b_row_matrix.data[c3][0]

                            calc_dibydt.data[c1][0] = new_dibydt

    return




def mat_ode_reduce(matrix_e, matrix_a, matrix_b):
    """
    Function to modify the matrices for E d/dt(x)=Ax+bu.
    Upper triangularization is used to calculate the value of d/dt(x).
    """

    # Check if it is a genuine set of equations
    if not ((matrix_e.rows==matrix_a.rows) and (matrix_a.rows==matrix_b.rows)):
        print("Matrices do not have the same number of rows.")
    else:
        for c1 in range(matrix_e.rows):
            #Make the diagonal element = 1.
            div_row = matrix_e.data[c1][c1]
            #Even after all possible row manipulations,
            #a diagonal element is zero, it means rank<size of matrix.
            if not div_row:
                #print "Check the circuit. Some variables have no dynamics."
                pass
            else:
                for c2 in range(matrix_e.columns):
                    matrix_e.data[c1][c2] = matrix_e.data[c1][c2]/div_row
                for c2 in range(matrix_a.columns):
                    matrix_a.data[c1][c2] = matrix_a.data[c1][c2]/div_row
                for c2 in range(matrix_b.columns):
                    matrix_b.data[c1][c2] = matrix_b.data[c1][c2]/div_row
                #Row operations to remove row entries below the diagonal unity element.
                for c2 in range(c1+1, matrix_e.rows):
                    mul_column = matrix_e.data[c2][c1]/matrix_e.data[c1][c1]

                    for c3 in range(matrix_e.columns):
                        matrix_e.data[c2][c3] = matrix_e.data[c2][c3]-matrix_e.data[c1][c3]*mul_column
                    for c3 in range(matrix_a.columns):
                        matrix_a.data[c2][c3] = matrix_a.data[c2][c3]-matrix_a.data[c1][c3]*mul_column
                    for c3 in range(matrix_b.columns):
                        matrix_b.data[c2][c3] = matrix_b.data[c2][c3]-matrix_b.data[c1][c3]*mul_column

    return



def mat_ode(matrix_e, matrix_a, matrix_b, state_vector, input_vector, dt, ode_vectors, list_of_nodes):
    """
    Solves the ODE using Runge Kutta 4th order method.
    """

    def runge_function4(x_plus_dxdt, ddt_mat, dbydt_order, ode_row):
        """
        Defines the function dx/dt=f(x) for 4th order
        Runge Kutta solver.
        """

        #Calculate d/dt vector in reverse.
        #for c1 in range(matrix_e.rows-1, -1, -1):
        if matrix_e.data[ode_row][ode_row]:
            try:
                if input_vector.rows:
                    pass
            except:
                if not (matrix_b.columns==1):
                    print("Input signal has to be a real number and not a vector.")
                else:
                    ddt_mat[dbydt_order-1].data[ode_row][0] = matrix_b.data[ode_row][0]*input_vector
            else:
                if not (matrix_b.columns==input_vector.rows):
                    print("Dimension of input vector incorrect.")
                else:
                    ddt_mat[dbydt_order-1].data[ode_row][0] = 0.0 # Added on Dec. 29, 2012.
                    for c2 in range(matrix_b.columns):
                        ddt_mat[dbydt_order-1].data[ode_row][0] += matrix_b.data[ode_row][c2]*input_vector.data[c2][0]

            if (dbydt_order==2):
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*0.5*ddt_mat[dbydt_order-2].data[c3][0]
            if (dbydt_order==3):
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*0.5*ddt_mat[dbydt_order-2].data[c3][0]
            if (dbydt_order==4):
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-2].data[c3][0]

            for c3 in range(matrix_a.columns):
                ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*x_plus_dxdt.data[c3][0]

            ddt_mat[dbydt_order-1].data[ode_row][0] = ddt_mat[dbydt_order-1].data[ode_row][0]*dt
            for c3 in range(ode_row+1, matrix_e.columns):
#           for c3 in range(matrix_e.columns):
                if not ode_row==c3:
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_e.data[ode_row][c3]*ode_vectors[4].data[c3][0]

            ddt_mat[dbydt_order-1].data[ode_row][0] = ddt_mat[dbydt_order-1].data[ode_row][0]
#           ddt_mat[dbydt_order-1].data[ode_row][0] = ddt_mat[dbydt_order-1].data[ode_row][0]/matrix_e.data[ode_row][ode_row]
        else:
            if not (matrix_a.data[ode_row][ode_row]):
                #The variable has no dynamics and can't even be calculated statically!
                # May be due to a redundant loop.
                ddt_mat[dbydt_order-1].data[ode_row][0] = 0.0
                state_vector[0].data[ode_row][0] = 0.0
                state_vector[1].data[ode_row][0] = 0.0
            else:

                ddt_mat[dbydt_order-1].data[ode_row][0] = 0.0
                state_vector[0].data[ode_row][0] = 0.0
                state_vector[1].data[ode_row][0] = 0.0
                try:
                    if input_vector.rows:
                        pass
                except:
                    if not (matrix_b.columns==1):
                        print("Input signal has to be a real number and not a vector.")
                    else:
                        state_vector[0].data[ode_row][0] += matrix_b.data[ode_row][0]*input_vector
                        #state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]
                else:
                    if not (matrix_b.columns==input_vector.rows):
                        print("Dimension of input vector incorrect.")
                    else:
                        for c2 in range(matrix_b.columns):
                            state_vector[0].data[ode_row][0] += matrix_b.data[ode_row][c2]*input_vector.data[c2][0]
                            #state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]

                for c2 in range(matrix_a.columns):
                    if not (ode_row==c2):
                        state_vector[0].data[ode_row][0] -= matrix_a.data[ode_row][c2]*state_vector[1].data[c2][0]
                        #state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]


                for c2 in range(matrix_e.columns):
                    state_vector[0].data[ode_row][0] -= matrix_e.data[ode_row][c2]*ode_vectors[4].data[c2][0]/dt
                    #state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]


                state_vector[0].data[ode_row][0] = state_vector[0].data[ode_row][0]/matrix_a.data[ode_row][ode_row]
                state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]
        return



    def runge_function5(x_plus_dxdt, ddt_mat, dbydt_order, ode_row):
        """
        Defines the function dx/dt=f(x) for higher order
        ODE solver
        """

        #Calculate d/dt vector in reverse.
        #for c1 in range(matrix_e.rows-1, -1, -1):
        if matrix_e.data[ode_row][ode_row]:
            try:
                if input_vector.rows:
                    pass
            except:
                if not (matrix_b.columns==1):
                    print("Input signal has to be a real number and not a vector.")
                else:
                    ddt_mat[dbydt_order-1].data[ode_row][0] = matrix_b.data[ode_row][0]*input_vector
            else:
                if not (matrix_b.columns==input_vector.rows):
                    print("Dimension of input vector incorrect.")
                else:
                    # Added on Dec. 29, 2012.
                    ddt_mat[dbydt_order-1].data[ode_row][0] = 0.0
                    for c2 in range(matrix_b.columns):
                        ddt_mat[dbydt_order-1].data[ode_row][0] += matrix_b.data[ode_row][c2]*input_vector.data[c2][0]

            if (dbydt_order==2):
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-2].data[c3][0]
            if (dbydt_order==3):
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*0.5*ddt_mat[dbydt_order-3].data[c3][0]
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*0.5*ddt_mat[dbydt_order-2].data[c3][0]

            if (dbydt_order==4):
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-4].data[c3][0]*(14.0/64.0)
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-3].data[c3][0]*(5.0/64.0)
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-2].data[c3][0]*(-3.0/64.0)

            if (dbydt_order==5):
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-5].data[c3][0]*(-12.0/96.0)
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-4].data[c3][0]*(-12.0/96.0)
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-3].data[c3][0]*(8.0/96.0)
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-2].data[c3][0]*(64.0/96.0)

            if (dbydt_order==6):
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-5].data[c3][0]*(-9.0/64.0)
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-4].data[c3][0]*(5.0/64.0)
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-3].data[c3][0]*(16.0/64.0)
                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*ddt_mat[dbydt_order-2].data[c3][0]*(36.0/64.0)


            for c3 in range(matrix_a.columns):
                ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_a.data[ode_row][c3]*x_plus_dxdt.data[c3][0]

            ddt_mat[dbydt_order-1].data[ode_row][0] = ddt_mat[dbydt_order-1].data[ode_row][0]*dt
            for c3 in range(matrix_e.columns):
                if not ode_row==c3:
                    ddt_mat[dbydt_order-1].data[ode_row][0] -= matrix_e.data[ode_row][c3]*ode_vectors[4].data[c3][0]

            ddt_mat[dbydt_order-1].data[ode_row][0] = ddt_mat[dbydt_order-1].data[ode_row][0]
        else:
            if not (matrix_a.data[ode_row][ode_row]):
                #The variable has no dynamics and can't even be calculated statically!
                # May be due to a redundant loop.
                state_vector[0].data[ode_row][0] = 0.0
                state_vector[1].data[ode_row][0] = 0.0
            else:

                ddt_mat[dbydt_order-1].data[ode_row][0] = 0.0
                state_vector[0].data[ode_row][0] = 0.0
                state_vector[1].data[ode_row][0] = 0.0
                try:
                    if input_vector.rows:
                        pass
                except:
                    if not (matrix_b.columns==1):
                        print("Input signal has to be a real number and not a vector.")
                    else:
                        state_vector[0].data[ode_row][0] += matrix_b.data[ode_row][0]*input_vector
                        state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]
                else:
                    if not (matrix_b.columns==input_vector.rows):
                        print("Dimension of input vector incorrect.")
                    else:
                        for c2 in range(matrix_b.columns):
                            state_vector[0].data[ode_row][0] += matrix_b.data[ode_row][c2]*input_vector.data[c2][0]
                            state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]

                for c2 in range(matrix_a.columns):
                    if not (ode_row==c2):
                        state_vector[0].data[ode_row][0] -= matrix_a.data[ode_row][c2]*state_vector[1].data[c2][0]
                        state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]

                state_vector[0].data[ode_row][0] = state_vector[0].data[ode_row][0]/matrix_a.data[ode_row][ode_row]
                state_vector[1].data[ode_row][0] = state_vector[0].data[ode_row][0]


        return



    def trapezoidal_mthd(x_plus_dxdt, ddt_mat, dbydt_order):
        """
        Defines the function dx/dt=f(x) for Trapezoidal
        method.
        """

        #Calculate d/dt vector in reverse.
        for c1 in range(matrix_e.rows-1, -1, -1):
            if matrix_e.data[c1][c1]:
                try:
                    if input_vector.rows:
                        pass
                except:
                    if not (matrix_b.columns==1):
                        print("Input signal has to be a real number and not a vector.")
                    else:
                        ddt_mat[dbydt_order-1].data[c1][0] = matrix_b.data[c1][0]*input_vector
                else:
                    if not (matrix_b.columns==input_vector.rows):
                        print("Dimension of input vector incorrect.")
                    else:
                        # Added on Dec. 29, 2012.
                        ddt_mat[dbydt_order-1].data[c1][0] = 0.0
                        for c2 in range(matrix_b.columns):
                            ddt_mat[dbydt_order-1].data[c1][0] += matrix_b.data[c1][c2]*input_vector.data[c2][0]

                for c3 in range(matrix_a.columns):
                    ddt_mat[dbydt_order-1].data[c1][0] -= matrix_a.data[c1][c3]*x_plus_dxdt.data[c3][0]

                ddt_mat[dbydt_order-1].data[c1][0] = ddt_mat[dbydt_order-1].data[c1][0]*dt

                for c3 in range(matrix_e.columns):
                    if not c1==c3:
                        ddt_mat[dbydt_order-1].data[c1][0] -= matrix_e.data[c1][c3]*ode_vectors[2].data[c3][0]

                ddt_mat[dbydt_order-1].data[c1][0] = ddt_mat[dbydt_order-1].data[c1][0]

            else:
                if not (matrix_a.data[c1][c1]):
                    #The variable has no dynamics and can't even be calculated statically!
                    # May be due to a redundant loop.
                    ddt_mat[dbydt_order-1].data[c1][0] = 0.0
                    state_vector[0].data[c1][0] = 0.0
                    state_vector[1].data[c1][0] = 0.0
                else:

                    ddt_mat[dbydt_order-1].data[c1][0] = 0.0
                    state_vector[0].data[c1][0] = 0.0
                    state_vector[1].data[c1][0] = 0.0
                    try:
                        if input_vector.rows:
                            pass
                    except:
                        if not (matrix_b.columns==1):
                            print("Input signal has to be a real number and not a vector.")
                        else:
                            state_vector[0].data[c1][0] += matrix_b.data[c1][0]*input_vector
                            state_vector[1].data[c1][0] = state_vector[0].data[c1][0]
                    else:
                        if not (matrix_b.columns==input_vector.rows):
                            print("Dimension of input vector incorrect.")
                        else:
                            for c2 in range(matrix_b.columns):
                                state_vector[0].data[c1][0] += matrix_b.data[c1][c2]*input_vector.data[c2][0]
                                state_vector[1].data[c1][0] = state_vector[0].data[c1][0]

                    for c2 in range(matrix_a.columns):
                        if not (c1==c2):
                            state_vector[0].data[c1][0] -= matrix_a.data[c1][c2]*state_vector[0].data[c2][0]
                            state_vector[1].data[c1][0] = state_vector[0].data[c1][0]

                    state_vector[0].data[c1][0] = state_vector[0].data[c1][0]/matrix_a.data[c1][c1]
                    state_vector[1].data[c1][0] = state_vector[0].data[c1][0]


        return


    # Trapezoidal method
##    trapezoidal_mthd(state_vector[0], ode_vectors, 2)                       #k1=dt*(dx/dt)
##        ode_vectors[2].data[c1][0]=(ode_vectors[0].data[c1][0]+ode_vectors[1].data[c1][0])/2.0
##        state_vector[1].data[c1][0]=state_vector[0].data[c1][0]+ode_vectors[2].data[c1][0]
##        ode_vectors[0].data[c1][0]=ode_vectors[1].data[c1][0]

    # Runge-Kutta 4th order method
    #k1=dt*(dx/dt)
    #k2=dt*d/dt(x+k1/2)
    #k3=dt*d/dt(x+k2/2)
    #k4=dt*d/dt(x+k3)

    for c1 in range(matrix_e.rows-1, -1, -1):
        runge_function4(state_vector[0], ode_vectors, 1, c1)
        runge_function4(state_vector[0], ode_vectors, 2, c1)
        runge_function4(state_vector[0], ode_vectors, 3, c1)
        runge_function4(state_vector[0], ode_vectors, 4, c1)

        ode_vectors[4].data[c1][0] = (ode_vectors[0].data[c1][0] + 2.0*ode_vectors[1].data[c1][0] + 2.0*ode_vectors[2].data[c1][0] + \
                                ode_vectors[3].data[c1][0])/6.0
        state_vector[1].data[c1][0] = state_vector[0].data[c1][0]+ode_vectors[4].data[c1][0]


    # Runge-Kutta 5th order method
    #k1=dt*(dx/dt)
    #k2=dt*d/dt(x+k1)
    #k3=dt*d/dt(x+(k1+k2)/2)
    #k4=dt*d/dt(x+(14k1+5k2-3k3)/64)
    #k5=dt*d/dt(x+(-12k1-12k2+8k3+64k4)/96)
    #k6=dt*d/dt(x+(-9k2+5k3+16k4+36k5)/64)

#    for c1 in range(state_vector[1].rows):
#        runge_function5(state_vector[0], ode_vectors, 1, c1)
#        runge_function5(state_vector[0], ode_vectors, 2, c1)
#        runge_function5(state_vector[0], ode_vectors, 3, c1)
#        runge_function5(state_vector[0], ode_vectors, 4, c1)
#        runge_function5(state_vector[0], ode_vectors, 5, c1)
#        runge_function5(state_vector[0], ode_vectors, 6, c1)

#        ode_vectors[4].data[c1][0]=(ode_vectors[0].data[c1][0] + 2.0*ode_vectors[1].data[c1][0] + 2.0*ode_vectors[2].data[c1][0] + \
#                            ode_vectors[3].data[c1][0])/6.0
#        state_vector[1].data[c1][0]=state_vector[0].data[c1][0]+ode_vectors[4].data[c1][0]

##        ode_vectors[6].data[c1][0]=7.0*ode_vectors[0].data[c1][0]
##        ode_vectors[6].data[c1][0] += 12.0*ode_vectors[2].data[c1][0]
##        ode_vectors[6].data[c1][0] += 7.0*ode_vectors[3].data[c1][0]
##        ode_vectors[6].data[c1][0] += 32.0*ode_vectors[4].data[c1][0]
##        ode_vectors[6].data[c1][0] += 32.0*ode_vectors[5].data[c1][0]
##        ode_vectors[6].data[c1][0]=ode_vectors[6].data[c1][0]/90.0

##        state_vector[1].data[c1][0]=state_vector[0].data[c1][0]+ode_vectors[6].data[c1][0]


    return



def reset_stiff_branch_currents(system_loop_map, branch_params, branches_in_stiff_loops, state_vector):
    """
    Find out which branches are only in stiff loops.
    Iterate through all branches. Check if a branch is
    in a loop. Check if that loop has a single instance
    of a stiff branch anywhere. If so, loop is stiff.
    If the branch is in a loop which does not have a single
    stiff branch, it is a non stiff branch. In all other cases
    it is a stiff branch.
    """

    for c1 in range(len(branches_in_stiff_loops)):
        branch_is_stiff = "yes"
        c2 = 0
        while c2<len(system_loop_map) and branch_is_stiff=="yes":
            if system_loop_map[c2][c1]=="no":
                pass
            else:
                current_loop_stiff = "no"
                for c3 in range(len(system_loop_map[c2])):
                    if system_loop_map[c2][c3]=="stiff_forward" or \
                                system_loop_map[c2][c3]=="stiff_reverse":
                        current_loop_stiff = "yes"

                if current_loop_stiff=="no":
                    branch_is_stiff = "no"
            c2 += 1

        if branch_is_stiff=="yes":
            branches_in_stiff_loops[c1] = "yes"
        else:
            branches_in_stiff_loops[c1] = "no"


    # Recalculate the stiff branch currents from the loop currents
    for c1 in range(len(branch_params)):
        if branches_in_stiff_loops[c1]=="yes":
            branch_params[c1][-1][2] = 0.0
            for c2 in range(len(system_loop_map)):
                if system_loop_map[c2][c1]=="forward" or system_loop_map[c2][c1]=="stiff_forward":
                    branch_params[c1][-1][2] += state_vector[1].data[c2][0]

                elif system_loop_map[c2][c1]=="reverse" or system_loop_map[c2][c1]=="stiff_reverse":
                    branch_params[c1][-1][2] -= state_vector[1].data[c2][0]


    return



def determine_nodes_in_kcl(inductor_list, branches_in_kcl_nodes, nodes_in_kcl_calc, branch_events):
    """
    Check which branch containing an inductor
    is incident at a node where a branch has a hard
    event. If so, nodal analysis is requires and the
    branches incident at the node need to checked
    for freewheeling.
    *******************************
    This function is no longer used.
    *******************************
    """

    for c1 in range(len(inductor_list)):
        for c2 in range(len(branches_in_kcl_nodes)):
            if inductor_list[c1] in branches_in_kcl_nodes[c2]:
                for c3 in branches_in_kcl_nodes[c2]:
                    if c3==inductor_list[c1]:
                        pass
                    else:
                        if branch_events[c3]=="hard":
                            nodal_analysis_reqd = "yes"
                            if c2 not in nodes_in_kcl_calc:
                                nodes_in_kcl_calc.append(c2)

    return



def determining_stiff_branches(system_loop_map, branches_in_stiff_loops, inductor_list, inductor_stiffness):
    """
    This function is to determine which branches exist ONLY
    in stiff loops. So the branches need not be stiff, they exist only
    in stiff loops and therefore their currents are negligible.
    """

    for c1 in range(len(branches_in_stiff_loops)):
        branch_is_stiff = "yes"
        c2 = 0
        while c2<len(system_loop_map) and branch_is_stiff=="yes":
            if system_loop_map[c2][c1]=="no":
                pass
            else:
                current_loop_stiff = "no"
                for c3 in range(len(system_loop_map[c2])):
                    if system_loop_map[c2][c3]=="stiff_forward" or system_loop_map[c2][c3]=="stiff_reverse":
                        current_loop_stiff = "yes"

                if current_loop_stiff=="no":
                    branch_is_stiff = "no"
            c2 += 1

        if branch_is_stiff=="yes":
            branches_in_stiff_loops[c1] = "yes"
        else:
            branches_in_stiff_loops[c1] = "no"

        if c1 in inductor_list:
            inductor_stiffness[inductor_list.index(c1)] = branches_in_stiff_loops[c1]


    return



def determining_matrices_for_stiff_loops(system_loop_map, branch_params, stiff_loops, nonstiff_loops, stiff_sys_mat_a1, stiff_sys_mat_a2, \
                        stiff_sys_mat_e, stiff_sys_mat_b):

    """
    This function generates the matrices for solving stiff equations in particular.
    A stiff equation is of the form -A1*xstiff = -E*xnonstiff + A2*xnonstiff + B*u
    """

    for c1 in range(len(stiff_loops)):
        for c2 in range(c1, len(stiff_loops)):
            if c1==c2:
                loop_row = stiff_loops[c1]
                for c3 in range(len(branch_params)):
                    if not system_loop_map[loop_row][c3]=="no":
                        stiff_sys_mat_a1.data[c1][c1] += branch_params[c3][-1][0][0]

                        if system_loop_map[loop_row][c3]=="forward" or system_loop_map[loop_row][c3]=="stiff_forward":
                            for c4 in range(stiff_sys_mat_b.columns):
                                stiff_sys_mat_b.data[c1][c4] += branch_params[c3][-1][1][c4]

                        if system_loop_map[loop_row][c3]=="reverse" or system_loop_map[loop_row][c3]=="stiff_reverse":
                            for c4 in range(stiff_sys_mat_b.columns):
                                stiff_sys_mat_b.data[c1][c4] -= branch_params[c3][-1][1][c4]

            else:
                loop_row1 = stiff_loops[c1]
                loop_row2 = stiff_loops[c2]
                for c3 in range(len(branch_params)):
                    if system_loop_map[loop_row1][c3]=="forward" or system_loop_map[loop_row1][c3]=="stiff_forward":
                        if system_loop_map[loop_row2][c3]=="forward" or system_loop_map[loop_row2][c3]=="stiff_forward":
                            stiff_sys_mat_a1.data[c1][c2] += branch_params[c3][-1][0][0]

                        elif system_loop_map[loop_row2][c3]=="reverse" or system_loop_map[loop_row2][c3]=="stiff_reverse":
                            stiff_sys_mat_a1.data[c1][c2] -= branch_params[c3][-1][0][0]

                    elif system_loop_map[loop_row1][c3]=="reverse" or system_loop_map[loop_row1][c3]=="stiff_reverse":
                        if system_loop_map[loop_row2][c3]=="forward" or system_loop_map[loop_row2][c3]=="stiff_forward":
                            stiff_sys_mat_a1.data[c1][c2] -= branch_params[c3][-1][0][0]

                        elif system_loop_map[loop_row2][c3]=="reverse" or system_loop_map[loop_row2][c3]=="stiff_reverse":
                            stiff_sys_mat_a1.data[c1][c2] += branch_params[c3][-1][0][0]


    for c1 in range(len(stiff_loops)):
        for c2 in range(c1):
            if not c1==c2:
                 stiff_sys_mat_a1.data[c1][c2] = stiff_sys_mat_a1.data[c2][c1]


    for c1 in range(len(stiff_loops)):
        for c2 in range(len(nonstiff_loops)):
            loop_row1 = stiff_loops[c1]
            loop_row2 = nonstiff_loops[c2]
            for c3 in range(len(branch_params)):
                if system_loop_map[loop_row1][c3]=="forward" or system_loop_map[loop_row1][c3]=="stiff_forward":
                    if system_loop_map[loop_row2][c3]=="forward" or system_loop_map[loop_row2][c3]=="stiff_forward":
                        stiff_sys_mat_a2.data[c1][c2] += branch_params[c3][-1][0][0]
                        stiff_sys_mat_e.data[c1][c2] += branch_params[c3][-1][0][1]

                    elif system_loop_map[loop_row2][c3]=="reverse" or system_loop_map[loop_row2][c3]=="stiff_reverse":
                        stiff_sys_mat_a2.data[c1][c2] -= branch_params[c3][-1][0][0]
                        stiff_sys_mat_e.data[c1][c2] -= branch_params[c3][-1][0][1]

                elif system_loop_map[loop_row1][c3]=="reverse" or system_loop_map[loop_row1][c3]=="stiff_reverse":
                    if system_loop_map[loop_row2][c3]=="forward" or system_loop_map[loop_row2][c3]=="stiff_forward":
                        stiff_sys_mat_a2.data[c1][c2] -= branch_params[c3][-1][0][0]
                        stiff_sys_mat_e.data[c1][c2] -= branch_params[c3][-1][0][1]

                    elif system_loop_map[loop_row2][c3]=="reverse" or system_loop_map[loop_row2][c3]=="stiff_reverse":
                        stiff_sys_mat_a2.data[c1][c2] += branch_params[c3][-1][0][0]
                        stiff_sys_mat_e.data[c1][c2] += branch_params[c3][-1][0][1]



    for c1 in range(stiff_sys_mat_a1.rows):
        if not stiff_sys_mat_a1.data[c1][c1]:
            c2 = c1+1
            branch_found = "no"
            while (c2<stiff_sys_mat_a1.rows) and branch_found=="no":
                if stiff_sys_mat_a1.data[c2][c1]:
                    for c3 in range(stiff_sys_mat_a1.columns):
                        stiff_sys_mat_a1.data[c1][c3], stiff_sys_mat_a1.data[c2][c3] = stiff_sys_mat_a1.data[c2][c3], stiff_sys_mat_a1.data[c1][c3]

                    for c3 in range(stiff_sys_mat_a2.columns):
                        stiff_sys_mat_a2.data[c1][c3], stiff_sys_mat_a2.data[c2][c3] = stiff_sys_mat_a2.data[c2][c3], stiff_sys_mat_a2.data[c1][c3]

                    for c3 in range(stiff_sys_mat_b.columns):
                        stiff_sys_mat_b.data[c1][c3], stiff_sys_mat_b.data[c2][c3] = stiff_sys_mat_b.data[c2][c3], stiff_sys_mat_b.data[c1][c3]

                    for c3 in range(stiff_sys_mat_e.columns):
                        stiff_sys_mat_e.data[c1][c3], stiff_sys_mat_e.data[c2][c3] = stiff_sys_mat_e.data[c2][c3], stiff_sys_mat_e.data[c1][c3]

                    branch_found = "yes"

                c2 += 1


        if stiff_sys_mat_a1.data[c1][c1]:
            for c2 in range(c1+1, stiff_sys_mat_a1.rows):
                if stiff_sys_mat_a1.data[c2][c1]:
                    diag_element = stiff_sys_mat_a1.data[c2][c1]
                    for c3 in range(stiff_sys_mat_a1.columns):
                        stiff_sys_mat_a1.data[c2][c3] -= stiff_sys_mat_a1.data[c1][c3]*diag_element/stiff_sys_mat_a1.data[c1][c1]
                    for c3 in range(stiff_sys_mat_a2.columns):
                        stiff_sys_mat_a2.data[c2][c3] -= stiff_sys_mat_a2.data[c1][c3]*diag_element/stiff_sys_mat_a1.data[c1][c1]
                    for c3 in range(stiff_sys_mat_b.columns):
                        stiff_sys_mat_b.data[c2][c3] -= stiff_sys_mat_b.data[c1][c3]*diag_element/stiff_sys_mat_a1.data[c1][c1]
                    for c3 in range(stiff_sys_mat_e.columns):
                        stiff_sys_mat_e.data[c2][c3] -= stiff_sys_mat_e.data[c1][c3]*diag_element/stiff_sys_mat_a1.data[c1][c1]


    return
