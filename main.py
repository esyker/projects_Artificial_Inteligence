from solution import PDMAProblem
import time

if __name__ == "__main__":
    problem_file=open('problem.txt','r')
    problem=PDMAProblem()
    problem.load(problem_file)
    
    print('Patients:')
    for patient in problem.initial.patient_list:
        print('(',patient._id," currW:",patient.currWaitTime," maxW:",patient.maxWaitTime,
                " remainC:",patient.remainConsultTime,')')    
    print('\nDoctors:')
    for doctor in problem.doctor_dict:
        print('(',problem.doctor_dict[doctor]._id,problem.doctor_dict[doctor].efficiency,')')
    print('\n Labels:',problem.labels)
    #actions=problem.actions(problem.initial)
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
    solution=problem.search(search_method="uninformed")
    end = time.time()
    totalTime=round(end-start,3)
    print("Total Time:",totalTime,"s")
    problem.save()
    #frontier_to_string=[]
    #for i in range(frontier.__len__()):
    #    frontier_to_string.append((frontier.heap[i],frontier.heap[i][1].state.toString()))
    #print(frontier.pop().state.toString())
    #print(solution.state.path_cost)
    #print(solution.state.doctor_assignment)
    #print(solution.state.toString())
    print("Expanded:",problem.nodes_expanded)
    print(problem.solution.state.doctor_assignment)
    print("Path Cost:",problem.solution.state.path_cost)
    