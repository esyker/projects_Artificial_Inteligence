from PMDAProblem import PMDAProblem
import time

if __name__ == "__main__":
    problem_file=open('problem.txt','r')
    problem=PMDAProblem(problem_file)
    actions=problem.actions(problem.initial)
    #for action in actions:
    #    print("Action: ",action)
    '''
    print("Initial State:\n",problem.initial.toString())
    results=[]
    for action in actions:
        print("Action: ",action)
        result=problem.result(problem.initial,action)
        print(result.toString())
        results.append(result)
     ''' 
    
    #for patient in result.patient_list:
    #    print(patient.toString())
    start = time.time()
    solution=problem.search()
    end = time.time()
    totalTime=round(end-start,3)
    print("Total Time:",totalTime,"s")
    
    #frontier_to_string=[]
    #for i in range(frontier.__len__()):
    #    frontier_to_string.append((frontier.heap[i],frontier.heap[i][1].state.toString()))
    #print(frontier.pop().state.toString())
    print(solution.state.path_cost)
    print(solution.state.doctor_assignment)