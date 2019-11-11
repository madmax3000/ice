#! /usr/bin/env python

import sys
import math
import circuit_exceptions as CktEx
import network_reader as NwRdr


class Resistor:
    """
    Resistor class. Contains functions to initiliaze
    the resistor according to name tag, unique cell position,
    update system matrix on each iteration.
    """


    def __init__(self, res_index, res_pos, res_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "Resistor"
        self.number = res_index
        self.pos_3D = res_pos
        self.sheet = NwRdr.csv_tuple(res_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(res_pos)[1:])
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.tag = res_tag
        self.has_voltage = "no"
        self.is_meter = "no"
        self.has_control = "no"
        self.resistor = 100.0
        self.voltage = 0.0
        self.current = 0.0

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Resistor is {}={} located at {} in sheet {}".format(
            self.tag, self.resistor, self.pos, self.sheet_name
        ))
        # print self.tag,
        # print "= %f" %self.resistor,
        # print " located at ",
        # print self.pos,
        # print " in sheet ",
        # print self.sheet_name

        return


    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        res_params = ["Resistor"]
        res_params.append(self.tag)
        res_params.append(self.pos)
        res_params.append(self.resistor)
        x_list.append(res_params)

        return


    def get_values(self, x_list, ckt_mat):
        """
        Takes the parameter from the spreadsheet.
        """
        self.resistor = float(x_list[0])

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix A in E.dx/dt=Ax+Bu will be updated by the
        resistor value.
        """
        for c1 in range(len(sys_loops)):
            for c2 in range(c1, len(sys_loops)):
                # Updating the elements depending
                # on the sense of the loops (aiding or opposing)
                for c3 in range(len(sys_loops[c1][c2])):
                    # Check is resistor position is there in the loop.
                    if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c2][c3]:
                        # Add resistor if branch is in forward direction
                        if sys_loops[c1][c2][c3][-1]=="forward":
                            mat_a.data[c1][c2] += self.resistor
                        else:
                            # Else subtract if branch is in reverse direction
                            mat_a.data[c1][c2] -= self.resistor
                        # Because the matrices are symmetric
                        mat_a.data[c2][c1] = mat_a.data[c1][c2]
        return


    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        The value of the resistor is transferred to the branch
        parameter in the branch where the resistor appears.
        """
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            sys_branch[-1][0][0] += self.resistor

        return


    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        pass


    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        pass

    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass

    def determine_state(self, br_currents, sys_branches, sys_events):
        pass



class Variable_Resistor:
    """
    Variable Resistor class. Similar to the class
    above except that the resistance value is a
    control input.
    """


    def __init__(self, res_index, res_pos, res_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "VariableResistor"
        self.number = res_index
        self.pos_3D = res_pos
        self.sheet = NwRdr.csv_tuple(res_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(res_pos)[1:])
        self.tag = res_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "no"
        self.is_meter = "no"
        self.has_control = "yes"
        self.control_tag=["Resistance"]
        self.control_values=[100.0]
        self.resistor = 100.0
        self.voltage = 0.0
        self.current = 0.0
        self.component_branch_pos = 0

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Variable Resistor is {}={} located at {} in sheet {}".format(
            self.tag, self.resistor, self.pos, self.sheet_name
        ))
        # print self.tag,
        # print "= %f" %self.resistor,
        # print " located at ",
        # print self.pos,
        # print " in sheet ",
        # print self.sheet_name

        return


    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        resistor_params = ["VariableResistor"]
        resistor_params.append(self.tag)
        resistor_params.append(self.pos)
        resistor_params.append("Initial resistance = %s" %str(self.resistor))
        resistor_params.append("Name of control signal = %s" %self.control_tag[0])
        x_list.append(resistor_params)

        return


    def get_values(self, x_list, ckt_mat):
        """ Takes the parameter from the spreadsheet."""
        self.resistor = float(x_list[0].split("=")[1])
        self.control_values[0] = self.resistor
        self.control_tag[0] = x_list[1].split("=")[1]
        while self.control_tag[0][0] == " ":
            self.control_tag[0] = self.control_tag[0][1:]

        while self.control_tag[0][-1] == " ":
            self.control_tag[0] = self.control_tag[0][:-1]

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix A in E.dx/dt=Ax+Bu will be updated by the
        resistor value.
        """
        for c1 in range(len(sys_loops)):
            for c2 in range(c1, len(sys_loops)):
                # Updating the elements depending
                # on the sense of the loops (aiding or opposing)
                for c3 in range(len(sys_loops[c1][c2])):
                    # Check is resistor position is there in the loop.
                    if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c2][c3]:
                        # Add resistor if branch is in forward direction
                        if sys_loops[c1][c2][c3][-1]=="forward":
                            mat_a.data[c1][c2] += self.resistor
                        else:
                            # Else subtract if branch is in reverse direction
                            mat_a.data[c1][c2] -= self.resistor
                        # Because the matrices are symmetric
                        mat_a.data[c2][c1] = mat_a.data[c1][c2]
        return


    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        The value of the resistor is transferred to the branch
        parameter in the branch where the resistor appears.
        """
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            sys_branch[-1][0][0] += self.resistor

        return


    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        pass


    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        The control input is pass on as the resistance value.
        """
        if not self.control_values[0]==self.resistor:
            sys_events[self.component_branch_pos] = "hard"
            self.resistor = self.control_values[0]

        return

    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass

    def determine_state(self, br_currents, sys_branches, sys_events):
        pass



class Inductor:
    """
    Inductor class. Contains functions to initiliaze
    the resistor according to name tag, unique cell position,
    update system matrix on each iteration.
    """

    def __init__(self, ind_index, ind_pos, ind_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "Inductor"
        self.number = ind_index
        self.pos_3D = ind_pos
        self.sheet = NwRdr.csv_tuple(ind_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(ind_pos)[1:])
        self.tag = ind_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "no"
        self.is_meter = "no"
        self.has_control = "no"
        self.inductor = 0.001
        self.voltage = 0.0
        self.current = 0.0
        self.polrty = [-1, -1]

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Inductor is {}={} located at {} in sheet {}".format(
            self.tag, self.inductor, self.pos, self.sheet_name
        ))
        # print self.tag,
        # print "= %f" %self.inductor,
        # print " located at ",
        # print self.pos,
        # print " in sheet ",
        # print self.sheet_name

        return


    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        ind_params = ["Inductor"]
        ind_params.append(self.tag)
        ind_params.append(self.pos)
        ind_params.append(self.inductor)
        # Looking for a default value of polarity
        # in the neighbouring cells
        # The polarity is for simulator use only. So not added into ind_params.
        # The polarity is in the direction of current
        # Just like an ammeter.
        self.ind_elem = NwRdr.csv_tuple_2D(self.pos)
        if self.ind_elem[0]>0:
            if ckt_mat[self.sheet][self.ind_elem[0]-1][self.ind_elem[1]]:
                self.polrty = [self.ind_elem[0]-1, self.ind_elem[1]]
        if self.ind_elem[1]>0:
            if ckt_mat[self.sheet][self.ind_elem[0]][self.ind_elem[1]-1]:
                self.polrty = [self.ind_elem[0], self.ind_elem[1]-1]
        if self.ind_elem[0]<len(ckt_mat[self.sheet])-1:
            if ckt_mat[self.sheet][self.ind_elem[0]+1][self.ind_elem[1]]:
                self.polrty = [self.ind_elem[0]+1, self.ind_elem[1]]
        if self.ind_elem[1]<len(ckt_mat[self.sheet][0])-1:
            if ckt_mat[self.sheet][self.ind_elem[0]][self.ind_elem[1]+1]:
                self.polrty = [self.ind_elem[0], self.ind_elem[1]+1]


        x_list.append(ind_params)

        return


    def get_values(self, x_list, ckt_mat):
        """
        Takes the parameter from the spreadsheet.
        """
        self.inductor = float(x_list[0])

        return


    def determine_branch(self, sys_branches):
        pass


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix E in E.dx/dt=Ax+Bu will be updated by the
        inductor value.
        """
        for c1 in range(len(sys_loops)):
            for c2 in range(c1, len(sys_loops)):
                # Updating the elements depending
                # on the sense of the loops (aiding or opposing)
                for c3 in range(len(sys_loops[c1][c2])):
                    # Check if inductor is there in loop
                    if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c2][c3]:
                        # Check is branch is in same direction as loop
                        if sys_loops[c1][c2][c3][-1]=="forward":
                            mat_e.data[c1][c2] += self.inductor
                        else:
                            mat_e.data[c1][c2] -= self.inductor
                        # Because the matrices are symmetric
                        mat_e.data[c2][c1] = mat_e.data[c1][c2]
        return


    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        The value of the inductor is added to the parameter of the
        branch where the inductor is found.
        """
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            sys_branch[-1][0][1] += self.inductor

        return


    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        pass


    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        pass

    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass

    def determine_state(self, br_currents, sys_branches, sys_events):
        pass



class Variable_Inductor:
    """
    Inductor class. Contains functions to initiliaze
    the resistor according to name tag, unique cell position,
    update system matrix on each iteration.
    """

    def __init__(self, ind_index, ind_pos, ind_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "VariableInductor"
        self.number = ind_index
        self.pos_3D = ind_pos
        self.sheet = NwRdr.csv_tuple(ind_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(ind_pos)[1:])
        self.tag = ind_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "no"
        self.is_meter = "no"
        self.has_control = "yes"
        self.control_tag=["Inductance"]
        self.control_values=[0.001]
        self.inductor = 0.001
        self.voltage = 0.0
        self.current = 0.0
        self.polrty = [-1, -1]

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("VariableInductor is {}={} located at {} in sheet {}".format(
            self.tag, self.inductor, self.pos, self.sheet_name
        ))
        # print self.tag,
        # print "= %f" %self.inductor,
        # print " located at ",
        # print self.pos,
        # print " in sheet ",
        # print self.sheet_name

        return


    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        ind_params = ["VariableInductor"]
        ind_params.append(self.tag)
        ind_params.append(self.pos)
        ind_params.append("Initial inductance = %s"%str(self.inductor))
        ind_params.append("Name of control signal = %s" %self.control_tag[0])
        # Looking for a default value of polarity
        # in the neighbouring cells
        # The polarity is for simulator use only. So not added into ind_params.
        # The polarity is in the direction of current
        # Just like an ammeter.
        self.ind_elem = NwRdr.csv_tuple(self.pos)
        if self.ind_elem[0]>0:
            if ckt_mat[self.sheet][self.ind_elem[0]-1][self.ind_elem[1]]:
                self.polrty = [self.ind_elem[0]-1, self.ind_elem[1]]
        if self.ind_elem[1]>0:
            if ckt_mat[self.sheet][self.ind_elem[0]][self.ind_elem[1]-1]:
                self.polrty = [self.ind_elem[0], self.ind_elem[1]-1]
        if self.ind_elem[0]<len(ckt_mat[self.sheet])-1:
            if ckt_mat[self.sheet][self.ind_elem[0]+1][self.ind_elem[1]]:
                self.polrty = [self.ind_elem[0]+1, self.ind_elem[1]]
        if self.ind_elem[1]<len(ckt_mat[self.sheet][0])-1:
            if ckt_mat[self.sheet][self.ind_elem[0]][self.ind_elem[1]+1]:
                self.polrty = [self.ind_elem[0], self.ind_elem[1]+1]

        x_list.append(ind_params)

        return


    def get_values(self, x_list, ckt_mat):
        """
        Takes the parameter from the spreadsheet.
        """
        self.inductor = float(x_list[0].split("=")[1])
        self.control_values[0] = self.inductor
        self.control_tag[0] = x_list[1].split("=")[1]
        while self.control_tag[0][0] == " ":
            self.control_tag[0] = self.control_tag[0][1:]

        while self.control_tag[0][-1] == " ":
            self.control_tag[0] = self.control_tag[0][:-1]

        return



    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix E in E.dx/dt=Ax+Bu will be updated by the
        inductor value.
        """
        for c1 in range(len(sys_loops)):
            for c2 in range(c1, len(sys_loops)):
                # Updating the elements depending
                # on the sense of the loops (aiding or opposing)
                for c3 in range(len(sys_loops[c1][c2])):
                    # Check if inductor is there in loop
                    if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c2][c3]:
                        # Check is branch is in same direction as loop
                        if sys_loops[c1][c2][c3][-1]=="forward":
                            mat_e.data[c1][c2] += self.inductor
                        else:
                            mat_e.data[c1][c2] -= self.inductor
                        # Because the matrices are symmetric
                        mat_e.data[c2][c1] = mat_e.data[c1][c2]
        return


    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        The value of the inductor is added to the parameter of the
        branch where the inductor is found.
        """
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            sys_branch[-1][0][1] += self.inductor

        return


    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        pass


    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        The control input is pass on as the resistance value.
        """
        if not self.control_values[0]==self.inductor:
            sys_events[self.component_branch_pos] = "hard"
            self.inductor = self.control_values[0]

        return

    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass

    def determine_state(self, br_currents, sys_branches, sys_events):
        pass



class Capacitor:
    """
    Capacitor class. Contains functions to initiliaze
    the resistor according to name tag, unique cell position,
    update system matrix on each iteration.
    """


    def __init__(self, cap_index, cap_pos, cap_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "Capacitor"
        self.number = cap_index
        self.pos_3D = cap_pos
        self.sheet = NwRdr.csv_tuple(cap_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(cap_pos)[1:])
        self.tag = cap_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "yes"
        self.is_meter = "no"
        self.has_control = "no"
        self.capacitor = 10.0e-6
        self.current = 0.0
        self.voltage = 0.0
        self.v_dbydt = 0.0
        self.polrty = [-1, -1]
        self.component_banch_pos = 0
        self.component_branch_dir = 1.0

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Capacitor is {}={} located at {} with positive polarity towards {} in sheet {}".format(
            self.tag, self.capacitor, self.pos, NwRdr.csv_element_2D(self.polrty), self.sheet_name
        ))
        # print self.tag,
        # print "= %f" %self.capacitor,
        # print " located at ",
        # print self.pos,
        # print " with positive polarity towards %s" %(NwRdr.csv_element_2D(self.polrty)),
        # print " in sheet ",
        # print self.sheet_name

        return



    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        cap_params = ["Capacitor"]
        cap_params.append(self.tag)
        cap_params.append(self.pos)
        cap_params.append(self.capacitor)

        self.cap_elem = NwRdr.csv_tuple_2D(self.pos)

        if self.polrty==[-1, -1]:
            # Looking for a default value of polarity
            # in the neighbouring cells

            if self.cap_elem[0]>0:
                if ckt_mat[self.sheet][self.cap_elem[0]-1][self.cap_elem[1]]:
                    self.polrty = [self.cap_elem[0]-1, self.cap_elem[1]]
            if self.cap_elem[1]>0:
                if ckt_mat[self.sheet][self.cap_elem[0]][self.cap_elem[1]-1]:
                    self.polrty = [self.cap_elem[0], self.cap_elem[1]-1]
            if self.cap_elem[0]<len(ckt_mat[self.sheet])-1:
                if ckt_mat[self.sheet][self.cap_elem[0]+1][self.cap_elem[1]]:
                    self.polrty = [self.cap_elem[0]+1, self.cap_elem[1]]
            if self.cap_elem[1]<len(ckt_mat[self.sheet][0])-1:
                if ckt_mat[self.sheet][self.cap_elem[0]][self.cap_elem[1]+1]:
                    self.polrty = [self.cap_elem[0], self.cap_elem[1]+1]
        else:
            for c1 in range(len(sys_branch)):
                if [self.sheet, self.cap_elem[0], self.cap_elem[1]] in sys_branch[c1]:
                    if not [self.sheet, self.polrty[0], self.polrty[1]] in sys_branch[c1]:
                        print()
                        print("!"*50)
                        print("ERROR!!! Capacitor polarity should be in the same branch as the capacitor. \
Check source at {} in sheet {}".format(self.pos, self.sheet_name))
                        print("!"*50)
                        print()
                        raise CktEx.PolarityError

        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]
        cap_params.append("Positive polarity towards (cell) = %s" %NwRdr.csv_element_2D(self.polrty))

        x_list.append(cap_params)

        return




    def get_values(self, x_list, ckt_mat):
        """
        Takes the parameter from the spreadsheet.
        """
        self.capacitor = float(x_list[0])
        cap_polrty = x_list[1].split("=")[1]

        # Convert the human readable form of cell
        # to [row, column] form
        while cap_polrty[0]==" ":
            cap_polrty = cap_polrty[1:]

        self.polrty = NwRdr.csv_tuple_2D(cap_polrty)
        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        if not ckt_mat[self.sheet][self.polrty[0]][self.polrty[1]]:
            print("Polarity incorrect or changed. Branch does not exist at {} in sheet {}".format(
                NwRdr.csv_element(self.polrty). self.sheet_name))
            print()
            raise CktEx.PolarityError

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1
                if sys_branches[c1].index(self.polrty_3D)<sys_branches[c1].index(NwRdr.csv_tuple(self.pos_3D)):
                    self.component_branch_dir = 1.0
                else:
                    self.component_branch_dir = -1.0

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix B in E.dx/dt=Ax+Bu will be updated by the
        polarity of the capacitor.
        """
        for c1 in range(len(sys_loops)):
            for c2 in range(len(sys_loops[c1][c1])):
                if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c1][c2]:
                    # If the positive polarity appears before the capacitor position
                    # it means as per KVL, we are moving from +ve to -ve
                    # and so the capacitor voltage will be taken negative
                    if sys_loops[c1][c1][c2].index(self.polrty)<sys_loops[c1][c1][c2].index(NwRdr.csv_tuple(self.pos)):
                        if sys_loops[c1][c1][c2][-1]=="forward":
                            mat_b.data[c1][source_list.index(self.pos)] = -1.0
                        else:
                            mat_b.data[c1][source_list.index(self.pos)] = 1.0
                    else:
                        if sys_loops[c1][c1][c2][-1]=="forward":
                            mat_b.data[c1][source_list.index(self.pos)] = 1.0
                        else:
                            mat_b.data[c1][source_list.index(self.pos)] = -1.0
        return


    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        Transfers parameters to system branch if capacitor
        exists in the branch.
        """
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            if sys_branch.index(self.polrty_3D)<sys_branch.index(NwRdr.csv_tuple(self.pos_3D)):
                sys_branch[-1][1][source_list.index(self.pos_3D)] = -1.0
            else:
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 1.0
        return


    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        """
        The capacitor voltage is updated in the matrix u in
        E.dx/dt=Ax+Bu .
        """
        self.v_dbydt = self.current/self.capacitor

        self.voltage += self.v_dbydt*dt
        mat_u.data[source_lst.index(self.pos_3D)][0] = self.voltage
        self.op_value = self.voltage

        return



    def update_val_old(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        The capacitor current is calculated as a result of the KVL.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1


        if sys_branches[branch_pos].index(self.polrty)<sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
            self.current = sys_branches[branch_pos][-1][2]
        else:
            self.current = -sys_branches[branch_pos][-1][2]

        return


    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        The capacitor current is calculated as a result of the KVL.
        """

        self.current = self.component_branch_dir*sys_branches[self.component_branch_pos][-1][2]
        return

    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass

    def determine_state(self, br_currents, sys_branches, sys_events):
        pass




class Voltage_Source:
    """
    Voltage Source class. Contains functions to initiliaze
    the resistor according to name tag, unique cell position,
    update system matrix on each iteration.
    """


    def __init__(self, volt_index, volt_pos, volt_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "VoltageSource"
        self.number = volt_index
        self.pos_3D = volt_pos
        self.sheet = NwRdr.csv_tuple(volt_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(volt_pos)[1:])
        self.tag = volt_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "yes"
        self.is_meter = "no"
        self.has_control = "no"
        self.v_peak = 120.0
        self.v_freq = 60.0
        self.v_phase = 0.0
        self.v_offset = 0.0
        self.voltage = 0.0
        self.current = 0.0
        self.op_value = 0.0
        self.polrty = [-1, -1]

        return



    def display(self):
        """
        Displays info about the component.
        """
        print("Voltage Source is {} of %f V(peak), {} Hz(frequency), {} (degrees phase shift) and {} dc offset \
with positive polarity towards {} in sheet {}".format(
            self.tag, self.v_peak, self.v_freq, self.v_phase, self.v_offset, self.pos, \
            NwRdr.csv_element_2D(self.polrty), self.sheet_name
        ))
        # print self.tag,
        # print "of %f V(peak), %f Hz(frequency), %f (degrees phase shift) and %f dc offset" %(self.v_peak, self.v_freq, self.v_phase, self.v_offset),
        # print " located at ",
        # print self.pos,
        # print " with positive polarity towards %s" %(NwRdr.csv_element_2D(self.polrty)),
        # print " in sheet ",
        # print self.sheet_name

        return



    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        volt_params = ["VoltageSource"]
        volt_params.append(self.tag)
        volt_params.append(self.pos)
        volt_params.append("Peak (Volts) = %f" %self.v_peak)
        volt_params.append("Frequency (Hertz) = %f" %self.v_freq)
        volt_params.append("Phase (degrees) = %f" %self.v_phase)
        volt_params.append("Dc offset = %f" %self.v_offset)

        self.volt_elem = NwRdr.csv_tuple_2D(self.pos)

        if self.polrty==[-1, -1]:
            # Looking for a default value of polarity
            # in the neighbouring cells

            if self.volt_elem[0]>0:
                if ckt_mat[self.sheet][self.volt_elem[0]-1][self.volt_elem[1]]:
                    self.polrty = [self.volt_elem[0]-1, self.volt_elem[1]]
            if self.volt_elem[1]>0:
                if ckt_mat[self.sheet][self.volt_elem[0]][self.volt_elem[1]-1]:
                    self.polrty = [self.volt_elem[0], self.volt_elem[1]-1]
            if self.volt_elem[0]<len(ckt_mat[self.sheet])-1:
                if ckt_mat[self.sheet][self.volt_elem[0]+1][self.volt_elem[1]]:
                    self.polrty = [self.volt_elem[0]+1, self.volt_elem[1]]
            if self.volt_elem[1]<len(ckt_mat[self.sheet][0])-1:
                if ckt_mat[self.sheet][self.volt_elem[0]][self.volt_elem[1]+1]:
                    self.polrty = [self.volt_elem[0], self.volt_elem[1]+1]
        else:
            for c1 in range(len(sys_branch)):
                if [self.sheet, self.volt_elem[0], self.volt_elem[1]] in sys_branch[c1]:
                    if not [self.sheet, self.polrty[0], self.polrty[1]] in sys_branch[c1]:
                        print()
                        print("!"*50)
                        print("ERROR!!! Voltage source polarity should be in the same branch as the voltage source. \
Check source at {} in sheet {}".format(self.pos, self.sheet_name))
                        print("!"*50)
                        print()

        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        volt_params.append("Positive polarity towards (cell) = %s" %NwRdr.csv_element_2D(self.polrty))
        x_list.append(volt_params)

        return



    def get_values(self, x_list, ckt_mat):
        """
        Takes the parameter from the spreadsheet.
        """
        self.v_peak = float(x_list[0].split("=")[1])
        self.v_freq = float(x_list[1].split("=")[1])
        self.v_phase = float(x_list[2].split("=")[1])
        self.v_offset = float(x_list[3].split("=")[1])
        volt_polrty = x_list[4].split("=")[1]

        # Convert the human readable form of cell
        # to [row, column] form
        while volt_polrty[0]==" ":
            volt_polrty = volt_polrty[1:]

        self.polrty = NwRdr.csv_tuple_2D(volt_polrty)
        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        if not ckt_mat[self.sheet][self.polrty[0]][self.polrty[1]]:
            print("Polarity incorrect. Branch does not exist at {} in sheet {}".format(
                NwRdr.csv_element(self.polrty), self.sheet_name
            ))

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix B in E.dx/dt=Ax+Bu will be updated by the
        polarity of the voltage source.
        """
        for c1 in range(len(sys_loops)):
            for c2 in range(len(sys_loops[c1][c1])):
                if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c1][c2]:
                    # If the positive polarity appears before the voltage position
                    # it means as per KVL, we are moving from +ve to -ve
                    # and so the voltage will be taken negative
                    if sys_loops[c1][c1][c2].index(self.polrty)<sys_loops[c1][c1][c2].index(NwRdr.csv_tuple(self.pos)):
                        if sys_loops[c1][c1][c2][-1]=="forward":
                            mat_b.data[c1][source_list.index(self.pos)] = -1.0
                        else:
                            mat_b.data[c1][source_list.index(self.pos)] = 1.0
                    else:
                        if sys_loops[c1][c1][c2][-1]=="forward":
                            mat_b.data[c1][source_list.index(self.pos)] = 1.0
                        else:
                            mat_b.data[c1][source_list.index(self.pos)] = -1.0
        return



    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        Transfers parameters to system branch if voltage
        source exists in the branch.
        """
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            if sys_branch.index(self.polrty_3D)<sys_branch.index(NwRdr.csv_tuple(self.pos_3D)):
                sys_branch[-1][1][source_list.index(self.pos_3D)] = -1.0
            else:
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 1.0



    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        """
        The source voltage is updated in the matrix u in
        E.dx/dt=Ax+Bu .
        """
        self.voltage = self.v_peak*math.sin(2*math.pi*self.v_freq*t + self.v_phase*math.pi/180.0) + self.v_offset
        mat_u.data[source_lst.index(self.pos_3D)][0] = self.voltage
        self.op_value = self.voltage



    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        pass


    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass

    def determine_state(self, br_currents, sys_branches, sys_events):
        pass



class Ammeter:
    """
    Ammeter class. Contains functions to initiliaze
    the resistor according to name tag, unique cell position,
    update system matrix on each iteration.
    """


    def __init__(self, amm_index, amm_pos, amm_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "Ammeter"
        self.number = amm_index
        self.pos_3D = amm_pos
        self.sheet = NwRdr.csv_tuple(amm_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(amm_pos)[1:])
        self.tag = amm_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "no"
        self.is_meter = "yes"
        self.has_control = "no"
        self.current = 0.0
        self.op_value = 0.0
        self.polrty = [-1, -1]
        self.component_branch_pos = 0
        self.component_branch_dir = 1.0

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Ammeter is {} located at {} with positive polarity towards {} in sheet {}".format(
            self.tag, self.pos, NwRdr.csv_element_2D(self.polrty), self.sheet_name
        ))
        # print self.tag,
        # print " located at ",
        # print self.pos,
        # print " with positive polarity towards %s" %(NwRdr.csv_element_2D(self.polrty)),
        # print " in sheet ",
        # print self.sheet_name

        return


    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        amm_params = ["Ammeter"]
        amm_params.append(self.tag)
        amm_params.append(self.pos)

        self.amm_elem = NwRdr.csv_tuple_2D(self.pos)

        if self.polrty==[-1, -1]:
            # Looking for a default value of polarity
            # in the neighbouring cells

            if self.amm_elem[0]>0:
                if ckt_mat[self.sheet][self.amm_elem[0]-1][self.amm_elem[1]]:
                    self.polrty = [self.amm_elem[0]-1, self.amm_elem[1]]
            if self.amm_elem[1]>0:
                if ckt_mat[self.sheet][self.amm_elem[0]][self.amm_elem[1]-1]:
                    self.polrty = [self.amm_elem[0], self.amm_elem[1]-1]
            if self.amm_elem[0]<len(ckt_mat[self.sheet])-1:
                if ckt_mat[self.sheet][self.amm_elem[0]+1][self.amm_elem[1]]:
                    self.polrty = [self.amm_elem[0]+1, self.amm_elem[1]]
            if self.amm_elem[1]<len(ckt_mat[self.sheet][0])-1:
                if ckt_mat[self.sheet][self.amm_elem[0]][self.amm_elem[1]+1]:
                    self.polrty = [self.amm_elem[0], self.amm_elem[1]+1]

        else:
            for c1 in range(len(sys_branch)):
                if [self.sheet, self.amm_elem[0], self.amm_elem[1]] in sys_branch[c1]:
                    if not [self.sheet, self.polrty[0], self.polrty[1]] in sys_branch[c1]:
                        print()
                        print("!"*50)
                        print("ERROR!!! Ammeter polarity should be in the same branch as ammeter. \
Check ammeter at {} in sheet {}".format(self.pos, self.sheet_name))
                        print("!"*50)
                        print()
                        raise CktEx.PolarityError


        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        amm_params.append("Positive polarity towards (cell) = %s" %NwRdr.csv_element_2D(self.polrty))
        x_list.append(amm_params)

        return



    def get_values(self, x_list, ckt_mat):
        """
        Takes the parameter from the spreadsheet.
        """
        amm_polrty = x_list[0].split("=")[1]

        # Convert the human readable form of cell
        # to [row, column] form
        while amm_polrty[0]==" ":
            amm_polrty = amm_polrty[1:]

        self.polrty = NwRdr.csv_tuple_2D(amm_polrty)
        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        if not ckt_mat[self.sheet][self.polrty[0]][self.polrty[1]]:
            print("Polarity incorrect or changed. Branch does not exist at {}".format(
                NwRdr.csv_element_2D(self.polrty)
            ))
            raise CktEx.PolarityError

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1
                if sys_branches[c1].index(self.polrty_3D)>sys_branches[c1].index(NwRdr.csv_tuple(self.pos_3D)):
                    self.component_branch_dir = 1.0
                else:
                    self.component_branch_dir = -1.0

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        pass


    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        pass


    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        pass



    def update_val_old(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        The ammeter current is calculated as a result of the KVL.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
            self.current = sys_branches[branch_pos][-1][2]
        else:
            self.current = -sys_branches[branch_pos][-1][2]

        # Since it is a meter, this is its output value
        self.op_value = self.current

        return


    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        The ammeter current is calculated as a result of the KVL.
        """

        self.current = self.component_branch_dir*sys_branches[self.component_branch_pos][-1][2]
        # Since it is a meter, this is its output value
        self.op_value = self.current
        return

        self.current = self.component_branch_dir*sys_branches[self.component_branch_pos][-1][2]


    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass


    def determine_state(self, br_currents, sys_branches, sys_events):
        pass




class Voltmeter:
    """
    Voltmeter class. Contains functions to initiliaze
    the resistor according to name tag, unique cell position,
    update system matrix on each iteration.
    """

    def __init__(self, vm_index, vm_pos, vm_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "Voltmeter"
        self.number = vm_index
        self.pos_3D = vm_pos
        self.sheet = NwRdr.csv_tuple(vm_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(vm_pos)[1:])
        self.tag = vm_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "no"
        self.is_meter = "yes"
        self.has_control = "no"
        self.vm_level = 120.0
        self.current = 0.0
        self.voltage = 0.0
        self.op_value = 0.0
        self.polrty = [-1, -1]
        self.component_branch_pos = 0
        self.component_branch_dir = 1.0

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Voltmeter is {} located at {} with positive polarity towards {} in sheet".format(
            self.tag, self.pos, NwRdr.csv_element_2D(self.polrty), self.sheet_name
        ))
        # print self.tag,
        # print " located at ",
        # print self.pos,
        # print " with positive polarity towards %s" %(NwRdr.csv_element_2D(self.polrty)),
        # print " in sheet ",
        # print self.sheet_name

        return


    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        vm_params = ["Voltmeter"]
        vm_params.append(self.tag)
        vm_params.append(self.pos)
        vm_params.append("Rated voltage level to be measured = %s" %self.vm_level)

        self.vm_elem = NwRdr.csv_tuple_2D(self.pos)

        if self.polrty==[-1, -1]:
            # Looking for a default value of polarity
            # in the neighbouring cells

            if self.vm_elem[0]>0:
                if ckt_mat[self.sheet][self.vm_elem[0]-1][self.vm_elem[1]]:
                    self.polrty = [self.vm_elem[0]-1, self.vm_elem[1]]
            if self.vm_elem[1]>0:
                if ckt_mat[self.sheet][self.vm_elem[0]][self.vm_elem[1]-1]:
                    self.polrty = [self.vm_elem[0], self.vm_elem[1]-1]
            if self.vm_elem[0]<len(ckt_mat[self.sheet])-1:
                if ckt_mat[self.sheet][self.vm_elem[0]+1][self.vm_elem[1]]:
                    self.polrty = [self.vm_elem[0]+1, self.vm_elem[1]]
            if self.vm_elem[1]<len(ckt_mat[self.sheet][0])-1:
                if ckt_mat[self.sheet][self.vm_elem[0]][self.vm_elem[1]+1]:
                    self.polrty = [self.vm_elem[0], self.vm_elem[1]+1]
        else:
            for c1 in range(len(sys_branch)):
                if [self.sheet, self.vm_elem[0], self.vm_elem[1]] in sys_branch[c1]:
                    if not [self.sheet, self.polrty[0], self.polrty[1]] in sys_branch[c1]:
                        print()
                        print("!"*50)
                        print("ERROR!!! Voltmeter polarity should be in the same branch as voltmeter. \
Check voltmeter at {} in sheet {}".format(self.pos, self.sheet_name))
                        print("!"*50)
                        print()
                        raise CktEx.PolarityError

        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        vm_params.append("Positive polarity towards (cell) = %s" %NwRdr.csv_element_2D(self.polrty))
        x_list.append(vm_params)

        return


    def get_values(self, x_list, ckt_mat):
        """
        Takes the parameter from the spreadsheet.
        """
        self.vm_level = float(x_list[0].split("=")[1])
        # Choosing 1 micro Amp as the leakage current that
        # is drawn by the voltmeter.
        self.resistor = self.vm_level/1.0e-6
        vm_polrty = x_list[1].split("=")[1]

        # Convert the human readable form of cell
        # to [row, column] form
        while vm_polrty[0]==" ":
            vm_polrty = vm_polrty[1:]

        self.polrty = NwRdr.csv_tuple_2D(vm_polrty)
        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        if not ckt_mat[self.sheet][self.polrty[0]][self.polrty[1]]:
            print("Polarity incorrect or changed. Branch does not exist at {} in sheet {}".format(
                NwRdr.csv_element(self.polrty), self.sheet_name
            ))
            raise CktEx.PolarityError

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1
                if sys_branches[c1].index(self.polrty_3D)<sys_branches[c1].index(NwRdr.csv_tuple(self.pos_3D)):
                    self.component_branch_dir = 1.0
                else:
                    self.component_branch_dir = -1.0

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix A in E.dx/dt=Ax+Bu will be updated by the
        resistor value.
        """

        for c1 in range(len(sys_loops)):
            for c2 in range(c1, len(sys_loops)):
                # Updating the elements depending
                # on the sense of the loops (aiding or opposing)
                for c3 in range(len(sys_loops[c1][c2])):
                    # Check if voltmeter position is there in the loop.
                    if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c2][c3]:
                        # Add voltmeter resistor if branch is in forward direction
                        if sys_loops[c1][c2][c3][-1]=="forward":
                            mat_a.data[c1][c2] += self.resistor
                        else:
                            # Else subtract if branch is in reverse direction
                            mat_a.data[c1][c2] -= self.resistor
                        # Because the matrices are symmetric
                        mat_a.data[c2][c1] = mat_a.data[c1][c2]

        return



    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        Update the resistor info of the voltmeter
        to the branch list.
        """
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            sys_branch[-1][0][0] += self.resistor

        return


    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        pass


    def update_val_old(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        The voltmeter current is calculated as a result of the KVL.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1


        if sys_branches[branch_pos].index(self.polrty)<sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
            self.current = sys_branches[branch_pos][-1][2]
        else:
            self.current = -sys_branches[branch_pos][-1][2]


        # Since it is a meter, this is its output value
        self.voltage = self.resistor*self.current
        self.op_value = self.voltage

        return



    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        The voltmeter current is calculated as a result of the KVL.
        """

        self.current = self.component_branch_dir*sys_branches[self.component_branch_pos][-1][2]

        # Since it is a meter, this is its output value
        self.voltage = self.resistor*self.current
        self.op_value = self.voltage

        return


    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass


    def determine_state(self, br_currents, sys_branches, sys_events):
        pass




class Current_Source:
    """
    Current source class. Contains functions to initiliaze
    the resistor according to name tag, unique cell position,
    update system matrix on each iteration.
    """


    def __init__(self, cs_index, cs_pos, cs_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "CurrentSource"
        self.number = cs_index
        self.pos_3D = cs_pos
        self.sheet = NwRdr.csv_tuple(cs_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(cs_pos)[1:])
        self.tag = cs_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "yes"
        self.is_meter = "no"
        self.has_control = "no"
        self.cs_peak = 5.0
        self.cs_freq = 60.0
        self.cs_phase = 0.0
        self.cs_level = 120.0
        self.resistor = 1.0
        self.current = 0.0
        self.voltage = 0.0
        self.op_value = 0.0
        self.polrty=[-1, -1]
        self.component_banch_pos = 0
        self.component_branch_dir = 1.0

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Current Source is {} of {} A (peak), {} Hz(frequency) and {} (degrees phase shift) \
located at {} with positive polarity towards {} in sheet {}".format(
            self.tag, self.cs_peak, self.cs_freq, self.cs_phase, self.pos, \
            NwRdr.csv_element(self.polrty), self.sheet_name
        ))
        # print self.tag,
        # print "of %f A (peak), %f Hz(frequency) and %f (degrees phase shift)" %(self.cs_peak, self.cs_freq, self.cs_phase),
        # print " located at ",
        # print self.pos,
        # print " with positive polarity towards %s" %(NwRdr.csv_element(self.polrty)),
        # print " in sheet ",
        # print self.sheet_name

        return


    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        cs_params = ["CurrentSource"]
        cs_params.append(self.tag)
        cs_params.append(self.pos)
        cs_params.append("Peak (Amps) = %f" %self.cs_peak)
        cs_params.append("Frequency (Hertz) = %f" %self.cs_freq)
        cs_params.append("Phase (degrees) = %f" %self.cs_phase)

        self.cs_elem = NwRdr.csv_tuple_2D(self.pos)

        if self.polrty==[-1, -1]:
            # Looking for a default value of polarity
            # in the neighbouring cells

            if self.cs_elem[0]>0:
                if ckt_mat[self.sheet][self.cs_elem[0]-1][self.cs_elem[1]]:
                    self.polrty = [self.cs_elem[0]-1, self.cs_elem[1]]
            if self.cs_elem[1]>0:
                if ckt_mat[self.sheet][self.cs_elem[0]][self.cs_elem[1]-1]:
                    self.polrty = [self.cs_elem[0], self.cs_elem[1]-1]
            if self.cs_elem[0]<len(ckt_mat[self.sheet])-1:
                if ckt_mat[self.sheet][self.cs_elem[0]+1][self.cs_elem[1]]:
                    self.polrty = [self.cs_elem[0]+1, self.cs_elem[1]]
            if self.cs_elem[1]<len(ckt_mat[self.sheet][0])-1:
                if ckt_mat[self.sheet][self.cs_elem[0]][self.cs_elem[1]+1]:
                    self.polrty = [self.cs_elem[0], self.cs_elem[1]+1]
        else:
            for c1 in range(len(sys_branch)):
                if NwRdr.csv_tuple(self.pos_3D) in sys_branch[c1]:
                    if not self.polrty in sys_branch[c1]:
                        print()
                        print("!"*50)
                        print("ERROR!!! Current source polarity should be in the same branch as the current source. \
Check source at {} in sheet {}".format(self.pos, self.sheet_name))
                        print("!"*50)
                        print()
                        raise CktEx.PolarityError

        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        cs_params.append("Positive polarity towards (cell) = %s" %NwRdr.csv_element_2D(self.polrty))
        x_list.append(cs_params)

        return



    def get_values(self, x_list, ckt_mat):
        """ Takes the parameter from the spreadsheet."""
        self.cs_peak = float(x_list[0].split("=")[1])
        self.cs_freq = float(x_list[1].split("=")[1])
        self.cs_phase = float(x_list[2].split("=")[1])
        curr_polrty = x_list[3].split("=")[1]

        # Convert the human readable form of cell
        # to [row, column] form
        while curr_polrty[0]==" ":
            curr_polrty = curr_polrty[1:]

        self.polrty = NwRdr.csv_tuple_2D(curr_polrty)
        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        if not ckt_mat[self.sheet][self.polrty[0]][self.polrty[1]]:
            print("Polarity incorrect. Branch does not exist at {} in sheet {}".format(
                NwRdr.csv_element_2D(self.polrty), self.sheet_name
            ))
            raise CktEx.PolarityError

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1
                if sys_branches[c1].index(self.polrty_3D)<sys_branches[c1].index(NwRdr.csv_tuple(self.pos_3D)):
                    self.component_branch_dir = 1.0
                else:
                    self.component_branch_dir = -1.0

        return



    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix A in E.dx/dt=Ax+Bu will be updated by the
        resistor value of the current source.
        """

        for c1 in range(len(sys_loops)):
            for c2 in range(c1, len(sys_loops)):
                # Updating the elements depending
                # on the sense of the loops (aiding or opposing)
                for c3 in range(len(sys_loops[c1][c2])):
                    # Check if current source position is there in the loop.
                    if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c2][c3]:
                        # Add current source series resistor
                        # if branch is in forward direction
                        if sys_loops[c1][c2][c3][-1]=="forward":
                            mat_a.data[c1][c2] += self.resistor
                        else:
                            # Else subtract if branch is in reverse direction
                            mat_a.data[c1][c2] -= self.resistor
                        # Because the matrices are symmetric
                        mat_a.data[c2][c1] = mat_a.data[c1][c2]

                        # If the positive polarity appears before the voltage position
                        # it means as per KVL, we are moving from +ve to -ve
                        # and so the voltage will be taken negative
                        if sys_loops[c1][c1][c2].index(self.polrty)<sys_loops[c1][c1][c2].index(NwRdr.csv_tuple(self.pos)):
                            if sys_loops[c1][c1][c2][-1]=="forward":
                                mat_b.data[c1][source_list.index(self.pos)] = -1.0
                            else:
                                mat_b.data[c1][source_list.index(self.pos)] = 1.0
                        else:
                            if sys_loops[c1][c1][c2][-1]=="forward":
                                mat_b.data[c1][source_list.index(self.pos)] = 1.0
                            else:
                                mat_b.data[c1][source_list.index(self.pos)] = -1.0

        return



    def transfer_to_branch(self, sys_branch, source_list, mat_u):
        """
        Update the resistor info of the current source
        to the branch list
        """
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            sys_branch[-1][0][0] += self.resistor

        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            if sys_branch.index(self.polrty_3D)<sys_branch.index(NwRdr.csv_tuple(self.pos_3D)):
                sys_branch[-1][1][source_list.index(self.pos_3D)] = -1.0
            else:
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 1.0

        return



    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        """
        The source current is updated in the matrix u in
        E.dx/dt=Ax+Bu. The matrix E has a row set to zero. The
        matrix B has the diagonal element in the row set to 1,
        others set to zero.
        """

        # Updating the current source value
        self.current = self.cs_peak*math.sin(2*math.pi*self.cs_freq*t+self.cs_phase)

        # The value passed to the input matrix is
        # the voltage calculated
        mat_u.data[source_lst.index(self.pos_3D)][0] = self.voltage

        # The output value of the source will the current
        # even though it is actually modelled as a
        # voltage source with a series resistance.
        self.op_value = self.current

        return



    def update_val_old(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        This function calculates the actual current in
        the current source branch. With this, the branch voltage is
        found with respect to the existing voltage source. The branch
        voltage is then used to calculate the new voltage source value.
        """

        # Local variable to calculate the branch
        # current from all loops that contain
        # the current source branch.
        act_current = 0.0


        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        if sys_branches[branch_pos].index(self.polrty)<sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
            act_current = sys_branches[branch_pos][-1][2]
        else:
            act_current = -sys_branches[branch_pos][-1][2]


        # The branch voltage is the KVL with the
        # existing voltage source and the branch current
        branch_voltage = self.voltage+act_current*self.resistor
        # The new source voltage will be the branch voltage
        # in addition to the desired value of current.
        self.voltage = branch_voltage+self.current*self.resistor

        return


    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        This function calculates the actual current in
        the current source branch. With this, the branch voltage is
        found with respect to the existing voltage source. The branch
        voltage is then used to calculate the new voltage source value.
        """

        # Local variable to calculate the branch
        # current from all loops that contain
        # the current source branch.
        act_current = 0.0
        act_current = self.component_branch_dir*sys_branches[self.component_branch_pos][-1][2]

        # The branch voltage is the KVL with the
        # existing voltage source and the branch current
        branch_voltage = self.voltage+act_current*self.resistor
        # The new source voltage will be the branch voltage
        # in addition to the desired value of current.
        self.voltage = branch_voltage+self.current*self.resistor

        return

    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass


    def determine_state(self, br_currents, sys_branches, sys_events):
        pass




class Controlled_Voltage_Source:
    """
    Controlled Voltage Source class. Takes the instantaneous
    voltage as input from the user file.
    """


    def __init__(self, volt_index, volt_pos, volt_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "ControlledVoltageSource"
        self.number = volt_index
        self.pos_3D = volt_pos
        self.sheet = NwRdr.csv_tuple(volt_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(volt_pos)[1:])
        self.tag = volt_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "yes"
        self.is_meter = "no"
        self.has_control = "yes"
        self.voltage = 0.0
        self.current = 0.0
        self.op_value = 0.0
        self.polrty = [-1, -1]
        self.control_tag = ["Control"]
        self.control_values = [0.0]

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Controlled Voltage Source is {} located at {} with positive polarity towards {} in sheet {}".format(
            self.tag, self.pos, NwRdr.csv_element_2D(self.polrty), self.sheet_name
        ))
        # print self.tag,
        # print " located at ",
        # print self.pos,
        # print " with positive polarity towards %s" %(NwRdr.csv_element_2D(self.polrty)),
        # print " in sheet ",
        # print self.sheet_name

        return


    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        volt_params = ["ControlledVoltageSource"]
        volt_params.append(self.tag)
        volt_params.append(self.pos)

        self.volt_elem = NwRdr.csv_tuple_2D(self.pos)

        if self.polrty==[-1, -1]:
            # Looking for a default value of polarity
            # in the neighbouring cells

            if self.volt_elem[0]>0:
                if ckt_mat[self.sheet][self.volt_elem[0]-1][self.volt_elem[1]]:
                    self.polrty = [self.volt_elem[0]-1, self.volt_elem[1]]
            if self.volt_elem[1]>0:
                if ckt_mat[self.sheet][self.volt_elem[0]][self.volt_elem[1]-1]:
                    self.polrty = [self.volt_elem[0], self.volt_elem[1]-1]
            if self.volt_elem[0]<len(ckt_mat[self.sheet])-1:
                if ckt_mat[self.sheet][self.volt_elem[0]+1][self.volt_elem[1]]:
                    self.polrty = [self.volt_elem[0]+1, self.volt_elem[1]]
            if self.volt_elem[1]<len(ckt_mat[self.sheet][0])-1:
                if ckt_mat[self.sheet][self.volt_elem[0]][self.volt_elem[1]+1]:
                    self.polrty = [self.volt_elem[0], self.volt_elem[1]+1]

        else:

            for c1 in range(len(sys_branch)):
                if NwRdr.csv_tuple(self.pos_3D) in sys_branch[c1]:
                    if not [self.sheet, self.polrty[0], self.polrty[1]]  in sys_branch[c1]:
                        print()
                        print("!"*50)
                        print("ERROR!!! Voltage source polarity should be in the same branch as the voltage source. \
Check source at {} in sheet {}".format(self.pos, self.sheet_name))
                        print("!"*50)
                        print()
                        raise CktEx.PolarityError

        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        volt_params.append("Positive polarity towards (cell) = %s" %NwRdr.csv_element_2D(self.polrty))
        volt_params.append("Name of control signal = %s" %self.control_tag[0])
        x_list.append(volt_params)

        return



    def get_values(self, x_list, ckt_mat):
        """ Takes the parameter from the spreadsheet."""
        volt_polrty = x_list[0].split("=")[1]

        # Convert the human readable form of cell
        # to [row, column] form
        while volt_polrty[0]==" ":
            volt_polrty = volt_polrty[1:]

        self.polrty = NwRdr.csv_tuple_2D(volt_polrty)
        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        if not ckt_mat[self.sheet][self.polrty[0]][self.polrty[1]]:
            print("Polarity incorrect. Branch does not exist at {} in sheet {}".format(
                NwRdr.csv_element_2D(self.polrty), self.sheet_name
            ))
            raise CktEx.PolarityError

        self.control_tag[0] = x_list[1].split("=")[1]
        while self.control_tag[0][0]==" ":
            self.control_tag[0] = self.control_tag[0][1:]

        return


    def determine_branch(self, sys_branches):
        pass


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix B in E.dx/dt=Ax+Bu will be updated by the
        polarity of the voltage source.
        """
        for c1 in range(len(sys_loops)):
            for c2 in range(len(sys_loops[c1][c1])):
                if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c1][c2]:
                    # If the positive polarity appears before the voltage position
                    # it means as per KVL, we are moving from +ve to -ve
                    # and so the voltage will be taken negative
                    if sys_loops[c1][c1][c2].index(self.polrty)<sys_loops[c1][c1][c2].index(NwRdr.csv_tuple(self.pos)):
                        if sys_loops[c1][c1][c2][-1]=="forward":
                            mat_b.data[c1][source_list.index(self.pos)] = -1.0
                        else:
                            mat_b.data[c1][source_list.index(self.pos)] = 1.0
                    else:
                        if sys_loops[c1][c1][c2][-1]=="forward":
                            mat_b.data[c1][source_list.index(self.pos)] = 1.0
                        else:
                            mat_b.data[c1][source_list.index(self.pos)] = -1.0

        return



    def transfer_to_branch(self, sys_branch, source_list, mat_u):
        """
        Transfers parameters to system branch if voltage
        source exists in the branch.
        """
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            if sys_branch.index(self.polrty_3D)<sys_branch.index(NwRdr.csv_tuple(self.pos_3D)):
                sys_branch[-1][1][source_list.index(self.pos_3D)] = -1.0
            else:
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 1.0

        return



    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        """
        The source voltage is updated in the matrix u in
        E.dx/dt=Ax+Bu.
        """
        mat_u.data[source_lst.index(self.pos_3D)][0] = self.control_values[0]
        self.op_value = self.control_values[0]

        return


    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        pass

    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        pass

    def determine_state(self, br_currents, sys_branches, sys_events):
        pass



class Diode:
    """
    Diode class. Contains functions to initiliaze
    the diode according to name tag, unique cell position,
    update system matrix on each iteration.
    """


    def __init__(self, diode_index, diode_pos, diode_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type = "Diode"
        self.number = diode_index
        self.pos_3D = diode_pos
        self.sheet = NwRdr.csv_tuple(diode_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(diode_pos)[1:])
        self.tag = diode_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "yes"
        self.is_meter = "no"
        self.has_control = "no"
        self.diode_level = 120.0
        self.current = 0.0
        self.voltage = 0.0
        self.polrty = [-1, -1]
        self.resistor_on = 0.01
        self.status = "off"
        self.component_banch_pos = 0
        self.component_branch_dir = 1.0

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Diode is {} located at {} with cathode polarity towards {} in sheet {}".format(
            self.tag, self.pos, NwRdr.csv_element_2D(self.polrty), self.sheet_name
        ))
        # print self.tag,
        # print " located at ",
        # print self.pos,
        # print " with cathode polarity towards %s" %(NwRdr.csv_element_2D(self.polrty)),
        # print " in sheet ",
        # print self.sheet_name

        return



    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        diode_params = ["Diode"]
        diode_params.append(self.tag)
        diode_params.append(self.pos)
        diode_params.append("Voltage level (V) = %f" %self.diode_level)

        self.diode_elem = NwRdr.csv_tuple_2D(self.pos)

        if self.polrty==[-1, -1]:
            # Looking for a default value of polarity
            # in the neighbouring cells

            if self.diode_elem[0]>0:
                if ckt_mat[self.sheet][self.diode_elem[0]-1][self.diode_elem[1]]:
                    self.polrty = [self.diode_elem[0]-1, self.diode_elem[1]]
            if self.diode_elem[1]>0:
                if ckt_mat[self.sheet][self.diode_elem[0]][self.diode_elem[1]-1]:
                    self.polrty = [self.diode_elem[0], self.diode_elem[1]-1]
            if self.diode_elem[0]<len(ckt_mat[self.sheet])-1:
                if ckt_mat[self.sheet][self.diode_elem[0]+1][self.diode_elem[1]]:
                    self.polrty = [self.diode_elem[0]+1, self.diode_elem[1]]
            if self.diode_elem[1]<len(ckt_mat[self.sheet][0])-1:
                if ckt_mat[self.sheet][self.diode_elem[0]][self.diode_elem[1]+1]:
                    self.polrty = [self.diode_elem[0], self.diode_elem[1]+1]
        else:
            for c1 in range(len(sys_branch)):
                if [self.sheet, self.diode_elem[0], self.diode_elem[1]] in sys_branch[c1]:
                    if not [self.sheet, self.polrty[0], self.polrty[1]] in sys_branch[c1]:
                        print()
                        print("!"*50)
                        print("ERROR!!! Diode polarity should be in the same branch as the diode. \
Check diode at {} in sheet {}".format(self.pos, self.sheet_name))
                        print("!"*50)
                        print()
                        raise CktEx.PolarityError

        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        diode_params.append("Cathode polarity towards (cell) = %s" %NwRdr.csv_element_2D(self.polrty))
        x_list.append(diode_params)

        return



    def get_values(self, x_list, ckt_mat):
        """
        Takes the parameter from the spreadsheet.
        """
        self.diode_level = float(x_list[0].split("=")[1])
        # Choosing 1 micro Amp as the leakage current that
        # is drawn by the diode in off state.
        self.resistor_off = self.diode_level/1.0e-6
        self.resistor = self.resistor_off


        diode_polrty = x_list[1].split("=")[1]

        # Convert the human readable form of cell
        # to [row, column] form
        while diode_polrty[0]==" ":
            diode_polrty = diode_polrty[1:]

        self.polrty = NwRdr.csv_tuple_2D(diode_polrty)
        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        if not ckt_mat[self.sheet][self.polrty[0]][self.polrty[1]]:
            print("Polarity incorrect. Branch does not exist at {} in sheet {}".format(
                NwRdr.csv_element2D(self.polrty), self.sheet_name
            ))
            raise CktEx.PolarityError

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1
                if sys_branches[c1].index(self.polrty_3D)>sys_branches[c1].index(NwRdr.csv_tuple(self.pos_3D)):
                    self.component_branch_dir = 1.0
                else:
                    self.component_branch_dir = -1.0

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix A in E.dx/dt=Ax+Bu will be updated by the
        resistor value of the diode.
        """

        for c1 in range(len(sys_loops)):
            for c2 in range(c1, len(sys_loops)):
                # Updating the elements depending
                # on the sense of the loops (aiding or opposing)
                for c3 in range(len(sys_loops[c1][c2])):
                    # Check if current source position is there in the loop.
                    if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c2][c3]:
                        # Add current source series resistor
                        # if branch is in forward direction
                        if sys_loops[c1][c2][c3][-1]=="forward":
                            mat_a.data[c1][c2] += self.resistor
                        else:
                            # Else subtract if branch is in reverse direction
                            mat_a.data[c1][c2] -= self.resistor
                        # Because the matrices are symmetric
                        mat_a.data[c2][c1] = mat_a.data[c1][c2]

                        # If the positive polarity appears before the voltage position
                        # it means as per KVL, we are moving from +ve to -ve
                        # and so the voltage will be taken negative
                        if sys_loops[c1][c1][c2].index(self.polrty)>sys_loops[c1][c1][c2].index(NwRdr.csv_tuple(self.pos)):
                            if sys_loops[c1][c1][c2][-1]=="forward":
                                mat_b.data[c1][source_list.index(self.pos)] = -1.0
                            else:
                                mat_b.data[c1][source_list.index(self.pos)] = 1.0
                        else:
                            if sys_loops[c1][c1][c2][-1]=="forward":
                                mat_b.data[c1][source_list.index(self.pos)] = 1.0
                            else:
                                mat_b.data[c1][source_list.index(self.pos)] = -1.0

        return



    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        Update the resistor info of the diode
        to the branch list.
        """

        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            sys_branch[-1][0][0] += self.resistor


        # For the diode forward voltage drop.
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            if sys_branch.index(self.polrty_3D)>sys_branch.index(NwRdr.csv_tuple(self.pos_3D)):
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 0.0
            else:
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 0.0

        if self.status=="on":
            mat_u.data[source_list.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0
        else:
            mat_u.data[source_list.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0

        return



    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        """
        The diode forward drop voltage is updated
        in the matrix u in E.dx/dt=Ax+Bu.
        """
        if self.status=="on":
            mat_u.data[source_lst.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0
        else:
            mat_u.data[source_lst.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0

        return


    def update_val_old(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        This function calculates the actual current in the
        diode branch. With this, the branch voltage is found
        with respect to the existing diode resistance. The diode
        voltage is then used to decide the turn on condition.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
            self.current = sys_branches[branch_pos][-1][2]
        else:
            self.current = -sys_branches[branch_pos][-1][2]

        self.voltage = self.current*self.resistor

        # Diode will turn on when it is forward biased
        # and it was previously off.
        if self.status=="off" and self.voltage>1.0:
            sys_events[branch_pos] = "hard"
            self.status = "on"

        # Diode will turn off only when current becomes
        # negative.
        if self.status=="on" and self.current<0.0:
            sys_events[branch_pos] = "yes"
            self.status = "off"

        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return


    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        This function calculates the actual current in the
        diode branch. With this, the branch voltage is found
        with respect to the existing diode resistance. The diode
        voltage is then used to decide the turn on condition.
        """

        self.current = self.component_branch_dir*sys_branches[self.component_branch_pos][-1][2]
        self.voltage = self.current*self.resistor

        # Diode will turn on when it is forward biased
        # and it was previously off.
        if self.status=="off" and self.voltage>1.0:
            sys_events[self.component_branch_pos] = "hard"
            self.status = "on"

        # Diode will turn off only when current becomes
        # negative.
        if self.status=="on" and self.current<0.0:
            sys_events[self.component_branch_pos] = "yes"
            self.status = "off"

        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return


    def determine_state_old(self, br_currents, sys_branches, sys_events):
        """
        Determines the state of the diode following an event
        where the continuity of current through an inductor is
        about to be broken.
        """

        # Mark the position of the diode in the branches list
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        # Since branch current direction is by default considered
        # positive when flowing away from the starting node
        # If the branch current is negative, with the diode cathode
        # closer towards the starting node, current direction is
        # positive
        if br_currents[branch_pos]*self.resistor<-1.0:
            if sys_branches[branch_pos].index(self.polrty)<sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
                if self.status=="off":
                    sys_events[branch_pos] = "yes"
                    self.status = "on"

        # If current direction is reverse, diode can never conduct
        if br_currents[branch_pos]<0.0:
            if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
                if self.status=="on":
                    sys_events[branch_pos] = "yes"
                    self.status = "off"


        if br_currents[branch_pos]*self.resistor>1.0:
            if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
                if self.status=="off":
                    sys_events[branch_pos] = "yes"
                    self.status = "on"

        if br_currents[branch_pos]>0.0:
            if sys_branches[branch_pos].index(self.polrty)<sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
                if self.status=="on":
                    sys_events[branch_pos] = "yes"
                    self.status = "off"

        # Update the value of resistance
        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return


    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        """
        Determines the state of the diode following an event
        where the continuity of current through an inductor is
        about to be broken.
        """

        # Since branch current direction is by default considered
        # positive when flowing away from the starting node
        # If the branch current is negative, with the diode cathode
        # closer towards the starting node, current direction is
        # positive
        if br_currents[self.component_branch_pos]*self.component_branch_dir*self.resistor>1.0:
            if self.status=="off":
                sys_events[self.component_branch_pos] = "yes"
                self.status = "on"

        # If current direction is reverse, diode can never conduct
        if br_currents[self.component_branch_pos]*self.component_branch_dir<0.0:
            if self.status=="on":
                sys_events[self.component_branch_pos] = "yes"
                self.status = "off"


        # Update the value of resistance
        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return


    def determine_state(self, br_currents, sys_branches, sys_events):
        """
        Determines the state of the diode following an event
        where the continuity of current through an inductor is
        about to be broken.
        """

        # Since branch current direction is by default considered
        # positive when flowing away from the starting node
        # If the branch current is negative, with the diode cathode
        # closer towards the starting node, current direction is
        # positive
        if br_currents[self.component_branch_pos]*self.component_branch_dir*self.resistor>1.0:
            if self.status=="off":
                sys_events[self.component_branch_pos] = "yes"
                self.status = "on"

        # If current direction is reverse, diode can never conduct
        if br_currents[self.component_branch_pos]*self.component_branch_dir<0.0:
            if self.status=="on":
                sys_events[self.component_branch_pos] = "yes"
                self.status = "off"


        # Update the value of resistance
        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return



class Switch:
    """
    Ideal switch class. Contains functions to initiliaze
    the switch according to name tag, unique cell position,
    update system matrix on each iteration.
    """

    def __init__(self, switch_index, switch_pos, switch_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type="Switch"
        self.number = switch_index
        self.pos_3D = switch_pos
        self.sheet = NwRdr.csv_tuple(switch_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(switch_pos)[1:])
        self.tag = switch_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "yes"
        self.switch_level = 120.0
        self.is_meter = "no"
        self.has_control = "yes"
        self.current = 0.0
        self.voltage = 0.0
        self.polrty = [-1, -1]
        self.resistor_on = 0.01
        self.status = "off"
        self.control_tag = ["Control"]
        self.control_values = [0.0]
        self.component_banch_pos = 0
        self.component_branch_dir = 1.0

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Switch is {} located at {} with negative polarity towards {} in sheet {}".format(
            self.tag, self.pos, NwRdr.csv_element_2D(self.polrty), self.sheet_name
        ))

        return



    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        switch_params = ["Switch"]
        switch_params.append(self.tag)
        switch_params.append(self.pos)
        switch_params.append("Voltage level (V) = %f" %self.switch_level)

        self.switch_elem = NwRdr.csv_tuple_2D(self.pos)

        if self.polrty==[-1, -1]:
            # Looking for a default value of polarity
            # in the neighbouring cells

            if self.switch_elem[0]>0:
                if ckt_mat[self.sheet][self.switch_elem[0]-1][self.switch_elem[1]]:
                    self.polrty = [self.switch_elem[0]-1, self.switch_elem[1]]
            if self.switch_elem[1]>0:
                if ckt_mat[self.sheet][self.switch_elem[0]][self.switch_elem[1]-1]:
                    self.polrty = [self.switch_elem[0], self.switch_elem[1]-1]

            if self.switch_elem[0]<len(ckt_mat[self.sheet])-1:
                if ckt_mat[self.sheet][self.switch_elem[0]+1][self.switch_elem[1]]:
                    self.polrty = [self.switch_elem[0]+1, self.switch_elem[1]]
            if self.switch_elem[1]<len(ckt_mat[self.sheet][0])-1:
                if ckt_mat[self.sheet][self.switch_elem[0]][self.switch_elem[1]+1]:
                    self.polrty = [self.switch_elem[0], self.switch_elem[1]+1]
        else:
            for c1 in range(len(sys_branch)):
                if NwRdr.csv_tuple(self.pos_3D) in sys_branch[c1]:
                    if not [self.sheet, self.polrty[0], self.polrty[1]] in sys_branch[c1]:
                        print()
                        print("!"*50)
                        print("ERROR!!! Switch polarity should be in the same branch as the switch. \
Check switch at {} in sheet {}".format(self.pos, self.sheet_name))
                        print("!"*50)
                        print()
                        raise CktEx.PolarityError

        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        switch_params.append("Negative polarity towards (cell) = %s" %NwRdr.csv_element_2D(self.polrty))
        switch_params.append("Name of control signal = %s" %self.control_tag[0])
        x_list.append(switch_params)

        return



    def get_values(self, x_list, ckt_mat):
        """ Takes the parameter from the spreadsheet."""
        self.switch_level = float(x_list[0].split("=")[1])
        # Choosing 1 micro Amp as the leakage current that
        # is drawn by the switch in off state.
        self.resistor_off = self.switch_level/1.0e-6
        self.resistor = self.resistor_off

        switch_polrty = x_list[1].split("=")[1]

        # Convert the human readable form of cell
        # to [row, column] form
        while switch_polrty[0]==" ":
            switch_polrty = switch_polrty[1:]

        self.polrty = NwRdr.csv_tuple_2D(switch_polrty)
        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        if not ckt_mat[self.sheet][self.polrty[0]][self.polrty[1]]:
            print("Polarity incorrect. Branch does not exist at {} in sheet {}".format(
                NwRdr.csv_element(self.polrty), self.sheet_name
            ))
            raise CktEx.PolarityError

        self.control_tag[0] = x_list[2].split("=")[1]
        while self.control_tag[0][0]==" ":
            self.control_tag[0] = self.control_tag[0][1:]

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1
                if sys_branches[c1].index(self.polrty_3D)>sys_branches[c1].index(NwRdr.csv_tuple(self.pos_3D)):
                    self.component_branch_dir = 1.0
                else:
                    self.component_branch_dir = -1.0

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix A in E.dx/dt=Ax+Bu will be updated by the
        resistor value of the switch.
        """

        for c1 in range(len(sys_loops)):
            for c2 in range(c1, len(sys_loops)):
                # Updating the elements depending
                # on the sense of the loops (aiding or opposing)
                for c3 in range(len(sys_loops[c1][c2])):
                    # Check if current source position is there in the loop.
                    if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c2][c3]:
                        # Add current source series resistor
                        # if branch is in forward direction
                        if sys_loops[c1][c2][c3][-1]=="forward":
                            mat_a.data[c1][c2] += self.resistor
                        else:
                            # Else subtract if branch is in reverse direction
                            mat_a.data[c1][c2] -= self.resistor
                        # Because the matrices are symmetric
                        mat_a.data[c2][c1] = mat_a.data[c1][c2]

                        # If the positive polarity appears before the voltage position
                        # it means as per KVL, we are moving from +ve to -ve
                        # and so the voltage will be taken negative
                        if sys_loops[c1][c1][c2].index(self.polrty)>sys_loops[c1][c1][c2].index(NwRdr.csv_tuple(self.pos)):
                            if sys_loops[c1][c1][c2][-1]=="forward":
                                mat_b.data[c1][source_list.index(self.pos)] = -1.0
                            else:
                                mat_b.data[c1][source_list.index(self.pos)] = 1.0
                        else:
                            if sys_loops[c1][c1][c2][-1]=="forward":
                                mat_b.data[c1][source_list.index(self.pos)] = 1.0
                            else:
                                mat_b.data[c1][source_list.index(self.pos)] = -1.0

        return



    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        Update the resistor info of the switch
        to the branch list.
        """

        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            sys_branch[-1][0][0] += self.resistor

        # For the switch forward voltage drop.
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            if sys_branch.index(self.polrty_3D)>sys_branch.index(NwRdr.csv_tuple(self.pos_3D)):
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 0.0
            else:
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 0.0

        if self.status=="on":
            mat_u.data[source_list.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0
        else:
            mat_u.data[source_list.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0

        return



    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        """
        The switch forward drop voltage is updated
        in the matrix u in E.dx/dt=Ax+Bu.
        """

        # The switch does not contain voltage when on.
        if self.status=="on":
            mat_u.data[source_lst.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0
        else:
            mat_u.data[source_lst.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0

        return



    def update_val_old(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        This function calculates the actual current in the
        switch branch. With this, the branch voltage is found
        with respect to the existing switch resistance. The switch
        voltage is then used to decide the turn on condition.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
            self.current = sys_branches[branch_pos][-1][2]
        else:
            self.current = -sys_branches[branch_pos][-1][2]

        self.voltage = self.current*self.resistor

        # Identifying the position of the switch branch
        # to generate events.
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        # Switch will turn on when it is forward biased
        # and it is gated on.
        if self.control_values[0]>=1.0 and self.voltage>1.0:
            if self.status=="off":
                sys_events[branch_pos] = "hard"
                self.status = "on"

        # Switch will turn off when gated off or
        # when current becomes negative.
        # If the current becomes negative, it is a soft turn off
        if self.current<0.0:
            if self.status=="on":
                sys_events[branch_pos] = "yes"
                self.status = "off"

        # If the switch turns off due to a gate signal
        # it is a hard turn off
        if self.control_values[0]==0.0:
            if self.status=="on":
                sys_events[branch_pos] = "hard"
                self.status = "off"

        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return



    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        This function calculates the actual current in the
        switch branch. With this, the branch voltage is found
        with respect to the existing switch resistance. The switch
        voltage is then used to decide the turn on condition.
        """

        self.current = self.component_branch_dir*sys_branches[self.component_branch_pos][-1][2]
        self.voltage = self.current*self.resistor

        # Switch will turn on when it is forward biased
        # and it is gated on.
        if self.control_values[0]>=1.0 and self.voltage>1.0:
            if self.status=="off":
                sys_events[self.component_branch_pos] = "hard"
                self.status = "on"

        # Switch will turn off when gated off or
        # when current becomes negative.
        # If the current becomes negative, it is a soft turn off
        if self.current<0.0:
            if self.status=="on":
                sys_events[self.component_branch_pos] = "yes"
                self.status = "off"

        # If the switch turns off due to a gate signal
        # it is a hard turn off
        if self.control_values[0]==0.0:
            if self.status=="on":
                sys_events[self.component_branch_pos] = "hard"
                self.status = "off"

        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return



    def determine_state_old(self, br_currents, sys_branches, sys_events):
        """
        Determines the state of the switch following an event
        where the continuity of current through an inductor is
        about to be broken. This can only check if the switch should
        turn off. Turn on is only decided by the update_value method.
        """

        # Mark the position of the switch in sys_branches
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        # If the current direction is reverse, switch can never conduct
        if br_currents[branch_pos]<0.0:
            if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
                if self.status=="on":
                    sys_events[branch_pos] = "yes"
                self.status = "off"

        if br_currents[branch_pos]>0.0:
            if sys_branches[branch_pos].index(self.polrty)<sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
                if self.status=="on":
                    sys_events[branch_pos] = "yes"
                self.status = "off"

        # Update the value of resistance
        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return


    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        """
        Determines the state of the switch following an event
        where the continuity of current through an inductor is
        about to be broken. This can only check if the switch should
        turn off. Turn on is only decided by the update_value method.
        """

        self.current = self.component_branch_dir*br_currents[self.component_branch_pos]
        self.voltage = self.current*self.resistor

        # Switch will turn on when it is forward biased
        # and it is gated on.
        if self.control_values[0]>=1.0 and self.voltage>1.0:
            if self.status=="off":
                sys_events[self.component_branch_pos] = "hard"
                self.status = "on"

        # Switch will turn off when gated off or
        # when current becomes negative.
        # If the current becomes negative, it is a soft turn off
        if self.current<0.0:
            if self.status=="on":
                sys_events[self.component_branch_pos] = "yes"
                self.status = "off"

        # If the switch turns off due to a gate signal
        # it is a hard turn off
        if self.control_values[0]==0.0:
            if self.status=="on":
                sys_events[self.component_branch_pos] = "hard"
                self.status = "off"

        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return



    def determine_state(self, br_currents, sys_branches, sys_events):
        """
        Determines the state of the switch following an event
        where the continuity of current through an inductor is
        about to be broken. This can only check if the switch should
        turn off. Turn on is only decided by the update_value method.
        """

        # If the current direction is reverse, switch can never conduct
        if br_currents[self.component_branch_pos]*self.component_branch_dir<0.0:
            #if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
            if self.status=="on":
                sys_events[self.component_branch_pos] = "yes"
            self.status = "off"

        # Update the value of resistance
        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return


class Thyristor:
    """
    Thyristor class. Contains functions to initiliaze
    the thyristor according to name tag, unique cell position,
    update system matrix on each iteration.
    """

    def __init__(self, thyristor_index, thyristor_pos, thyristor_tag, nw_input):
        """
        Constructor to initialize value.
        Also, takes in the identifiers -
        index (serial number), cell position and tag.
        """
        self.type="Thyristor"
        self.number = thyristor_index
        self.pos_3D = thyristor_pos
        self.sheet = NwRdr.csv_tuple(thyristor_pos)[0]
        self.pos = NwRdr.csv_element_2D(NwRdr.csv_tuple(thyristor_pos)[1:])
        self.tag = thyristor_tag
        self.sheet_name = nw_input[self.sheet] + ".csv"
        self.has_voltage = "yes"
        self.thyristor_level = 120.0
        self.is_meter = "no"
        self.has_control = "yes"
        self.current = 0.0
        self.voltage = 0.0
        self.polrty = [-1, -1]
        self.resistor_on = 0.01
        self.status = "off"
        self.control_tag = ["Control"]
        self.control_values = [0.0]
        self.component_banch_pos = 0
        self.component_branch_dir = 1.0

        return


    def display(self):
        """
        Displays info about the component.
        """
        print("Thyristor is {} located at {} with negative polarity towards {} in sheet {}".format(
            self.tag, self.pos, NwRdr.csv_element_2D(self.polrty), self.sheet_name
        ))

        return



    def ask_values(self, x_list, ckt_mat, sys_branch):
        """
        Writes the values needed to the spreadsheet.
        """
        thyristor_params = ["Thyristor"]
        thyristor_params.append(self.tag)
        thyristor_params.append(self.pos)
        thyristor_params.append("Voltage level (V) = %f" %self.thyristor_level)

        self.thyristor_elem = NwRdr.csv_tuple_2D(self.pos)

        if self.polrty==[-1, -1]:
            # Looking for a default value of polarity
            # in the neighbouring cells

            if self.thyristor_elem[0]>0:
                if ckt_mat[self.sheet][self.thyristor_elem[0]-1][self.thyristor_elem[1]]:
                    self.polrty = [self.thyristor_elem[0]-1, self.thyristor_elem[1]]
            if self.thyristor_elem[1]>0:
                if ckt_mat[self.sheet][self.thyristor_elem[0]][self.thyristor_elem[1]-1]:
                    self.polrty = [self.thyristor_elem[0], self.thyristor_elem[1]-1]

            if self.thyristor_elem[0]<len(ckt_mat[self.sheet])-1:
                if ckt_mat[self.sheet][self.thyristor_elem[0]+1][self.thyristor_elem[1]]:
                    self.polrty = [self.thyristor_elem[0]+1, self.thyristor_elem[1]]
            if self.thyristor_elem[1]<len(ckt_mat[self.sheet][0])-1:
                if ckt_mat[self.sheet][self.thyristor_elem[0]][self.thyristor_elem[1]+1]:
                    self.polrty = [self.thyristor_elem[0], self.thyristor_elem[1]+1]
        else:
            for c1 in range(len(sys_branch)):
                if NwRdr.csv_tuple(self.pos_3D) in sys_branch[c1]:
                    if not [self.sheet, self.polrty[0], self.polrty[1]] in sys_branch[c1]:
                        print()
                        print("!"*50)
                        print("ERROR!!! Thyristor polarity should be in the same branch as the thyristor. \
Check thyristor at {} in sheet {}".format(self.pos, self.sheet_name))
                        print("!"*50)
                        print()
                        raise CktEx.PolarityError

        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        thyristor_params.append("Negative polarity towards (cell) = %s" %NwRdr.csv_element_2D(self.polrty))
        thyristor_params.append("Name of control signal = %s" %self.control_tag[0])
        x_list.append(thyristor_params)

        return



    def get_values(self, x_list, ckt_mat):
        """ Takes the parameter from the spreadsheet."""
        self.thyristor_level = float(x_list[0].split("=")[1])
        # Choosing 1 micro Amp as the leakage current that
        # is drawn by the thyristor in off state.
        self.resistor_off = self.thyristor_level/1.0e-6
        self.resistor = self.resistor_off

        thyristor_polrty = x_list[1].split("=")[1]

        # Convert the human readable form of cell
        # to [row, column] form
        while thyristor_polrty[0]==" ":
            thyristor_polrty = thyristor_polrty[1:]

        self.polrty = NwRdr.csv_tuple_2D(thyristor_polrty)
        self.polrty_3D = [self.sheet, self.polrty[0], self.polrty[1]]

        if not ckt_mat[self.sheet][self.polrty[0]][self.polrty[1]]:
            print("Polarity incorrect. Branch does not exist at {} in sheet {}".format(
                NwRdr.csv_element(self.polrty), self.sheet_name
            ))
            raise CktEx.PolarityError

        self.control_tag[0] = x_list[2].split("=")[1]
        while self.control_tag[0][0]==" ":
            self.control_tag[0] = self.control_tag[0][1:]

        return


    def determine_branch(self, sys_branches):
        """
        Determines which branch the component is found in.
        """
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos_3D) in sys_branches[c1]:
                self.component_branch_pos = c1
                if sys_branches[c1].index(self.polrty_3D)>sys_branches[c1].index(NwRdr.csv_tuple(self.pos_3D)):
                    self.component_branch_dir = 1.0
                else:
                    self.component_branch_dir = -1.0

        return


    def transfer_to_sys(self, sys_loops, mat_e, mat_a, mat_b, mat_u, source_list):
        """
        The matrix A in E.dx/dt=Ax+Bu will be updated by the
        resistor value of the thyristor.
        """

        for c1 in range(len(sys_loops)):
            for c2 in range(c1, len(sys_loops)):
                # Updating the elements depending
                # on the sense of the loops (aiding or opposing)
                for c3 in range(len(sys_loops[c1][c2])):
                    # Check if current source position is there in the loop.
                    if NwRdr.csv_tuple(self.pos) in sys_loops[c1][c2][c3]:
                        # Add current source series resistor
                        # if branch is in forward direction
                        if sys_loops[c1][c2][c3][-1]=="forward":
                            mat_a.data[c1][c2] += self.resistor
                        else:
                            # Else subtract if branch is in reverse direction
                            mat_a.data[c1][c2] -= self.resistor
                        # Because the matrices are symmetric
                        mat_a.data[c2][c1] = mat_a.data[c1][c2]

                        # If the positive polarity appears before the voltage position
                        # it means as per KVL, we are moving from +ve to -ve
                        # and so the voltage will be taken negative
                        if sys_loops[c1][c1][c2].index(self.polrty)>sys_loops[c1][c1][c2].index(NwRdr.csv_tuple(self.pos)):
                            if sys_loops[c1][c1][c2][-1]=="forward":
                                mat_b.data[c1][source_list.index(self.pos)] = -1.0
                            else:
                                mat_b.data[c1][source_list.index(self.pos)] = 1.0
                        else:
                            if sys_loops[c1][c1][c2][-1]=="forward":
                                mat_b.data[c1][source_list.index(self.pos)] = 1.0
                            else:
                                mat_b.data[c1][source_list.index(self.pos)] = -1.0

        return



    def transfer_to_branch(self, sys_branch, source_list,  mat_u):
        """
        Update the resistor info of the thyristor
        to the branch list.
        """

        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            sys_branch[-1][0][0] += self.resistor

        # For the thyristor forward voltage drop.
        if NwRdr.csv_tuple(self.pos_3D) in sys_branch:
            if sys_branch.index(self.polrty_3D)>sys_branch.index(NwRdr.csv_tuple(self.pos_3D)):
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 0.0
            else:
                sys_branch[-1][1][source_list.index(self.pos_3D)] = 0.0

        if self.status=="on":
            mat_u.data[source_list.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0
        else:
            mat_u.data[source_list.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0

        return



    def generate_val(self, source_lst, mat_e, mat_a, mat_b, mat_u, t, dt):
        """
        The thyristor forward drop voltage is updated
        in the matrix u in E.dx/dt=Ax+Bu.
        """

        # The thyristor does not contain voltage when on.
        if self.status=="on":
            mat_u.data[source_lst.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0
        else:
            mat_u.data[source_lst.index(self.pos_3D)][0] = 0.0
            self.voltage = 0.0

        return



    def update_val_old(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        This function calculates the actual current in the
        thyristor branch. With this, the branch voltage is found
        with respect to the existing thyristor resistance. The thyristor
        voltage is then used to decide the turn on condition.
        """

        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
            self.current = sys_branches[branch_pos][-1][2]
        else:
            self.current = -sys_branches[branch_pos][-1][2]

        self.voltage = self.current*self.resistor

        # Identifying the position of the thyristor branch
        # to generate events.
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        # Thyrsistor will turn on when it is forward biased
        # and it is gated on.
        if self.control_values[0]>=1.0 and self.voltage>1.0:
            if self.status=="off":
                sys_events[branch_pos] = "hard"
                self.status = "on"

        # Thyrsistor will turn off when gated off or
        # when current becomes negative.
        # If the current becomes negative, it is a soft turn off
        if self.current<0.0:
            if self.status=="on":
                sys_events[branch_pos] = "yes"
                self.status = "off"

        # If the thyristor turns off due to a gate signal
        # it is a hard turn off
        if self.control_values[0]==0.0:
            if self.status=="on":
                sys_events[branch_pos] = "hard"
                self.status = "off"

        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return



    def update_val(self, sys_loop_map, lbyr_ratio, mat_e, mat_a, mat_b, state_vec, mat_u, sys_branches, sys_events):
        """
        This function calculates the actual current in the
        thyristor branch. With this, the branch voltage is found
        with respect to the existing thyristor resistance. The thyristor
        voltage is then used to decide the turn on condition.
        """

        self.current = self.component_branch_dir*sys_branches[self.component_branch_pos][-1][2]
        self.voltage = self.current*self.resistor

        # Thyristor will turn on when it is forward biased
        # and it is gated on.
        if self.control_values[0]>=1.0 and self.voltage>1.0:
            if self.status=="off":
                sys_events[self.component_branch_pos] = "hard"
                self.status = "on"

        # Thyristor will turn off when gated off or
        # when current becomes negative.
        # If the current becomes negative, it is a soft turn off
        if self.current<0.0:
            if self.status=="on":
                sys_events[self.component_branch_pos] = "yes"
                self.status = "off"

        # If the thyristor turns off due to a gate signal
        # it is a hard turn off
        # THYRISTOR DOES NOT HAVE A HARD TURN OFF
        # if self.control_values[0]==0.0:
        #     if self.status=="on":
        #         sys_events[self.component_branch_pos] = "hard"
        #         self.status = "off"

        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return



    def determine_state_old(self, br_currents, sys_branches, sys_events):
        """
        Determines the state of the thyristor following an event
        where the continuity of current through an inductor is
        about to be broken. This can only check if the thyristor should
        turn off. Turn on is only decided by the update_value method.
        """

        # Mark the position of the thyristor in sys_branches
        for c1 in range(len(sys_branches)):
            if NwRdr.csv_tuple(self.pos) in sys_branches[c1]:
                branch_pos = c1

        # If the current direction is reverse, thyristor can never conduct
        if br_currents[branch_pos]<0.0:
            if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
                if self.status=="on":
                    sys_events[branch_pos] = "yes"
                self.status = "off"

        if br_currents[branch_pos]>0.0:
            if sys_branches[branch_pos].index(self.polrty)<sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
                if self.status=="on":
                    sys_events[branch_pos] = "yes"
                self.status = "off"

        # Update the value of resistance
        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return


    def pre_determine_state(self, br_currents, sys_branches, sys_events):
        """
        Determines the state of the thyristor following an event
        where the continuity of current through an inductor is
        about to be broken. This can only check if the thyristor should
        turn off. Turn on is only decided by the update_value method.
        """

        self.current = self.component_branch_dir*br_currents[self.component_branch_pos]
        self.voltage = self.current*self.resistor

        # Thyristor will turn on when it is forward biased
        # and it is gated on.
        if self.control_values[0]>=1.0 and self.voltage>1.0:
            if self.status=="off":
                sys_events[self.component_branch_pos] = "hard"
                self.status = "on"

        # Thyrsistor will turn off when gated off or
        # when current becomes negative.
        # If the current becomes negative, it is a soft turn off
        if self.current<0.0:
            if self.status=="on":
                sys_events[self.component_branch_pos] = "yes"
                self.status = "off"

        # If the thyristor turns off due to a gate signal
        # it is a hard turn off
        # THYRISTOR CANNOT DO A HARD TURN OFF
        # if self.control_values[0]==0.0:
        #     if self.status=="on":
        #         sys_events[self.component_branch_pos] = "hard"
        #         self.status = "off"

        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return



    def determine_state(self, br_currents, sys_branches, sys_events):
        """
        Determines the state of the thyristor following an event
        where the continuity of current through an inductor is
        about to be broken. This can only check if the thyristor should
        turn off. Turn on is only decided by the update_value method.
        """

        # If the current direction is reverse, thyristor can never conduct
        if br_currents[self.component_branch_pos]*self.component_branch_dir<0.0:
            #if sys_branches[branch_pos].index(self.polrty)>sys_branches[branch_pos].index(NwRdr.csv_tuple(self.pos)):
            if self.status=="on":
                sys_events[self.component_branch_pos] = "yes"
            self.status = "off"

        # Update the value of resistance
        if self.status=="off":
            self.resistor = self.resistor_off
        else:
            self.resistor = self.resistor_on

        return



nonlinear_freewheel_components = ["Switch", "Diode", "Thyristor"]

component_list = {"resistor":Resistor, "inductor":Inductor, "capacitor":Capacitor, \
        "voltagesource":Voltage_Source, "ammeter":Ammeter, "voltmeter":Voltmeter, \
        "currentsource":Current_Source, "controlledvoltagesource":Controlled_Voltage_Source, \
        "diode":Diode, "switch":Switch, "variableresistor":Variable_Resistor, "variableinductor":Variable_Inductor, \
        "thyristor": Thyristor}
