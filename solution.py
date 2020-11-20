from search import Problem
from search import uniform_cost_search
from search import astar_search
from itertools import permutations

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
        return ("ID:"+str(self._id)+" currWaitTime:"+str(self.currWaitTime)+
    " remainConsultTime:"+str(self.remainConsultTime))
        
    def copy(self):
        return Patient(self._id,self.currWaitTime,self.labelID,self.remainConsultTime,self.maxWaitTime)
    
    def __eq__(self,other):
        if(self.currWaitTime==other.currWaitTime and self.remainConsultTime==other.remainConsultTime):
            return True
        return False
    

class State():
    def __init__(self,patient_list,pathCost,docAssignment,depth):
        self.patient_list=patient_list
        self.path_cost=pathCost
        self.doctor_assignment=docAssignment
        self.depth=depth        
    
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
        return State(newStateList,self.path_cost,doctor_list,self.depth)
   
    def __lt__(self,state):
        return self.path_cost<state.path_cost
    
    def __eq__(self, other):
        if(other.patient_list == None or self.patient_list==None):
            return True
        for i in range(len(self.patient_list)):
            if self.patient_list[i]!=other.patient_list[i]:
                return False
        return True
    
    def __hash__(self):
        return hash(self.path_cost)

        
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
        
        if(state.patient_list==None):
            return []
        patients_on_limit=list()
        patients_not_on_limit=list()
        patient_ids=list()

        for patient in state.patient_list:
            if patient.remainConsultTime>0:
                patient_ids.append(patient._id)
                if patient.currWaitTime == self.labels[patient.labelID].maxWaitTime:#pruning
                    patients_on_limit.append(patient._id)
                else:
                    patients_not_on_limit.append(patient._id)

        _min=min(len(doctor_ids),len(patient_ids))
            
        if len(patients_on_limit)!=0:
            if len(patients_on_limit)>self.numb_docs:
                #impossible to solve
                return []
            elif len(patients_on_limit)==self.numb_docs:
                #mandatory to choose all the patients_on_limit
                permuts=permutations(list(patients_on_limit),_min)
            else:
                #permuts=permutations(patient_ids,_min)
                _permuts=permutations(patient_ids,_min)
                permuts=[]
                for p in _permuts:
                    correct=True
                    for patient in patients_on_limit:
                        if patient not in p:
                            correct=False
                            break
                    if correct:
                        permuts.append(p)
                             
        else:
            permuts=permutations(patient_ids,_min)
        
        possibleActions = [dict(zip(x,doctor_ids)) for x in permuts]
        return possibleActions
    
    def result(self,state,action):
        '''
        Returns the state resulting from applying action a to state s
        '''
        newState=state.copy()
        newState.depth+=1
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
        print('True')
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
        self.initial=State(patient_list,0,doctor_assignments,0)
        
        self.nodes_expanded+=1

        
    def save(self,f):
        if self.solution==None:
            return 
        output={code:[] for code in self.doctor_dict.keys()}
        for action in self.solution.state.doctor_assignment:
            action = {doc: patient for patient, doc in action.items()}
            docs_assigned=set(action.keys())
            for doc in output:
                if doc in docs_assigned:
                    output[doc].append(action[doc])
                else:
                    output[doc].append('empty')
        for doc in output:
            f.write('MD ')
            f.write(doc)
            for patient in output[doc]:
                f.write(' '+patient)
            f.write('\n')
                    
     
    def search(self,**kwargs):
        '''
        Computes the solution to the problem. It should return True or False, indicating
        whether it was possible or not to find a solution
        '''
        #See if problem is solvable
        #Check maximum maxWaitTime
        maxWaitTime=-1
        for patient in self.initial.patient_list:
            if patient.maxWaitTime>maxWaitTime:
                maxWaitTime=patient.maxWaitTime
        numb_cycles=maxWaitTime/5
        if (len(self.initial.patient_list)-self.numb_docs*numb_cycles)>0:
            return False
        
        search_method = kwargs.get('search_method')
        if search_method=="uninformed":
            self.solution=uniform_cost_search(self)
        else:
            self.solution=astar_search(self, h=self.heuristic)
        return self.solution!=None
    
    def heuristic(self,node):
        if not node.state.patient_list:
            return float('inf')
        docs=list(self.doctor_dict.values())
        docs.sort(key=lambda x:x.efficiency,reverse=True)
        newState=node.state.copy()
        while 1:
            done=True
            for patient in newState.patient_list:
                if patient.remainConsultTime>0:
                    done=False
                    break
            if done:
                break
            newState.patient_list.sort(key=lambda x:x.currWaitTime)
            attended_count=0
            attend_patient_id=set()
            for patient in newState.patient_list:
                if patient.remainConsultTime>0:
                    attend_patient_id.add(patient._id)
                    attended_count+=1
                    if attended_count==self.numb_docs:
                        break

            for patient in newState.patient_list:
                if patient.remainConsultTime>0:
                        if patient._id not in attend_patient_id:    
                            patient.currWaitTime+=5
                        else:
                            patient.remainConsultTime=0
            
        goal_cost=self.path_cost(None,None,None,newState)
        h=goal_cost-node.state.path_cost
        return h
    

        
                
       