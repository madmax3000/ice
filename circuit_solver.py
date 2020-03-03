#! /usr/bin/env python

import sys
import math
import network_reader as NwRdr
import solver as Slv
import matrix
import time
import circuit_exceptions as CktEx
import gv
''' this program has changes made by john jose to incorprate and 
    automation for the parameter search , respective changes which was made are
    commented'''

def main():

    # The parameters of the simulation are in the circuit_inputs.csv file.
    # A blank file with defaults are created if nothing is found in the
    # folder.
    
    ckt_param_exists = "no"
    while ckt_param_exists=="no":
        try:
            ckt_param_file = open("circuit_inputs.csv", "r")
        except:
            # If there is no circuit_inputs.csv file in the directory, create it.
            ckt_param_file = open("circuit_inputs.csv", "w")


            ckt_param_file.write("Name of the circuit file")
            ckt_param_file.write(", ")
            ckt_param_file.write("Change the file name to the name of the circuit file. The file has to be .csv file so do not use another extension.")
            ckt_param_file.write(", ")
            ckt_param_file.write("sample_ckt.csv")
            ckt_param_file.write("\n")


            ckt_param_file.write("Time duration of simulation")
            ckt_param_file.write(", ")
            ckt_param_file.write("This is the time in seconds.")
            ckt_param_file.write(", ")
            ckt_param_file.write("1")
            ckt_param_file.write("\n")


            ckt_param_file.write("Time step of the simulation")
            ckt_param_file.write(", ")
            ckt_param_file.write("Recommened to be less than 10 microseconds for accuracy.")
            ckt_param_file.write(", ")
            ckt_param_file.write("1.0e-6")
            ckt_param_file.write("\n")


            ckt_param_file.write("Time step of data storage")
            ckt_param_file.write(", ")
            ckt_param_file.write("This is the time step with data is stored and has to be equal to or greater than the simulation time step.")
            ckt_param_file.write(", ")
            ckt_param_file.write("10.0e-6")
            ckt_param_file.write("\n")


            ckt_param_file.write("Name of the data storage file")
            ckt_param_file.write(", ")
            ckt_param_file.write("This is where all meter data and control signals will be stored.")
            ckt_param_file.write(", ")
            ckt_param_file.write("ckt_output.dat")
            ckt_param_file.write("\n")


            ckt_param_file.write("Name of control files")
            ckt_param_file.write(", ")
            ckt_param_file.write("Add or remove as many control files as needed in separate columns.")
            ckt_param_file.write(", ")
            ckt_param_file.write("control1.py")
            ckt_param_file.write(", ")
            ckt_param_file.write("control2.py")
            ckt_param_file.write(", ")
            ckt_param_file.write("control3.py")
            ckt_param_file.write("\n")


            ckt_param_file.write("Split the output file?")
            ckt_param_file.write(", ")
            ckt_param_file.write("Say yes if you think the data file is too large and plotting is taking too much time or else say no.")
            ckt_param_file.write(", ")
            ckt_param_file.write("Yes")
            ckt_param_file.write("\n")


            ckt_param_file.write("Length of time windows")
            ckt_param_file.write(", ")
            ckt_param_file.write("There should be at least two intervals for storage.")
            ckt_param_file.write(", ")
            ckt_param_file.write("")
            ckt_param_file.write("\n")


            ckt_param_file.close()

            # Wait for the user to enter parameters before
            # reading the circuit_inputs.csv file.
            cont_ans="n"
            #cont_ans="y"
            while cont_ans.lower()!="y":
                print("This appears to be a new project.")
                print("A sample circuit_inputs.csv file has been created.")
                print("Enter simulation parameters in file circuit_inputs.csv.")
                cont_ans = input("When done, close the file and press y and enter to continue -> ")

            ckt_param_exists = "yes"

        
        if gv.c == 0:
            # If a circuit_inputs.csv file exists, ask the user to update it and continue.

            # Wait for the user to enter parameters before
            # reading the circuit_inputs.csv file.
            cont_ans = "n"
            #cont_ans = "y"
            #if it is first time with the help of global variable the program identifies and display it.
            while cont_ans.lower()!="y":
                print("A circuit_inputs.csv file has been found.")
                print("Check whether the simulation parameters have changed and if so enter new parameters in file circuit_inputs.csv.")
                cont_ans = input("When done, close the file and press y and enter to continue -> ")

            ckt_param_exists = "yes"
            ckt_param_file.close()
        if gv.c ==1:
            ckt_param_exists = "yes" #if the optimization algorithum runs there is no futher questioning and program skips here.
            break


    # Read the circuit_inputs.csv file and perform error checking for each parameter.
    if ckt_param_exists=="yes":

        ckt_param_file = open("circuit_inputs.csv", "r")

        lines_in_input_file = []
        for line in ckt_param_file:
            lines_in_input_file.append(line)


        ckt_input_line = lines_in_input_file[0]
        ckt_input_fields = ckt_input_line.split(",")
        nw_layout = ckt_input_fields[2:]
        nw_input = []
        for c1 in range(len(nw_layout)):
            if nw_layout[c1]:
                while nw_layout[c1][0]==" ":
                    nw_layout[c1] = nw_layout[c1][1:]
                    if not nw_layout[c1]:
                        break
            if nw_layout[c1]:
                while nw_layout[c1][-1]==" ":
                    nw_layout[c1] = nw_layout[c1][:-1]
                    if not nw_layout[c1]:
                        break
            if nw_layout[c1]:
                while nw_layout[c1][0]=="\r" or nw_layout[c1][0]=="\n":
                    nw_layout[c1] = nw_layout[c1][1:]
                    if not nw_layout[c1]:
                        break
            if nw_layout[c1]:
                while nw_layout[c1][-1]=="\r" or nw_layout[c1][-1]=="\n":
                    nw_layout[c1] = nw_layout[c1][:-1]
                    if not nw_layout[c1]:
                        break
            if nw_layout[c1]:
                if nw_layout[c1][-1]=="\n" or nw_layout[c1][-1]=="\r":
                    nw_layout[c1] = nw_layout[c1][:-1]
                    if not nw_layout[c1]:
                        break

            nw_input.append(nw_layout[c1].split(".csv")[0])



        ckt_input_line = lines_in_input_file[1]
        ckt_input_fields = ckt_input_line.split(",")
        t_limit = ckt_input_fields[2]
        while t_limit[0]==" ":
            t_limit = t_limit[1:]
            if not t_limit:
                break
        while t_limit[-1]==" ":
            t_limit = t_limit[:-1]
            if not t_limit:
                break
        while t_limit[-1]=="\n" or t_limit[-1]=="\r":
            t_limit = t_limit[:-1]
            if not t_limit:
                break

        try:
            t_limit = float(t_limit)
        except:
            print("Error. Invalid time duration. Check row 2 of circuit_inputs.csv.")
            print()
            sys.exit(1)
        else:
            if t_limit>0.0:
                pass
            else:
                print("Error. Invalid time duration. Check row 2 of circuit_inputs.csv.")
                print()
                sys.exit(1)


        ckt_input_line = lines_in_input_file[2]
        ckt_input_fields = ckt_input_line.split(",")
        dt = ckt_input_fields[2]
        while dt[0]==" ":
            dt = dt[1:]
            if not dt:
                break
        while dt[-1]==" ":
            dt = dt[:-1]
            if not dt:
                break
        while dt[-1]=="\n" or dt[-1]=="\r":
            dt = dt[:-1]
            if not dt:
                break

        try:
            dt = float(dt)
        except:
            print("Error. Invalid time step. Check row 3 of circuit_inputs.csv.")
            print
            sys.exit(1)
        else:
            if dt>0.0:
                pass
            else:
                print("Error. Invalid time step. Check row 3 of circuit_inputs.csv.")
                print()
                sys.exit(1)


        ckt_input_line = lines_in_input_file[3]
        ckt_input_fields = ckt_input_line.split(",")
        dt_store = ckt_input_fields[2]
        while dt_store[0]==" ":
            dt_store = dt_store[1:]
            if not dt_store:
                break
        while dt_store[-1]==" ":
            dt_store = dt_store[:-1]
            if not dt_store:
                break
        while dt_store[-1]=="\n" or dt_store[-1]=="\r":
            dt_store = dt_store[:-1]
            if not dt_store:
                break

        try:
            dt_store = float(dt_store)
        except:
            print("Error. Invalid time storage step. Check row 4 of circuit_inputs.csv.")
            print()
            sys.exit(1)
        else:
            if dt_store>=dt:
                pass
            else:
                print("Error. Invalid time storage step. Check row 4 of circuit_inputs.csv.")
                print()
                sys.exit(1)



        ckt_input_line = lines_in_input_file[4]
        ckt_input_fields = ckt_input_line.split(",")
        op_dat_file = ckt_input_fields[2]
        while op_dat_file[0]==" ":
            op_dat_file = op_dat_file[1:]
            if not op_dat_file:
                break
        while op_dat_file[-1]==" ":
            op_dat_file = op_dat_file[:-1]
            if not op_dat_file:
                break
        while op_dat_file[-1]=="\n" or op_dat_file[-1]=="\r":
            op_dat_file = op_dat_file[:-1]
            if not op_dat_file:
                break



        ckt_input_line = lines_in_input_file[5]
        ckt_input_fields = ckt_input_line.split(",")
        control_files = ckt_input_fields[2:]
        for c1 in range(len(control_files)):
            if control_files[c1]:
                while control_files[c1][0]==" ":
                    control_files[c1] = control_files[c1][1:]
                    if not control_files[c1]:
                        break
                while control_files[c1][-1]==" ":
                    control_files[c1] = control_files[c1][:-1]
                    if not control_files[c1]:
                        break
                while control_files[c1][-1]=="\n" or control_files[c1][-1]=="\r":
                    control_files[c1] = control_files[c1][:-1]
                    if not control_files[c1]:
                        break

            if control_files[c1]!="" and control_files[c1]!=" ":
                extract_filename = control_files[c1].split(".py")
                if not len(extract_filename)==2:
                    print("Error. Control file {} is not a .py file.".format(control_files[c1]))
                    sys.exit(1)
                control_files[c1] = extract_filename[0]

        for c1 in range(len(control_files)-1, -1, -1):
            if not control_files[c1]:
                del control_files[c1]


        ckt_input_line = lines_in_input_file[6]
        ckt_input_fields = ckt_input_line.split(",")
        window_exist = ckt_input_fields[2]
        while window_exist[0]==" ":
            window_exist = window_exist[1:]
            if not window_exist:
                break
        while window_exist[-1]==" ":
            window_exist = window_exist[:-1]
            if not window_exist:
                break
        while window_exist[-1]=="\n" or window_exist[-1]=="\r":
            window_exist = window_exist[:-1]
            if not window_exist:
                break

        if window_exist.lower()=="yes" or window_exist.lower()=="no":
            pass
        else:
            print("Error. Invalid response for data storage split up. Check row 7 of circuit_inputs.csv.")
            print()
            sys.exit(1)


        if window_exist.lower()=="yes":
            ckt_input_line = lines_in_input_file[7]
            ckt_input_fields = ckt_input_line.split(",")
            t_window = ckt_input_fields[2]
            while t_window[0]==" ":
                t_window = t_window[1:]
                if not t_window:
                    break
            while t_window[-1]==" ":
                t_window = t_window[:-1]
                if not t_window:
                    break
            while t_window[-1]=="\n" or t_window[-1]=="\r":
                t_window = t_window[:-1]
                if not t_window:
                    break

            try:
                t_window = float(t_window)
            except:
                print("Error. Invalid time window. Check row 8 of circuit_inputs.csv.")
                print()
                sys.exit(1)
            else:
                if t_window:
                    if t_limit/t_window>=2:
                        t_split_file = []
                        t_split = 0.0
                        while t_split<t_limit:
                            t_split_file.append(t_split)
                            t_split += t_window

                        t_split_file.append(t_limit)

                else:
                    print("Error. Invalid time window. Check row 8 of circuit_inputs.csv.")
                    print()
                    sys.exit(1)

        else:
            t_split_file = [0.0, t_limit]

        if len(t_split_file)>2:
            f = []
            file_name_list = []
            op_file_name = op_dat_file.split(".")
            if len(op_file_name)>1:
                op_file_ext = op_dat_file.split(".")[1]
                op_file_name = op_file_name[0]
            else:
                op_file_name = op_dat_file
                op_file_ext = ""

            for c1 in range(1, len(t_split_file)):
                file_name_list.append(op_file_name + str(c1) + "." + op_file_ext)

        else:
            file_name_list = [op_dat_file]

        # Check if the output file exists in the directory
        for file_item in file_name_list:
            try:
                output_file = open(file_item, "r")
            except:
                pass
            else:
                print(gv.c)
                if gv.c == 1:              #checks if the run is a simulation run of optimization run
                    cont_ans = "n"
                if gv.c == 0:
                    cont_ans = "p"       #similar program skipping occcurs here.
                while cont_ans.lower()=="p":
                    print("Output data file {} exists from a previous \
simulation.".format(file_item))
                    cont_ans = input("Would you like to abort now and make a backup or change the \
name of the output data file in circuit_inputs.csv? (Y/N) ")

                    if cont_ans.lower()=="y" or cont_ans.lower()=="n":
                        break

                if cont_ans.lower()=="y":
                    print()
                    print()
                    sys.exit(1)
                else:
                    print()
                    print()
                    break


        f = []
        for file_item in file_name_list:
            f.append(open(file_item, "w"))


    for c1 in range(len(nw_layout)-1, -1, -1):
        if nw_layout[c1]=="\n" or nw_layout[c1]=="\r":
            del nw_layout[c1]
            del nw_input[c1]
        if not nw_layout[c1]:
            del nw_layout[c1]
            del nw_input[c1]


    test_ckt = []
    for c1 in range(len(nw_layout)):
        try:
            test_ckt.append(open(nw_layout[c1],"r"))
        except IOError:
            print("File {} cannot be read. Make sure \
file name is correct, and in the same \
folder/directory as circuit_solver.py".format(nw_layout[c1]))
            print()
            sys.exit(1)



    # Read the circuit into tst_mat
    # Also performs a scrubbing of tst_mat
    conn_ckt_mat = []
    for c1 in range(len(test_ckt)):
        conn_ckt_mat.append(NwRdr.csv_reader(test_ckt[c1]))


    # Making a list of the type of components in the
    # circuit.
    components_found, component_objects = \
            NwRdr.determine_circuit_components(conn_ckt_mat, nw_input)


    # Segregating the elements in the circuit as those
    # having source voltages, meters and those that can be
    # controlled.
    bundled_list_of_elements = NwRdr.classify_components(components_found, component_objects)

    source_list = bundled_list_of_elements[0]
    meter_list = bundled_list_of_elements[1]
    controlled_elements = bundled_list_of_elements[2]


    # Make lists of nodes and branches in the circuit.
    node_list, branch_map = NwRdr.determine_nodes_branches(conn_ckt_mat, nw_input)

    # Make a list of all the loops in the circuit.
    loop_list, loop_branches = NwRdr.determine_loops(conn_ckt_mat, node_list, branch_map)

    # Convert the above list of loops as segments of branches
    # while branch_params lists out the branch segments with
    # their parameters as the last element
    system_loops, branch_params = NwRdr.update_branches_loops(loop_branches, source_list)


    # Make lists of all the nodes connected together by
    # empty branches.
    shortnode_list, shortbranch_list = NwRdr.delete_empty_branches(system_loops, branch_params, node_list, component_objects)
#    NwRdr.delete_empty_branches_new(system_loops,  branch_params,  node_list,  component_objects)


    # Make a list which has the components of a branch
    # as every element of the list.
    components_in_branch = []
    for c1 in range(len(branch_params)):
        current_branch_vector = []
        for c2 in range(len(branch_params[c1][:-1])):
            try:
                comp_pos = NwRdr.csv_element(branch_params[c1][c2])
                component_objects[comp_pos]
            except:
                pass
            else:
                current_branch_vector.append(comp_pos)

        components_in_branch.append(current_branch_vector)


    # Branch currents for nodal analysis
    branch_currents = []
    for c1 in range(len(branch_params)):
        branch_currents.append(0.0)


    # This is a list of branches which are only
    # in stiff loops. This comes in handy to recalculate
    # currents through branches that have recently become
    # stiff.
    branches_in_stiff_loops = []
    for c1 in range(len(branch_params)):
        branches_in_stiff_loops.append("yes")

    # Stiff ratio indicates whether a branch
    # is stiff.
    stiff_ratio = []
    for c1 in range(len(branch_params)):
        stiff_ratio.append("no")

    # An event vector which corresponds to every branch
    # in the circuit. An event is generated if any element
    # in the branch changes. Intitally, an event is generated
    # for each branch in the circuit.
    branch_events = []
    for c1 in range(len(branch_params)):
        branch_events.append("yes")

    # Saving the previous set of branch events
    # to look for device state changes.
    branch_events_prev = []
    for c1 in range(len(branch_params)):
        branch_events_prev.append("no")


    # Mark which loops are stiff.
    loop_stiff_info = []
    for c1 in range(len(system_loops)):
        loop_stiff_info.append("no")


    # Node voltages for nodal analysis
    node_voltage = []
    for c1 in range(len(node_list)):
        node_voltage.append(0.0)


    # Collect branches into bundles - those with
    # inductances, those with nonlinear elements,
    # those with voltage sources.
    bundled_list_of_branches = NwRdr.classify_branches(branch_params,  component_objects)

    nonlinear_freewheel_branches = bundled_list_of_branches[0]
    inductor_list = bundled_list_of_branches[1][0]
    inductor_stiffness = bundled_list_of_branches[1][1]
    voltmeter_branches = bundled_list_of_branches[2][0]
    voltmeter_voltages = bundled_list_of_branches[2][1]


    # For debugging, lists out a branch as a collection of
    # the elements in the branch.
    branch_tags_in_loops = NwRdr.human_branch_names(branch_params, component_objects)


    # These are lists needed to perform the KCL. Contains
    # all the branches connected at a branch
    kcl_node_list,  abridged_node_voltage,  kcl_branch_map,  \
            branches_in_kcl_nodes,  admittance_matrix,  source_vector = \
            NwRdr.determine_kcl_parameters(branch_params,  node_list,  shortnode_list)


    # These are dictionaries to take snapshops of the system
    # at every event. The system loop map, and loop current
    # calculation information is stored when a new event is
    # detected and is retrieved when the event repeats.
    snap_branch_stiffness = {}
    snap_system_loopmap = {}
    snap_nonstiff_loops = {}
    snap_single_collection_nonstiff = {}
    snap_compute_loops_nonstiff = {}
    snap_loop_map_collection_nonstiff = {}
    snap_single_collection_stiff = {}
    snap_compute_loops_stiff = {}
    snap_loop_map_collection_stiff = {}




    # Initialize the system loop map.
    system_loop_map = []

    # System matrices for the ODE

    system_size = len(loop_branches)

    sys_mat_a = matrix.Matrix(system_size, system_size)
    sys_mat_e = matrix.Matrix(system_size, system_size)
    curr_state_vec = matrix.Matrix(system_size)
    next_state_vec = matrix.Matrix(system_size)

    # These vectors are for the reduced order KVL
    reduced_curr_state = matrix.Matrix(system_size)
    reduced_next_state = matrix.Matrix(system_size)

    if source_list:
        source_size = len(source_list)
        sys_mat_b = matrix.Matrix(system_size, len(source_list))
        sys_mat_u = matrix.Matrix(len(source_list))

    else:
        source_size = 1
        sys_mat_b = matrix.Matrix(system_size)
        sys_mat_u = 0.0



    # 5th order Runge Kutta method
    ##ode_k1=matrix.Matrix(system_size)
    ##ode_k2=matrix.Matrix(system_size)
    ##ode_k3=matrix.Matrix(system_size)
    ##ode_k4=matrix.Matrix(system_size)
    ##ode_k5=matrix.Matrix(system_size)
    ##ode_k6=matrix.Matrix(system_size)
    ##ode_dbydt=matrix.Matrix(system_size)
    ##ode_var=[ode_k1, ode_k2, ode_k3, ode_k4, ode_k5, ode_k6, ode_dbydt]

    # 4th order Runge Kutta method
    ode_k1 = matrix.Matrix(system_size)
    ode_k2 = matrix.Matrix(system_size)
    ode_k3 = matrix.Matrix(system_size)
    ode_k4 = matrix.Matrix(system_size)
    ode_dbydt = matrix.Matrix(system_size)
    ode_var = [ode_k1, ode_k2, ode_k3, ode_k4, ode_dbydt]

    # Trapezoidal rule
    ##ode_k1=matrix.Matrix(system_size)
    ##ode_k2=matrix.Matrix(system_size)
    ##ode_dbydt=matrix.Matrix(system_size)
    ##ode_var=[ode_k1, ode_k2, ode_dbydt]


    # Assign the parameters to the circuit elements.
    NwRdr.read_circuit_parameters(nw_input, conn_ckt_mat, branch_params, component_objects, components_found)

    if (gv.c==0):
        print()
        print("*"*50)
        # Just checking the objects
        for items in component_objects.keys():
            component_objects[items].display()
        print("*"*50)
        print()


    # Read the control code and the descriptions of the control code
    control_files,  control_functions,  control_file_inputs, \
            control_file_outputs, control_file_staticvars, control_file_timeevents, \
            control_file_variablestorage,  control_file_events = \
            NwRdr.update_control_code(component_objects, components_found, \
                                      controlled_elements, meter_list, control_files)

    import __control


    plotted_variable_list = []
#    if controlled_elements:
    for c1 in control_file_variablestorage.keys():
        if control_file_variablestorage[c1][1]=="yes":
            plotted_variable_list.append(c1)


    print()
    print()


    t = 0.0
    t_ode = 0.0
    t_ode_prev = -dt
    t_diff = dt
    t_store = dt_store


    if (gv.c==0):
        print()
        print()
        print("*"*50)
        print("Output file is in columns and the columns are in the following sequence")
        print("1 => Time")
        print("Meters are in the following sequence:")
        for count1 in range(len(meter_list)):
            print("{prt_index} => {prt_meter_type}_{prt_meter_tag} at {prt_meter_pos}".format(
                    prt_index=str(count1+2),
                    prt_meter_type=component_objects[meter_list[count1]].type,
                    prt_meter_tag=component_objects[meter_list[count1]].tag,
                    prt_meter_pos=component_objects[meter_list[count1]].pos
            ))
        if plotted_variable_list:
            print("Control variables to be plotted are in the following sequence")
            for count2 in range(len(plotted_variable_list)):
                print("{} => {}".format(str(count1 + count2 + 3), plotted_variable_list[count2]))
    
        print()
        print("*"*50)


    start_time = time.time()
    print()
    print()


    while t<t_limit:
        # Check if an event has been generated. If yes,
        # recalculate the system matrices. If not, just
        # solve the ODE

        if ("yes" in branch_events) or ("hard" in branch_events):

            # Initialize the branch parameters from the
            # values of the components in the branch.
            NwRdr.initialize_branch_params(branch_params, branch_events, component_objects, source_list, sys_mat_u, components_in_branch)


            # This system map is to describe whether in each loop
            # a branch exists - if it does, is it "stiff" or not ("yes")
            # Initialize all of the elements to "no"
            if not system_loop_map:
                for c1 in range(len(system_loops)):
                    br_vector = []
                    for c2 in range(len(branch_params)):
                        br_vector.append("no")
                    system_loop_map.append(br_vector)

                # This function will populate the system loop map from the system loops
                # Also, this will create the list stiff_ratio that defines which
                # branches are stiff
                Slv.generate_system_loops(system_loops, branch_params, system_loop_map, stiff_ratio, dt)


                # Delete any loops that violate the basic rules
                for c1 in range(len(system_loop_map)-1, -1, -1):
                    is_loop_genuine = Slv.loop_validity_checking(system_loop_map[c1], branches_in_kcl_nodes, kcl_branch_map)
                    if is_loop_genuine=="no":
                        del system_loop_map[c1]


                # The next block of code seeks to eliminate redundant loops
                # or dependent loops. These are loops that are not identical to
                # other loops but are linear combinations of other loops. If not
                # eliminated, these extra loops can cause instability.

                # The loops are arranged into clusters according to the first
                # branch in these loops.
                loop_clusters = []
                c1 = 0
                c2 = 0
                while (c1<len(system_loop_map)) and (c2<len(system_loop_map[0])):
                    # For each loop, attempt to loop for the first branch.
                    curr_loop_cluster = []

                    # Assume that the first branch c2 in the loop c1
                    # is not a branch. In that case loop for subsequent
                    # loops to check if any of those loops have branches
                    # at c2.
                    branch_found = "no"
                    if system_loop_map[c1][c2]=="no":
                        c3 = c1 + 1
                        c4 = c2
                        while c3<len(system_loop_map) and c4<len(system_loop_map[c1]) and branch_found=="no":
                            if not system_loop_map[c3][c4]=="no":
                                # Interchange the loops if another loop below it
                                # has a branch.
                                branch_found = "yes"
                                if not c1==c3:
                                    system_loop_map[c1], system_loop_map[c3] = system_loop_map[c3], system_loop_map[c1]
                                c2 = c4
                            else:
                                c3 += 1
                                # If all the loops have been exhausted, it means the
                                # branch is only found in previous loops. So move on
                                # to the next branch and go back to the loop c1.
                                if c3==len(system_loop_map):
                                    c3 = c1
                                    c4 += 1

                    else:
                        branch_found = "yes"


                    # If a branch has been found, eliminate branches from
                    # all subsequent loops. Sometimes, this is not possible
                    # as the loops are not compatible. In that case the cluster
                    # is expanded and loops are interchanged.
                    if branch_found=="yes":
                        curr_loop_cluster.append(c1)
                        # Start with the first loop after the cluster.
                        c3 = curr_loop_cluster[-1] + 1
                        while c3<len(system_loop_map):
                            # Attempt to perform manipulations with every
                            # loop in the cluster. Once successful, exit
                            c4 = 0
                            loop_manip_success = "no"
                            common_branch_found = "no"
                            while c4<len(curr_loop_cluster) and common_branch_found=="no":
                                row_position = curr_loop_cluster[c4]
                                if not system_loop_map[c3][c2]=="no":
                                    if not system_loop_map[row_position][c2]=="no":
                                        common_branch_found = "yes"
                                        if system_loop_map[c3][c2]==system_loop_map[row_position][c2]:
                                            loop_manip_result = Slv.loop_manipulations(system_loop_map, branches_in_kcl_nodes, kcl_branch_map, \
                                                    row_position, c3, "difference", branch_params, branch_tags_in_loops, stiff_ratio)
                                        else:
                                            loop_manip_result = Slv.loop_manipulations(system_loop_map, branches_in_kcl_nodes, kcl_branch_map, \
                                                    row_position, c3, "addition", branch_params, branch_tags_in_loops, stiff_ratio)

                                        if loop_manip_result:
                                            loop_manip_success = "yes"

                                # Look for a common branch with every loop in the cluster
                                if common_branch_found=="no":
                                    c4 += 1

                            # If a common branch has been found, but no loop
                            # manipulation was successful, the loop will have to
                            # be added to the cluster.
                            if loop_manip_success=="no" and common_branch_found=="yes":
                                # If the loop is away from the last loop in the cluster,
                                # a loop interchange needs to be performed to bring the loop
                                # just below the cluster
                                if c3>curr_loop_cluster[-1]+1:
                                    system_loop_map[c3], system_loop_map[curr_loop_cluster[-1]+1] = system_loop_map[curr_loop_cluster[-1]+1], \
                                                    system_loop_map[c3]
                                    # Increment the loop pointer as the new loop will come below
                                    # the cluster.
                                    c3 = curr_loop_cluster[-1]+2
                                    curr_loop_cluster.append(c3-1)
                                else:
                                    c3 += 1
                                    curr_loop_cluster.append(c3)
                            else:
                                c3 += 1

                        # Add the custer to all the loop clusters
                        loop_clusters.append(curr_loop_cluster)

                    # Increment the loop and branch counters.
                    # The loop counter will be loop subsequent to the
                    # last loop in the last cluster.
#                    if loop_clusters:
                    c1 = loop_clusters[-1][-1] + 1
                    c2 += 1
                

                # Determine which branch each component is in. This is to
                # speed up the simulator so as it does not search for a
                # component in the circuit every time.
                for c1 in range(len(branch_params)):
                    for c2 in range(len(branch_params[c1][:-1])):
                        try:
                            comp_pos = NwRdr.csv_element(branch_params[c1][c2])
                            component_objects[comp_pos]
                        except:
                            pass
                        else:
                            component_objects[comp_pos].determine_branch(branch_params)


                # No branch in the circuit that has an element in it can
                # have zero resistance. An empty branch with only "wire"
                # is possible.
                for c1 in range(len(branch_params)):
                    if (branch_params[c1][-1][0][1] or \
                        ((1.0 in branch_params[c1][-1][1]) or \
                        (-1.0 in branch_params[c1][-1][1]))):

                            if not branch_params[c1][-1][0][0]:

                                print("Following branch has zero resistance")
                                NwRdr.human_loop(branch_params[c1][:-1])
                                print()
                                raise CktEx.BranchZeroResistanceError


                # This is to speed up the KCL calculations. This way the
                # branches connected to nodes can be looked up from this
                # table and don't have to be calculated every time. The
                # only branches that will be calculated are the nonlinear
                # branches.
                kcl_branch_lookup = []
                for c1 in range(len(branch_params)):
                    branch_vector = []
                    branch_vector.append(branch_events[c1])
                    for c2 in range(len(kcl_branch_map)):
                        for c3 in range(c2+1, len(kcl_branch_map[c2])):
                            if kcl_branch_map[c2][c3]:
                                if c1 in kcl_branch_map[c2][c3][0]:
                                    branch_vector.append([c2, c3])
                                    br_pos = kcl_branch_map[c2][c3][0].index(c1)
                                    branch_vector.append(kcl_branch_map[c2][c3][1][br_pos])

                    if stiff_ratio[c1]=="yes":
                        branch_vector.append(1)
                    else:
                        if (branch_params[c1][-1][0][1]):
                            if  abs(branch_params[c1][-1][0][1]/branch_params[c1][-1][0][0]) < 0.1*dt:
                                branch_vector.append(1)
                            else:
                                branch_vector.append(2)
                        else:
                            branch_vector.append(1)

                    branch_vector.append(branch_params[c1][-1][3])
                    branch_vector.append(branch_params[c1][-1][0][0])
                    branch_vector.append(branch_params[c1][-1][2])
                    kcl_branch_lookup.append(branch_vector)


            # This function will update the system loop map with
            # the stiffness information from previous iteration.
            Slv.update_system_loop_map(branch_params, system_loop_map, stiff_ratio, dt)


            # Store the branch events
            for c1 in range(len(branch_params)):
                branch_events_prev[c1] = branch_events[c1]


            # Each case of the simulation with a different set of
            # branch stiffness, will be stored for future reference to
            # reduce repeated calculations. These cases will be stored
            # in dictionaries and the keys will be the stiffness
            # information of the branches.
            branch_stiffness_key = ""
            for c1 in range(len(stiff_ratio)):
                if stiff_ratio[c1]=="yes":
                    branch_stiffness_key += "y"
                else:
                    branch_stiffness_key += "n"


            if branch_stiffness_key in snap_branch_stiffness.keys():
                branch_layout_found = "yes"
            else:
                branch_layout_found = "no"


            # Generate the system information matrices either by calculation or
            # by extracting the stored information from snapshots.

            if branch_layout_found=="no":
                # If the snapshot of the system interms of branch stiffness has not been
                # found, it means, that this state of the system has not been encountered
                # before. So all snapshot information is stored.


                # Check if the system is stiff and recalculate if it is.
                # The stiff loops are isolated to the minimum number of loops
                # So that the system dynamics are captured as far as possible.
                Slv.remove_stiffness(system_loop_map, [curr_state_vec, next_state_vec], loop_stiff_info, branches_in_kcl_nodes, kcl_branch_map, \
                                        branch_params, branch_tags_in_loops, stiff_ratio)

                Slv.approximate_nonstiff_loops(branch_params, stiff_ratio, system_loop_map, branches_in_kcl_nodes, kcl_branch_map, branch_tags_in_loops)


                # With the stiff branches minimized to the minimum number
                # of loops, the stiffness information of the branches and the
                # manipulated system_loop_map are stored.
                snap_branch_stiffness[branch_stiffness_key] = []
                for c1 in range(len(stiff_ratio)):
                    snap_branch_stiffness[branch_stiffness_key].append(stiff_ratio[c1])


                snap_system_loopmap[branch_stiffness_key] = []
                for c1 in range(len(system_loop_map)):
                    row_vector = []
                    for c2 in range(len(system_loop_map[c1])):
                        row_vector.append(system_loop_map[c1][c2])
                    snap_system_loopmap[branch_stiffness_key].append(row_vector)


                single_nonstiff_collection = []
                compute_loops_nonstiff = []
                loop_map_collection_nonstiff = []
                single_stiff_collection = []
                compute_loops_stiff = []
                loop_map_collection_stiff = []
                nonstiff_loops = []



                # The next step is to divide the loops into stiff and non-stiff loops
                # After which information on how to compute the loop currents of the
                # non-stiff loops is stored in the snapshot dictionaries.
                single_nonstiff_collection, compute_loops_nonstiff, loop_map_collection_nonstiff, \
                single_stiff_collection, compute_loops_stiff, loop_map_collection_stiff, nonstiff_loops = \
                    Slv.compute_loop_currents_generate(branch_params, stiff_ratio, system_loop_map, branch_events, branches_in_kcl_nodes)


#                Slv.compute_loop_currents_calc(single_nonstiff_collection, compute_loops_nonstiff, loop_map_collection_nonstiff, \
#                            single_stiff_collection, compute_loops_stiff, loop_map_collection_stiff, branch_params, \
#                            [curr_state_vec, next_state_vec])


                # These are the branches that occur only once in a nonstiff loop
                # and so the branch currents automatically become the loop currents.
                snap_single_collection_nonstiff[branch_stiffness_key] = []
                for c1 in range(len(single_nonstiff_collection)):
                    row_vector = []
                    for c2 in range(len(single_nonstiff_collection[c1])):
                        row_vector.append(single_nonstiff_collection[c1][c2])
                    snap_single_collection_nonstiff[branch_stiffness_key].append(row_vector)


                # These are the nonstiff loops whose current needs to be calculated
                # as they do not have any unique branches.
                snap_compute_loops_nonstiff[branch_stiffness_key] = []
                for c1 in range(len(compute_loops_nonstiff)):
                    snap_compute_loops_nonstiff[branch_stiffness_key].append(compute_loops_nonstiff[c1])

                # The calculation of the loop currents is by solving equations AX=B
                # Below is the matrix A. The matrix B will always change as it is the
                # input.
                snap_loop_map_collection_nonstiff[branch_stiffness_key] = []
                for c1 in range(len(loop_map_collection_nonstiff)):
                    row_vector = []
                    for c2 in range(len(loop_map_collection_nonstiff[c1])):
                        row_vector.append(loop_map_collection_nonstiff[c1][c2])
                    snap_loop_map_collection_nonstiff[branch_stiffness_key].append(row_vector)


                # These are the branches that occur only once in a stiff loop
                # and so the branch currents automatically become the loop currents.
                snap_single_collection_stiff[branch_stiffness_key] = []
                for c1 in range(len(single_stiff_collection)):
                    row_vector = []
                    for c2 in range(len(single_stiff_collection[c1])):
                        row_vector.append(single_stiff_collection[c1][c2])
                    snap_single_collection_stiff[branch_stiffness_key].append(row_vector)


                # These are the stiff loops whose current needs to be calculated
                # as they do not have any unique branches.
                snap_compute_loops_stiff[branch_stiffness_key] = []
                for c1 in range(len(compute_loops_stiff)):
                    snap_compute_loops_stiff[branch_stiffness_key].append(compute_loops_stiff[c1])

                # The calculation of the loop currents is by solving equations AX=B
                # Below is the matrix A. The matrix B will always change as it is the
                # input.
                snap_loop_map_collection_stiff[branch_stiffness_key] = []
                for c1 in range(len(loop_map_collection_stiff)):
                    row_vector = []
                    for c2 in range(len(loop_map_collection_stiff[c1])):
                        row_vector.append(loop_map_collection_stiff[c1][c2])
                    snap_loop_map_collection_stiff[branch_stiffness_key].append(row_vector)


                # All the nonstiff loops. This is used for solving the final ODE.
                snap_nonstiff_loops[branch_stiffness_key] = []
                for c1 in range(len(nonstiff_loops)):
                    snap_nonstiff_loops[branch_stiffness_key].append(nonstiff_loops[c1])

            else:
                # If the system snapshot has been found before, all the information can be
                # immediately extracted from the snapshot matrices with minimal or no
                # calculations.

                system_loop_map = []
                for c1 in range(len(snap_system_loopmap[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_system_loopmap[branch_stiffness_key][c1])):
                        row_vector.append(snap_system_loopmap[branch_stiffness_key][c1][c2])
                    system_loop_map.append(row_vector)


                single_nonstiff_collection = []
                for c1 in range(len(snap_single_collection_nonstiff[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_single_collection_nonstiff[branch_stiffness_key][c1])):
                        row_vector.append(snap_single_collection_nonstiff[branch_stiffness_key][c1][c2])
                    single_nonstiff_collection.append(row_vector)


                compute_loops_nonstiff = []
                for c1 in range(len(snap_compute_loops_nonstiff[branch_stiffness_key])):
                    compute_loops_nonstiff.append(snap_compute_loops_nonstiff[branch_stiffness_key][c1])


                loop_map_collection_nonstiff = []
                for c1 in range(len(snap_loop_map_collection_nonstiff[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_loop_map_collection_nonstiff[branch_stiffness_key][c1])):
                        row_vector.append(snap_loop_map_collection_nonstiff[branch_stiffness_key][c1][c2])
                    loop_map_collection_nonstiff.append(row_vector)

                single_stiff_collection = []
                for c1 in range(len(snap_single_collection_stiff[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_single_collection_stiff[branch_stiffness_key][c1])):
                        row_vector.append(snap_single_collection_stiff[branch_stiffness_key][c1][c2])
                    single_stiff_collection.append(row_vector)


                compute_loops_stiff = []
                for c1 in range(len(snap_compute_loops_stiff[branch_stiffness_key])):
                    compute_loops_stiff.append(snap_compute_loops_stiff[branch_stiffness_key][c1])


                loop_map_collection_stiff = []
                for c1 in range(len(snap_loop_map_collection_stiff[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_loop_map_collection_stiff[branch_stiffness_key][c1])):
                        row_vector.append(snap_loop_map_collection_stiff[branch_stiffness_key][c1][c2])
                    loop_map_collection_stiff.append(row_vector)

                nonstiff_loops = []
                for c1 in range(len(snap_nonstiff_loops[branch_stiffness_key])):
                    nonstiff_loops.append(snap_nonstiff_loops[branch_stiffness_key][c1])


            # When a branch becomes stiff naturally such as a diode or an IGBT turning off
            # because current through it reverses, it actual practice, the current is
            # extremely low and the reverse current that restores the charge is also extremely low.
            # In simulations however, when a device turns off the current can be significant.
            # When a branch becomes stiff for reason such as this, it should not result in
            # freewheeling as current is almost zero. Therefore, to ensure that freewheeling does
            # not take place, these branch currents are made zero.
            Slv.new_stiff_branch_adjustment(system_loop_map, branch_params, branch_events, stiff_ratio, [curr_state_vec, next_state_vec], \
                            sys_mat_e, sys_mat_a, sys_mat_b, sys_mat_u,  dt)


            # Calculate the inductor voltages
            # For debugging only
            #inductor_voltages = NwRdr.inductor_volt_calc(inductor_list, system_loop_map, branch_params, ode_var, dt)

            freewheel_attempt_no = 0
            new_branch_events = "yes"
            # This list is no longer used.
            nodes_in_kcl_calc = []
            while new_branch_events=="yes":

                # Initialize currents in branches
                # This is used to determine whether any
                # inductor current change event occurs.
                for c1 in range(len(branch_currents)):
                    branch_currents[c1] = 0.0

                # Update the look up table for the KCL calculations.
                for c1 in range(len(branch_params)):
                    kcl_branch_lookup[c1][0] = branch_events[c1]
#                    if branch_events[c1]=="yes" or branch_events[c1]=="hard":
                    if branch_events[c1]=="yes" or branch_events[c1]=="hard" or branch_params[c1][-1][0][1]:
                        if stiff_ratio[c1]=="yes":
                            kcl_branch_lookup[c1][3] = 1
                        else:
                            if (branch_params[c1][-1][0][1]):
                                if  abs(branch_params[c1][-1][0][1]/branch_params[c1][-1][0][0]) < 0.1*dt:
                                    kcl_branch_lookup[c1][3] = 1
                                else:
                                    kcl_branch_lookup[c1][3] = 2
                            else:
                                kcl_branch_lookup[c1][3] = 1

                    kcl_branch_lookup[c1][4] = branch_params[c1][-1][3]
                    kcl_branch_lookup[c1][5] = branch_params[c1][-1][0][0]
                    kcl_branch_lookup[c1][6] = branch_params[c1][-1][2]


                # Nodal analysis
                Slv.current_continuity(kcl_branch_lookup, admittance_matrix, source_vector, abridged_node_voltage, node_voltage, \
                                kcl_node_list, node_list, shortnode_list, branch_params, nonlinear_freewheel_branches, branch_currents, \
                                "det_state", t, 1)


                # Determine the state of nonlinear devices
                # Using the currents from nodal analysis,
                # it will check if any of the devices will start
                # or stop conducting.

                if freewheel_attempt_no > 1:
                    for comps in component_objects.keys():
                        component_objects[comps].determine_state(branch_currents, branch_params, branch_events)
                else:
                    for comps in component_objects.keys():
                        component_objects[comps].pre_determine_state(branch_currents, branch_params, branch_events)


                # Check if there is a difference in the branch events as opposed
                # to the previous nodal analysis. Keep performing nodal analysis
                # until there are no new branch events
                new_branch_events = "no"
                for c1 in range(len(branch_params)):
                    if not branch_events[c1]==branch_events_prev[c1]:
                        new_branch_events = "yes"


                # For those branches that have experienced an event,
                # get the new values of branch parameters from the
                # components in the branch.
                NwRdr.initialize_branch_params(branch_params, branch_events, component_objects, source_list, sys_mat_u, components_in_branch)


                # Store the branch events
                for c1 in range(len(branch_params)):
                    branch_events_prev[c1] = branch_events[c1]

                freewheel_attempt_no += 1

            # This is the end of the block to determine freewheeling.


            # This function will update the system loop map with
            # the stiffness information from continuity check.
            Slv.update_system_loop_map(branch_params, system_loop_map, stiff_ratio, dt)


            # Arrange the nonstiff loops in ascending order of di/dt.
##            Slv.arrange_nonstiff_loops(sys_mat_e, sys_mat_a, sys_mat_b, sys_mat_u,  dt, branch_params, stiff_ratio, system_loop_map,\
##                    [curr_state_vec, next_state_vec],  branch_events)


            # To obtain the system information matrices, check if the stiffness information
            # has been encountered before. If so, extract from the snapshot dictionaries
            # or else run the remove_stiffness and compute_loop_currents functions.
            branch_stiffness_key = ""
            for c1 in range(len(stiff_ratio)):
                if stiff_ratio[c1]=="yes":
                    branch_stiffness_key += "y"
                else:
                    branch_stiffness_key += "n"

            if branch_stiffness_key in snap_branch_stiffness.keys():
                branch_layout_found = "yes"
            else:
                branch_layout_found = "no"


            if branch_layout_found=="no":

                # Check if the system is stiff and recalculate if it is.
                # The stiff loops are isolated to the minimum number of loops
                # So that the system dynamics are captured as far as possible.
                Slv.remove_stiffness(system_loop_map, [curr_state_vec, next_state_vec], loop_stiff_info, branches_in_kcl_nodes, kcl_branch_map, \
                                        branch_params, branch_tags_in_loops, stiff_ratio)

                # Add all the system matrices to the dictionary
                # corresponding to the layout of the branch stiff
                # information.

                Slv.approximate_nonstiff_loops(branch_params, stiff_ratio, system_loop_map, branches_in_kcl_nodes, kcl_branch_map, branch_tags_in_loops)


                snap_branch_stiffness[branch_stiffness_key] = []
                for c1 in range(len(stiff_ratio)):
                    snap_branch_stiffness[branch_stiffness_key].append(stiff_ratio[c1])


                snap_system_loopmap[branch_stiffness_key] = []
                for c1 in range(len(system_loop_map)):
                    row_vector = []
                    for c2 in range(len(system_loop_map[c1])):
                        row_vector.append(system_loop_map[c1][c2])
                    snap_system_loopmap[branch_stiffness_key].append(row_vector)


                single_nonstiff_collection = []
                compute_loops_nonstiff = []
                loop_map_collection_nonstiff = []
                single_stiff_collection = []
                compute_loops_stiff = []
                loop_map_collection_stiff = []
                nonstiff_loops = []


                # The generate function generates the matrices for
                # the loops that result from a given layout of branches.
                single_nonstiff_collection, compute_loops_nonstiff, loop_map_collection_nonstiff, \
                single_stiff_collection, compute_loops_stiff, loop_map_collection_stiff, nonstiff_loops = \
                    Slv.compute_loop_currents_generate(branch_params, stiff_ratio, system_loop_map, branch_events, branches_in_kcl_nodes)


#                Slv.compute_loop_currents_calc(single_collection_nonstiff, compute_loops_nonstiff, loop_map_collection_nonstiff, \
#                            single_collection_stiff, compute_loops_stiff, loop_map_collection_stiff, branch_params, \
#                            [curr_state_vec, next_state_vec])


                snap_single_collection_nonstiff[branch_stiffness_key] = []
                for c1 in range(len(single_nonstiff_collection)):
                    row_vector = []
                    for c2 in range(len(single_nonstiff_collection[c1])):
                        row_vector.append(single_nonstiff_collection[c1][c2])
                    snap_single_collection_nonstiff[branch_stiffness_key].append(row_vector)


                snap_compute_loops_nonstiff[branch_stiffness_key] = []
                for c1 in range(len(compute_loops_nonstiff)):
                    snap_compute_loops_nonstiff[branch_stiffness_key].append(compute_loops_nonstiff[c1])


                snap_loop_map_collection_nonstiff[branch_stiffness_key] = []
                for c1 in range(len(loop_map_collection_nonstiff)):
                    row_vector = []
                    for c2 in range(len(loop_map_collection_nonstiff[c1])):
                        row_vector.append(loop_map_collection_nonstiff[c1][c2])
                    snap_loop_map_collection_nonstiff[branch_stiffness_key].append(row_vector)


                snap_single_collection_stiff[branch_stiffness_key] = []
                for c1 in range(len(single_stiff_collection)):
                    row_vector = []
                    for c2 in range(len(single_stiff_collection[c1])):
                        row_vector.append(single_stiff_collection[c1][c2])
                    snap_single_collection_stiff[branch_stiffness_key].append(row_vector)


                snap_compute_loops_stiff[branch_stiffness_key] = []
                for c1 in range(len(compute_loops_stiff)):
                    snap_compute_loops_stiff[branch_stiffness_key].append(compute_loops_stiff[c1])


                snap_loop_map_collection_stiff[branch_stiffness_key] = []
                for c1 in range(len(loop_map_collection_stiff)):
                    row_vector = []
                    for c2 in range(len(loop_map_collection_stiff[c1])):
                        row_vector.append(loop_map_collection_stiff[c1][c2])
                    snap_loop_map_collection_stiff[branch_stiffness_key].append(row_vector)


                snap_nonstiff_loops[branch_stiffness_key] = []
                for c1 in range(len(nonstiff_loops)):
                    snap_nonstiff_loops[branch_stiffness_key].append(nonstiff_loops[c1])

            else:

                # If the layout of the branches has been found before, the
                # system matrices can be extracted from the dictionaries

                system_loop_map = []
                for c1 in range(len(snap_system_loopmap[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_system_loopmap[branch_stiffness_key][c1])):
                        row_vector.append(snap_system_loopmap[branch_stiffness_key][c1][c2])
                    system_loop_map.append(row_vector)


                single_nonstiff_collection = []
                for c1 in range(len(snap_single_collection_nonstiff[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_single_collection_nonstiff[branch_stiffness_key][c1])):
                        row_vector.append(snap_single_collection_nonstiff[branch_stiffness_key][c1][c2])
                    single_nonstiff_collection.append(row_vector)


                compute_loops_nonstiff = []
                for c1 in range(len(snap_compute_loops_nonstiff[branch_stiffness_key])):
                    compute_loops_nonstiff.append(snap_compute_loops_nonstiff[branch_stiffness_key][c1])


                loop_map_collection_nonstiff = []
                for c1 in range(len(snap_loop_map_collection_nonstiff[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_loop_map_collection_nonstiff[branch_stiffness_key][c1])):
                        row_vector.append(snap_loop_map_collection_nonstiff[branch_stiffness_key][c1][c2])
                    loop_map_collection_nonstiff.append(row_vector)


                single_stiff_collection = []
                for c1 in range(len(snap_single_collection_stiff[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_single_collection_stiff[branch_stiffness_key][c1])):
                        row_vector.append(snap_single_collection_stiff[branch_stiffness_key][c1][c2])
                    single_stiff_collection.append(row_vector)


                compute_loops_stiff = []
                for c1 in range(len(snap_compute_loops_stiff[branch_stiffness_key])):
                    compute_loops_stiff.append(snap_compute_loops_stiff[branch_stiffness_key][c1])


                loop_map_collection_stiff = []
                for c1 in range(len(snap_loop_map_collection_stiff[branch_stiffness_key])):
                    row_vector = []
                    for c2 in range(len(snap_loop_map_collection_stiff[branch_stiffness_key][c1])):
                        row_vector.append(snap_loop_map_collection_stiff[branch_stiffness_key][c1][c2])
                    loop_map_collection_stiff.append(row_vector)


                nonstiff_loops = []
                for c1 in range(len(snap_nonstiff_loops[branch_stiffness_key])):
                    nonstiff_loops.append(snap_nonstiff_loops[branch_stiffness_key][c1])


            # This second run of the function is to determine the new
            # branch currents because of any possible change in the state
            # of nonlinear devices.

            # Initializing the branch currents for the next set of nodal analysis
            for c1 in range(len(branch_params)):
                branch_currents[c1] = 0.0


            for c1 in range(len(branch_params)):
                kcl_branch_lookup[c1][0] = branch_events[c1]
#                if branch_events[c1]=="yes" or branch_events[c1]=="hard":
#                if branch_events[c1]=="yes" or branch_events[c1]=="hard" or branch_params[c1][-1][0][1]:
                if stiff_ratio[c1]=="yes":
                    kcl_branch_lookup[c1][3] = 1
                else:
                    if (branch_params[c1][-1][0][1]):
                        if  abs(branch_params[c1][-1][0][1]/branch_params[c1][-1][0][0]) < 0.1*dt:
                            kcl_branch_lookup[c1][3] = 1
                        else:
                            kcl_branch_lookup[c1][3] = 2
                    else:
                        kcl_branch_lookup[c1][3] = 1


                kcl_branch_lookup[c1][4] = branch_params[c1][-1][3]
                kcl_branch_lookup[c1][5] = branch_params[c1][-1][0][0]
                kcl_branch_lookup[c1][6] = branch_params[c1][-1][2]



            # Nodal analysis
            Slv.current_continuity(kcl_branch_lookup, admittance_matrix, source_vector, abridged_node_voltage, node_voltage, \
                        kcl_node_list, node_list, shortnode_list, branch_params, nonlinear_freewheel_branches, \
                        branch_currents, "calc_currents",  t,  1)

            # Set the branch parameter currents equal to
            # the branch currents from the above nodal analysis.
            for c1 in range(len(branch_params)):
                branch_params[c1][-1][2] = branch_currents[c1]


            # This next part arranges the non stiff loops according
            # to their L/R ratios and attempts at isolating loops
            # with very low L/R ratio that may need to be approximated
            # as static loops. These loops will be different from
            # stiff loops as their current could ne non-negligible.
#            Slv.approximate_nonstiff_loops(branch_params, stiff_ratio, system_loop_map, branches_in_kcl_nodes, kcl_branch_map)
            single_nonstiff_collection, compute_loops_nonstiff, loop_map_collection_nonstiff, \
            single_stiff_collection, compute_loops_stiff, loop_map_collection_stiff, nonstiff_loops = \
                    Slv.compute_loop_currents_generate(branch_params, stiff_ratio, system_loop_map, branch_events, branches_in_kcl_nodes)


            # Compute loop currents from the branch currents
            Slv.compute_loop_currents_calc(single_nonstiff_collection, compute_loops_nonstiff, loop_map_collection_nonstiff, \
                            single_stiff_collection, compute_loops_stiff, loop_map_collection_stiff, branch_params, \
                            [curr_state_vec, next_state_vec])


            # Re-initialize the matrices A, B, and E
            # Only the nonstiff loops are solved. The stiff branches
            # are claculated by KCL.
            sys_mat_a.zeros(len(nonstiff_loops),len(nonstiff_loops))
            sys_mat_e.zeros(len(nonstiff_loops),len(nonstiff_loops))
            sys_mat_b.zeros(len(nonstiff_loops),sys_mat_b.columns)

            # Recalculate the system matrices for the new loops.
            Slv.recalculate_sys_matrices(system_loop_map, nonstiff_loops, branch_params, sys_mat_a, sys_mat_e, sys_mat_b, dt)


            # Upper triangularization of matrix E.
            Slv.mat_ode_reduce(sys_mat_e, sys_mat_a, sys_mat_b)


            # Mark the stiff loops
            stiff_loops = []
            for c1 in range(len(system_loop_map)):
                if not c1 in nonstiff_loops:
                    stiff_loops.append(c1)
                    if abs(curr_state_vec.data[c1][0])>1.0e-4:
                        curr_state_vec.data[c1][0] = 0.0
                        next_state_vec.data[c1][0] = 0.0


            # Initialize the matrices for the stiff equations
            stiff_sys_mat_a1 = matrix.Matrix(len(stiff_loops), len(stiff_loops))
            stiff_sys_mat_a2 = matrix.Matrix(len(stiff_loops),len(nonstiff_loops))
            stiff_sys_mat_e = matrix.Matrix(len(stiff_loops),len(nonstiff_loops))
            stiff_sys_mat_b = matrix.Matrix(len(stiff_loops),sys_mat_b.columns)

            # Set the values for the matrices for the stiff equations.
            Slv.determining_matrices_for_stiff_loops(system_loop_map, branch_params, stiff_loops, nonstiff_loops, stiff_sys_mat_a1, \
                                        stiff_sys_mat_a2, stiff_sys_mat_e, stiff_sys_mat_b)

            # Find out which are the branches and loops that have turned stiff in
            # this iteration. These branches and loops will have currents that
            # are not nelgigible but the resistances will be large.
            branches_turned_stiff = []
            loops_turned_stiff = []
            for c1 in stiff_loops:
                for c2 in range(len(system_loop_map[c1])):
                    if not system_loop_map[c1][c2]=="no":
                        if branch_events[c2]=="yes" or branch_events[c2]=="hard":
                            if stiff_ratio[c2]=="yes":
                                if c2 not in branches_turned_stiff:
                                    branches_turned_stiff.append(c2)
                                if c1 not in loops_turned_stiff:
                                    loops_turned_stiff.append(c1)


            # Reset the loops that have turned stiff in this iteration.
            for c1 in loops_turned_stiff:
                curr_state_vec.data[stiff_loops.index(c1)][0] = 0.0
                next_state_vec.data[stiff_loops.index(c1)][0] = 0.0


            # Determine the branches that are only in stiff loops.
#            Slv.determining_stiff_branches(system_loop_map, branches_in_stiff_loops, inductor_list, inductor_stiffness)

            # Remove the branch events
            for c1 in range(len(branch_events)):
                branch_events[c1] = "no"

            # Since the system has changed, generate a time_event
            # for the ODE solver to execute.
            time_event = "yes"

            # print("*"*100)
            # print(t)
            # Slv.debug_loops(system_loop_map, branches_in_kcl_nodes, branch_params, branch_tags_in_loops, range(len(system_loop_map)))
            # print()
            # print()
            # End of the event driven tasks.


        # If there has been a system change or time_event
        # or if time is greater than the simulation time step.
        if ((t>=t_ode) or (time_event=="yes")):

            # Update the input values in u matrix
            for c1 in range(len(source_list)):
                component_objects[source_list[c1]].generate_val(source_list, sys_mat_e, sys_mat_a, sys_mat_b, sys_mat_u, t, t-t_ode_prev)


            # Since only the nonstiff loops are involved in the ODE
            # use a reduced order state vector and map the currents
            # to the nonstiff loops in the complete state vector.
            reduced_curr_state.zeros(len(nonstiff_loops))
            reduced_next_state.zeros(len(nonstiff_loops))

            for c1 in range(len(nonstiff_loops)):
                reduced_curr_state.data[c1][0] = curr_state_vec.data[nonstiff_loops[c1]][0]
                reduced_next_state.data[c1][0] = next_state_vec.data[nonstiff_loops[c1]][0]


            # The ODE solver.
            # Will return the x(k+1) value called
            # as next_state_vec from x(k) value
            # called curr_state_vec

            Slv.mat_ode(sys_mat_e, sys_mat_a, sys_mat_b, [reduced_curr_state, reduced_next_state], sys_mat_u, t-t_ode_prev, ode_var, node_list)


            # Return the currents in the reduced order state vector to the
            # nonstiff loops in the full state vector
            for c1 in range(len(nonstiff_loops)):
                curr_state_vec.data[nonstiff_loops[c1]][0] = reduced_curr_state.data[c1][0]
                next_state_vec.data[nonstiff_loops[c1]][0] = reduced_next_state.data[c1][0]


            # Calculate the currents in the stiff loops.
            for c1 in range(len(stiff_loops)-1, -1, -1):
                current_in_stiff_loop = 0

                for c2 in range(stiff_sys_mat_b.columns):
                    current_in_stiff_loop += stiff_sys_mat_b.data[c1][c2]*sys_mat_u.data[c2][0]

                for c2 in range(len(nonstiff_loops)):
                    current_in_stiff_loop -= stiff_sys_mat_a2.data[c1][c2]*curr_state_vec.data[nonstiff_loops[c2]][0]

                for c2 in range(len(nonstiff_loops)):
                    current_in_stiff_loop -= stiff_sys_mat_e.data[c1][c2]*ode_var[4].data[c2][0]/dt

                for c2 in range(c1+1, len(stiff_loops)):
                    current_in_stiff_loop -= stiff_sys_mat_a1.data[c1][c2]*curr_state_vec.data[c2][0]

                curr_state_vec.data[c1][0] = current_in_stiff_loop/stiff_sys_mat_a1.data[c1][c1]
                if (curr_state_vec.data[c1][0] > 0.0) and (curr_state_vec.data[c1][0] > 1.0e-4):
                    curr_state_vec.data[c1][0] = 0.0
                if (curr_state_vec.data[c1][0] < 0.0) and (curr_state_vec.data[c1][0] < -1.0e-4):
                    curr_state_vec.data[c1][0] = 0.0
                next_state_vec.data[c1][0] = curr_state_vec.data[c1][0]


            # Recalculate the branch currents from the loop currents
            for c1 in range(len(branch_params)):
                branch_params[c1][-1][4] = branch_params[c1][-1][2]
                branch_params[c1][-1][2] = 0.0
                for c2 in range(len(system_loop_map)):
                    if system_loop_map[c2][c1]=="forward" or system_loop_map[c2][c1]=="stiff_forward":
                        branch_params[c1][-1][2] += next_state_vec.data[c2][0]

                    elif system_loop_map[c2][c1]=="reverse" or system_loop_map[c2][c1]=="stiff_reverse":
                        branch_params[c1][-1][2] -= next_state_vec.data[c2][0]

                branch_params[c1][-1][3] = 0.0
                for c2 in range(len(branch_params[c1][-1][1])):
                    branch_params[c1][-1][3] += branch_params[c1][-1][1][c2]*sys_mat_u.data[c2][0]


            # This last run of KCL is to determine the currents in
            # the stiff branches.

            last_kcl_branches = []

            # Initializing the branch currents for the next set of nodal analysis
            for c1 in range(len(branch_params)):
                branch_currents[c1] = 0.0

            for c1 in range(len(branch_params)):
                kcl_branch_lookup[c1][0] = branch_events[c1]
#                if branch_events[c1]=="yes" or branch_events[c1]=="hard" or branch_params[c1][-1][0][1]:
                if stiff_ratio[c1]=="yes":
                    kcl_branch_lookup[c1][3] = 1
                    last_kcl_branches.append(c1)
                else:
                    if (branch_params[c1][-1][0][1]):
                        if  abs(branch_params[c1][-1][0][1]/branch_params[c1][-1][0][0]) < 0.1*dt:
                            kcl_branch_lookup[c1][3] = 1
                        else:
                            kcl_branch_lookup[c1][3] = 2
                    else:
                        kcl_branch_lookup[c1][3] = 1

                non_stiff_found = "no"
                for c2 in nonstiff_loops:
                    if not system_loop_map[c2][c1]=="no":
                        non_stiff_found = "yes"

                if non_stiff_found=="no":
                    kcl_branch_lookup[c1][3] = 1
                    if c1 not in last_kcl_branches:
                        last_kcl_branches.append(c1)

                kcl_branch_lookup[c1][4] = branch_params[c1][-1][3]
                kcl_branch_lookup[c1][5] = branch_params[c1][-1][0][0]
                kcl_branch_lookup[c1][6] = branch_params[c1][-1][2]


            # Nodal analysis
            Slv.current_continuity(kcl_branch_lookup, admittance_matrix, source_vector, abridged_node_voltage, node_voltage, \
                                kcl_node_list, node_list, shortnode_list, branch_params, nonlinear_freewheel_branches, branch_currents, \
                                "calc_currents",  t,  0)

            # Set the currents of the stiff branches as outputs of the KCL.
            for c1 in range(len(branch_params)):
                if stiff_ratio[c1]=="yes" or c1 in last_kcl_branches:
                    branch_params[c1][-1][2] = branch_currents[c1]
                    if branch_params[c1][-1][5]>0:
                        branch_params[c1][-1][5] -= 1

                else:
                    if branch_params[c1][-1][2]>0 and branch_params[c1][-1][4]<0:
                        branch_params[c1][-1][5] += 1

                    elif branch_params[c1][-1][2]<0 and branch_params[c1][-1][4]>0:
                        branch_params[c1][-1][5] += 1

                    else:
                        if branch_params[c1][-1][5]>0:
                            branch_params[c1][-1][5] -= 1


            # Update the values of objects based on x(k+1)
            for comps in component_objects.keys():
                component_objects[comps].update_val(system_loop_map, stiff_ratio, sys_mat_e, sys_mat_a, sys_mat_b, next_state_vec, \
                                    sys_mat_u, branch_params, branch_events)


            # x(k)=x(k+1) for next iteration.
            for c1 in range(system_size):
                curr_state_vec.data[c1][0] = next_state_vec.data[c1][0]


            # Save the previous time instant of ODE solver
            t_ode_prev = t
            # If the above code is running because of a
            # change in the system and not because of time
            # greater than t_ode, do not increment the t_ode.
            if time_event=="yes" and t<t_ode:
                time_event = "no"
            else:
                t_ode = t_ode + dt

            if (t>t_ode):
                t_ode = t_ode + dt


        # Store the measured values.
        if (t>=t_store):

            c1 = 1
            while c1<len(t_split_file):
                if t>t_split_file[c1-1] and t<t_split_file[c1]:
                    t_index = c1
                    c1 = len(t_split_file)
                else:
                    c1 += 1

            f[t_index-1].write("%s " %str(t),)

            for c1 in range(len(meter_list)):
                f[t_index-1].write("%s " %component_objects[meter_list[c1]].op_value,)


            if plotted_variable_list:
                for c1 in plotted_variable_list:
                    if control_file_variablestorage[c1][1]=="yes":
                        f[t_index-1].write("%s " %control_file_variablestorage[c1][0],)

            f[t_index-1].write("\n")

            t_store = t_store+dt_store


        # This time vector will contain all the future time events
        # generated by the control functions and the main ODE solver
        time_vector = [t_ode]

        # Call the control codes only if controlled elements exist.
        #if controlled_elements:
        if control_files:
            # Call the control functions in the main control programs.
            # Use the eval function to call the functions as string arguments
            for c1 in range(len(control_files)):
                eval("__control.%s(control_file_inputs, control_file_outputs, control_file_staticvars, control_file_timeevents, \
                            control_file_variablestorage, control_file_events, component_objects, c1, t, time_vector)" %control_functions[c1])

            if 1 in control_file_events:
                time_event = "yes"


        # The soonest event will be the next time instant.
        time_vector.sort()

        t = time_vector[0]
        if (t-t_ode_prev)>dt:
            t = t_ode_prev + dt


        # The next block was to ensure that the next time step is not too
        # close. Save the previous time instant of ODE solver
        if (t-t_ode_prev)<dt/(1/dt):
            t = t_ode_prev + t_diff
        else:
            if (t-t_ode_prev<t_diff):
                t_diff = t - t_ode_prev


    for c1 in range(len(f)):
        f[c1].close()

    log_file = open("output_log.txt","w")

    log_file.write("The data in the output file is as follows: \n")

    log_file.write("Time ",)

    for c1 in range(len(meter_list)):
        log_file.write("%s-%s " %(component_objects[meter_list[c1]].type, meter_list[c1]))

    log_file.write("\n \n")

    log_file.write("For plotting using Gnuplot, a sample command will be: \n")
    log_file.write("plot '%s' u 1:2 w l \n" %op_dat_file)
    log_file.write("This will plot column 2 with respect to time. \n \n")
    log_file.write("plot '%s' u 1:2 w l,'' u 1:3 w l \n" %op_dat_file)
    log_file.write("This will plot columns 2 and 3 with respect to time.")

    log_file.close()


    print("Data stored in {}. Check output log file output_log.txt for description of output".format(op_dat_file))

    end_time = time.time()

    print(str(end_time-start_time))
    if gv.c == 0:
        gv.time = float(str(end_time - start_time))
    if gv.c != 0:
        tv = float(str(end_time-start_time))
        gv.timetotal = gv.timetotal-tv
        if  gv.timetotal>0:
            print("estimated remaining time is:",gv.timetotal,"seconds")
        else:
            print(" sorry for keeping you waiting  it is gonna take a bit longer than expected")
    if (gv.optotimer == 0 and gv.c != 0):
        tv = gv.time
        expectation = 0.01
        gv.timetotal = tv*gv.algo + (tv*gv.algo)*expectation
        print(" the total time for optimization is: ",gv.timetotal,'seconds')
    if (gv.vectotimer == 0 and gv.inti_repeat == 0 and gv.vector == 1):
        tv = gv.time
        expectation = 0.02
        gv.timetotal = (tv*gv.algo + (tv*gv.algo)*expectation)*gv.ele_chg
        print(" the total time for optimization is: ",gv.timetotal,'seconds')


if __name__ == "__main__":
    main()
