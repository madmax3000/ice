from platypus import NSGAII, Problem, Real

def belegundu(vars):
    x = vars[0]
    y = vars[1]
    return [-2*x + y, 2*x + y], [-x + y - 1, x + y - 7]


problem = Problem(2, 2)
problem.types[:] = [Real(-10, 10),Real(-5,5)]
problem.function = belegundu

algorithm = NSGAII(problem)
algorithm.run(10000)
import matplotlib.pyplot as plt

plt.scatter([s.objectives[0] for s in algorithm.result],
            [s.objectives[1] for s in algorithm.result])
plt.xlim([0, 1.1])
plt.ylim([0, 1.1])
plt.xlabel("$f_1(x)$")
plt.ylabel("$f_2(x)$")
plt.show()