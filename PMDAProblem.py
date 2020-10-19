from search import Problem

class Doctor():
    def __init__(self,_id,efficiency):
        self._id=_id
        self.efficiency=efficiency
        
    
'''
class PatientLabel():
    def __init__(self,max_wait_time,consult_time):
        self
        self.max_wait_time=max_wait_time
        self.consult_time=consult_time
'''
 
class Patient():
    def __init__(self,_id,curr_wait_time,label,remain_consult_time):
        self.label=label 
        self._id=_id
        self.curr_wait_time=curr_wait_time
        self.remain_consult_time=remain_consult_time
    

class State():
    def __init__(self,patient_list):
        self.patient_list=patient_list
        #[(1,15,30,15),(2,12,40,20),...] (#patient_id,curr_wait_time,max_wait_time,remain_consult_time) 
        #[(1,15,3),(2,12,2),...] (#patient_id,curr_wait_time,#label,remain_consult_time)
        #state.numb_doctors
        #self.labels=labels #{'labelid':(max_wait_time)}
    
        
class PMDAProblem(Problem):
    def __init__(self,file):
        super().__init__(None)
        self.labels=dict()
        self.doctor_list=list()
        self.initial=None
        self.load(file)
        print('Patients:')
        for patient in self.initial.patient_list:
            print('(',patient._id,patient.curr_wait_time,patient.label,patient.remain_consult_time,')')    
        print('\nDoctors:')
        for doctor in self.doctor_list:
            print('(',doctor._id,doctor.efficiency,')')
        print('\n Labels:',self.labels)
        
    def actions(state):
        '''
        Returns a list (or a generator) of operators applicable to state s
        '''
        #possibleactions=combinations(state.patient_list,
        #                             len(state.patient_list),state.num_doctors)
        pass
    
    def result(state,action):
        '''
        Returns the state resulting from applying action a to state s
        '''
        pass
    
    def goal_test(state):
        '''
        Returns True if state s is a goal state, and False otherwise
        '''
        pass
    
    def path_cost(cost,state1,action,state2):
        '''
        Returns the path cost of state s2, reached from state s1 by
        applying action a, knowing that the path cost of s1 is c.
        We consider the following cost associated to all the patients in the waiting room: 
            C(P) = SUM(p in P) (p_cw)=^2 where p_cw is the patient waiting time
        '''
        pass
    
    def load(self,file):
        '''
        Loads a problem from a (opened) file object f (see below for format specification)
        '''
        patient_list=list()
        
        for line in file.readlines():
            info=line.split()
            if (info[0]=='MD'):
                self.doctor_list.append(Doctor(info[1],float(info[2])))
            elif(info[0]=='PL'):
                self.labels[info[1]]=(int(info[2]),int(info[3]))
            elif(info[0]=='P'):
                patient_list.append(Patient(info[1],int(info[2])
                ,self.labels[info[3]],int(self.labels[info[3]][1])))
        
        self.initial=State(patient_list)
    
    
    def search():
        '''
        Computes the solution to the problem. It should return True or False, indicating
        whether it was possible or not to find a solution
        '''
        pass
    
    def heuristic(node):
        '''
        returns the heuristic of node n
        '''
        pass
        
    