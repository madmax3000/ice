def input(abbas):
    if(abbas=="Do you want to plot?\n y or n"):
        return 'n'
    if (abbas == "Do you want to optimize?\n y or n"):
        return 'y'
    if (abbas == "Which of the following feature do you want?\n 1.Optimization \n 2.Topology change and Optimization"):
        return 1
    if (abbas == "Enter circuit_params_file name\n"):
        return 'buck_ckt_params.csv'
    if (abbas == "enter no of elements to vary\n"):
        return 2
    if (abbas == "Specify the element's parameters in the following format \n (max,min,row)"):
        return '7,5,4'
    if (abbas == "Enter the output file in which the optimization targets are present \n "):
        return 'ckt_output2.dat'
    if (abbas == "enter no of output parameters to optimize"):
        return 1
    if (abbas == "enter output meter no in output file "):
        return 4
    if (abbas =="1 for avg\n2 for ripple\n3 for rms \n 4 for THD "):
        return 1
    if (abbas == "Enter the max and min limits of the output in the following format \n ( max,min)"):
        return '6,5.9'
    if (abbas == "Enter the no: of iterations"):
        return 11
   