from platypus import NSGAII, Problem, Real

def schaffer(vars):
    x=vars[0]
    y=vars[1]
    print(x,y)
    
    return [(x+y-3)**2, (2*x+2*y-6)**2]

def ga():
    problem = Problem(2, 2)
    list1=input("enter nos:")
    list2=int(list1)
    for i in range(0,len(list1)):
        list1[i]=int(list1[i])
    list1=int(list1)
    print(list1)
    for i  in range(0,2):
        
        problem.types[i] = [Real(an, am)]
    problem.function = schaffer

    algorithm = NSGAII(problem)
    algorithm.run(100)
    for solution in algorithm.result:
        print(solution.objectives)
ga()