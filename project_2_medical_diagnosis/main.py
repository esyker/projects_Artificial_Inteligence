from solution import MDProblem

fh=open("problem.txt")
problem=MDProblem(fh)
problem.toString()
'''
parents=problem.get_parents()
for disease in parents.keys():
    print("D",disease,end=" ")
    for parent in parents[disease]:
        print(parent,end=" ")
    print("\n",end="")
''' 
bayes_network=problem.bayes_network
print(bayes_network)
result=problem.solve()
print("Result",result)