from search import Problem
from itertools import permutations,combinations

class Doctor():
    def __init__(self,_id,efficiency):
        self._id=_id
        self.efficiency=efficiency
        
    

class PatientLabel():
    def __init__(self,max_wait_time,consult_time):
        self.maxWaitTime=max_wait_time
        self.consult_time=consult_time

 
class Patient():
    def __init__(self,_id,curr_wait_time,label,remain_consult_time):
        self.labelID = label 
        self._id=_id
        self.currWaitTime=curr_wait_time
        self.remainConsultTime=remain_consult_time
    
    def toString(self):
        return ("ID:"+str(self._id)+" currWaitTime:"+str(self.currWaitTime)+
    " remainConsultTime:"+str(self.remainConsultTime))
    

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
        self.doctor_dict=dict()
        self.initial=None
        self.load(file)
        print('Patients:')
        for patient in self.initial.patient_list:
            print('(',patient._id,patient.currWaitTime,patient.label,patient.remainConsultTime,')')    
        print('\nDoctors:')
        for doctor in self.doctor_dict:
            print('(',self.doctor_dict[doctor]._id,self.doctor_dict[doctor].efficiency,')')
        print('\n Labels:',self.labels)
        
    def actions(self,state):
        '''
        Returns a list (or a generator) of operators applicable to state s
        '''
        #with_ids
        patient_ids=[patient._id for patient in state.patient_list if patient.remainConsultTime>0]
        doctor_ids=self.doctor_dict.keys()
        _min=min(len(doctor_ids),len(patient_ids))
        doctorsPermutations=[d for d in permutations(doctor_ids,_min)]
        patientsCombinations=[p for p in combinations(patient_ids,_min)]
        '''
        #with pointers
        _min=min(len(self.doctor_list),len(state.patient_list))
        doctorsPermutations=[d for d in permutations(self.doctor_list,_min)]
        patientsCombinations=[p for p in combinations(state.patient_list,_min)]
        '''
        possibleActions=list()
        #_list=[d for d in doctorsPermutations]
        #print("DOCS:",_list)
        for docs in doctorsPermutations:
            for patients in patientsCombinations:
                action=dict()
                for i in range(len(docs)):
                    #print("Appended:(",docs[i],patients[i],")")
                    action[patients[i]]=docs[i]
                possibleActions.append(action)
        #possibleActions[0][0][0]._id=-1
        return possibleActions
    
    def result(self,state,action):
        '''
        Returns the state resulting from applying action a to state s
        '''
        newState=State(state.patient_list.copy())
        for patient in newState.patient_list:
            if patient.remainConsultTime != 0 :
                try:
                    doc_id=action[patient._id]
                    patient.remainConsultTime=max(0,patient.remainConsultTime-self.doctor_dict[doc_id].efficiency*5)
                except KeyError:
                    patient.currWaitTime+=5
        return newState
    
    def goal_test(self,state):
        '''
        Returns True if state s is a goal state, and False otherwise
        '''
        for patient in state :
            if (patient.currWaitTime > self.labels[patient.labelID].maxWaitTime) or (patient.remainConsultTime != 0):
                return False
        return True


        
    
    def path_cost(self,cost,state1,action,state2):
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
                #dict with keys as doc_id and doctors as values
                self.doctor_dict[info[1]]=Doctor(info[1],float(info[2])) 
            elif(info[0]=='PL'):
                self.labels[int(info[1])]=PatientLabel(int(info[2]),int(info[3]))
            elif(info[0]=='P'):
                patient_list.append(Patient(info[1],int(info[2])
                ,int(info[3]),int(self.labels[info[3]][1])))
        
        self.initial=State(patient_list)
    
    
    def search(self):
        '''
        Computes the solution to the problem. It should return True or False, indicating
        whether it was possible or not to find a solution
        '''
        pass
    
    def heuristic(self,node):
        '''
        returns the heuristic of node n
        '''
        pass
        
    