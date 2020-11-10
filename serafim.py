from search import Problem
from search import uniform_cost_search
from search import astar_search
from itertools import permutations,combinations
import time
import math
import sys

class Doctor():
    def __init__(self,_id,efficiency):
        self._id=_id
        self.efficiency=efficiency
        
    

class PatientLabel():
    def __init__(self,max_wait_time,consult_time):
        self.maxWaitTime=max_wait_time
        self.consult_time=consult_time

 
class Patient():
    def __init__(self,_id,curr_wait_time,label,remain_consult_time,max_wait_time):
        self.labelID = label 
        self._id=_id
        self.currWaitTime=curr_wait_time
        self.remainConsultTime=remain_consult_time
        self.maxWaitTime=max_wait_time
    
    def toString(self):
        return ("ID:"+self._id+" currWaitTime:"+str(self.currWaitTime)+
    " label:"+self.labelID)
        
    def copy(self):
        return Patient(self._id,self.currWaitTime,self.labelID,self.remainConsultTime,self.maxWaitTime)
    
    def __eq__(self,other):
        if(self.currWaitTime==other.currWaitTime and self.remainConsultTime==other.remainConsultTime):
            return True
        return False
    

class State():
    def __init__(self,patient_list,pathCost,docAssignment):
        self.patient_list=patient_list
        self.path_cost=pathCost
        self.doctor_assignment=docAssignment
        #[(1,15,30,15),(2,12,40,20),...] (#patient_id,curr_wait_time,max_wait_time,remain_consult_time) 
        #[(1,15,3),(2,12,2),...] (#patient_id,curr_wait_time,#label,remain_consult_time)
        #state.numb_doctors
        #self.labels=labels #{'labelid':(max_wait_time)}
        
    
    def toString(self):
        result="--State--"
        for patient in self.patient_list:
            result+=("\n"+patient.toString())
        return result
    
    def copy(self):
        newStateList=[]
        for patient in self.patient_list: 
            new_patient=patient.copy()
            newStateList.append(new_patient)
        doctor_list=self.doctor_assignment.copy()
        return State(newStateList,self.path_cost,doctor_list)
   
    def __lt__(self,state):
        return self.path_cost<state.path_cost
    
    def __eq__(self, other):
        if(other.patient_list == None):
            return True
        for i in range(len(self.patient_list)):
            if self.patient_list[i]!=other.patient_list[i]:
                return False
        return True
    
    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.path_cost)
     
        

    '''
    def goal_test(self,state):
        
        Returns True if state s is a goal state, and False otherwise
        
        for patient in state.patient_list :
            if (patient.currWaitTime > patient.maxWaitTime) or (patient.remainConsultTime != 0):
                return False
        return True
    '''
    
    '''
    def __lt__(self,state):#put in front possible nodes or with smaller path costs
        #if inserted Node is impossible
        if self.goal_test(self)==False:
            return False
        #if other Node is impossible
        elif self.goal_test(state)==False:
            return True
        #if both nodes are possible
        else:
            #Check which has greater cost
            state1Cost=0
            for patient in self.patient_list:
                state1Cost+=patient.currWaitTime*patient.currWaitTime
            state2Cost=0
            for patient in state.patient_list:
                state2Cost+=patient.currWaitTime*patient.currWaitTime
            return state1Cost<state2Cost#return True when new state has smaller cost than others
        '''

        
class PDMAProblem(Problem):
    def __init__(self):
        super().__init__(None)
        self.labels=dict()
        self.doctor_dict=dict()
        self.initial=None
        self.nodes_expanded=0
        self.numb_docs=0
        self.solution=None
        
    def actions(self,state):
        '''
        Returns a list (or a generator) of operators applicable to state s
        '''
        doctor_ids=self.doctor_dict.keys()
        '''
        if(state.patient_list==None):
            return list()
        patients_on_limit=[]
        for patient in state.patient_list:
            if patient.currWaitTime == self.labels[patient.labelID].maxWaitTime:#pruning
                patients_on_limit.append(patient._id)
        #with_ids
        #print("ON LIMIT: ",patients_on_limit)
        if len(patients_on_limit)!=0:
            if len(patients_on_limit)>self.numb_docs:
                return list()
            if len(patients_on_limit)==self.numb_docs:
                patient_ids=patients_on_limit
                _min=min(len(doctor_ids),len(patient_ids))
                possibleActions = [dict(zip(x,doctor_ids)) for x in permutations(patient_ids,_min)]
            else:
                patient_ids=[patient._id for patient in state.patient_list if patient.remainConsultTime>0]
                _min=min(len(doctor_ids),len(patient_ids))
                permuts=permutations(patient_ids,_min)
                #print("Permuts")
                #for p in permuts:
                #    print(p)
                _permuts=[]
                for permutation in permuts:
                    for on_limit in patients_on_limit:
                        if on_limit not in permutation:
                            continue
                        _permuts.append(permutation)
                #print("_Permuts")
                #for p in _permuts:
                #    print(p)
                possibleActions = [dict(zip(x,doctor_ids)) for x in _permuts]
                #print(possibleActions)
        '''
        if state.patient_list==None:
            return []
        #else:
        patient_ids=[patient._id for patient in state.patient_list if patient.remainConsultTime>0]
        _min=min(len(doctor_ids),len(patient_ids))
        permuts=permutations(patient_ids,_min)
        possibleActions = [dict(zip(x,doctor_ids)) for x in permuts]
        #print(state.toString())
        #print(possibleActions)
        return possibleActions
    
    def result(self,state,action):
        '''
        Returns the state resulting from applying action a to state s
        '''
        newState=state.copy()
        #newState=State(state.patient_list.copy())
        #print(newState.toString())
        for patient in newState.patient_list:
            if patient.remainConsultTime != 0 :
                try:
                    doc_id=action[patient._id]
                    patient.remainConsultTime=max(0,patient.remainConsultTime-self.doctor_dict[doc_id].efficiency*5)
                except KeyError:
                    patient.currWaitTime+=5
            if patient.currWaitTime > self.labels[patient.labelID].maxWaitTime:#pruning
                newState.patient_list=None
                newState.path_cost=float('inf')
                self.nodes_expanded+=1
                return newState
        
        newState.doctor_assignment.append(action)
        
        newState.path_cost=self.path_cost(state.path_cost,state,action,newState)
        self.nodes_expanded+=1
        return newState
    
    def goal_test(self,state):
        '''
        Returns True if state s is a goal state, and False otherwise
        '''
        if state.patient_list==None:
            return False
        for patient in state.patient_list :
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
        '''
        state1Cost=0
        for patient in state1.patient_list:
            state1Cost+=patient.currWaitTime*patient.currWaitTime
        '''
        if state2.patient_list==None:
            return float('inf')
        state2Cost=0
        for patient in state2.patient_list:
            state2Cost+=patient.currWaitTime*patient.currWaitTime
        
        return state2Cost
    
    def load(self,file):
        '''
        Loads a problem from a (opened) file object f (see below for format specification)
        '''
        patient_list=list()
        doctor_assignments=list()
                
        for line in file:
            line = line.rstrip()
            if not line:
                continue
            info=line.split()
            if (info[0]=='MD'):
                #dict with keys as doc_id and doctors as values
                self.doctor_dict[info[1]]=Doctor(info[1],float(info[2])) 
            elif(info[0]=='PL'):
                self.labels[info[1]]=PatientLabel(int(info[2]),int(info[3]))
            elif(info[0]=='P'):
                patient_list.append(Patient(info[1],int(info[2])
                ,info[3],int(self.labels[info[3]].consult_time),
            self.labels[info[3]].maxWaitTime))
        self.numb_docs=len(self.doctor_dict.keys())
        self.initial=State(patient_list,0,doctor_assignments)

        
    def save(self,f):
        i=0
        f.write('MD ')
        for doctor in self.doctor_dict:
            f.write('DOC ')
            d=self.doctor_dict[doctor]._id+' '+str(self.doctor_dict[doctor].efficiency)+' '
            f.write(d)
        f.write('\n')
        f.write('MD')
        for label in self.labels.keys():
            f.write(' LAB ')
            f.write(label)
            f.write(' ')
            f.write(str(self.labels[label].maxWaitTime))
            f.write(' ')
            f.write(str(self.labels[label].consult_time))
        f.write('\n')
        f.write('MD ')
        for patient in self.initial.patient_list:
            f.write('Patient')
            f.write(patient.toString()) 
            print(patient.toString())
            i+=1
            if i==self.numb_docs:
                break
        f.write('\n')
        '''
        for patient in problem.initial.patient_list:
            print('(',patient._id," currW:",patient.currWaitTime," maxW:",patient.maxWaitTime,
                    " remainC:",patient.remainConsultTime,')')    
        print('\nDoctors:')
        for doctor in problem.doctor_dict:
            print('(',problem.doctor_dict[doctor]._id,problem.doctor_dict[doctor].efficiency,')')
        print('\n Labels:',problem.labels)
        '''
        
     
    def search(self,**kwargs):
        return True
    
    
    def heuristic(self,node):
        return 0       
    
        
                
       