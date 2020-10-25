from PMDAProblem import PMDAProblem

if __name__ == "__main__":
    problem_file=open('problem.txt','r')
    problem=PMDAProblem(problem_file)
    actions=problem.actions(problem.initial)
    #for action in actions:
        #print("Action: ",action)
    print("Action: ",actions[0])
    result=problem.result(problem.initial,actions[0])
    for patient in result.patient_list:
        print(patient.toString())