from probability import BayesNet
from probability import elimination_ask
from itertools import product

class Disease :
    '''
    --------------------------------------------------------------
    Disease name
    --------------------------------------------------------------
    '''
    def __init__ (self,name):
        self.name=name
    
    def __str__(self):
     return self.name
 
class Symptom:
    '''
    --------------------------------------------------------------
    Symptom name and associated diseases
    --------------------------------------------------------------
    '''
    def __init__ (self,name,rel_diseases):
        self.name=name
        self.rel_diseases=rel_diseases
        
    def __str__(self):
     string="S"+self.name
     for disease in self.rel_diseases:
         string+=(" "+disease)
     return string
        
class Exam:
    '''
    --------------------------------------------------------------
    Exam name, associated disease, True Positive Rate and False
    Positive Rate
    --------------------------------------------------------------
    '''
    def __init__ (self,name,disease,TPR,FPR):
        self.name=name
        self.disease=disease
        self.TPR=TPR
        self.FPR=FPR
    
    def __str__(self):
     return "E"+self.name+" "+self.disease+" "+self.TPR+" "+self.FPR

class Result:
    '''
    --------------------------------------------------------------
    Exam name and associated Result (True/False)
    --------------------------------------------------------------
    '''
    def __init__ (self,exam_name,result):
        self.exam_name=exam_name
        self.result=result
    
    def __str__(self):
     return "M"+self.exam_name+" "+str(self.result)
 
class MDProblem :
    def __init__ (self,fh):
        '''
        -------------------------------------------------------------------------------
        Function to load the problem from a file, create the bayseian network,
        get the measured evidences and get the desired output nodes name 
        (self.last_nodes)
        -------------------------------------------------------------------------------
        '''
        # Load problem from opened file object fh
        # and use create_bayes_network() to create the Bayesian network .
        self.Diseases=list()
        self.Symptoms=list()
        self.Exams=dict()
        self.Measurements=list()
        self.propagation_probability=0
        #there is no information about the probability of the patient having the disease
        self.P_D=0.5#probability of disease
        self.load_from_file(fh)
        self.bayes_network=self.create_bayes_network()
        self.evidences=self.get_evidences()
        n = len(self.Measurements)-1
        self.last_nodes = [disease.name+f'#t{n}' for disease in self.Diseases]
        
    def load_from_file(self,fh):
        '''
        -------------------------------------------------------------------------------
        Function to load the problem from an opened file object fh
        -------------------------------------------------------------------------------
        '''
        for line in fh:
            line = line.rstrip()
            if not line:
                continue
            info=line.split()
            if (info[0]=='D'):
                for i in range(1,len(info)):
                    self.Diseases.append(Disease(info[i]))
            elif(info[0]=='S'):
                symptom=info[1]
                symptom_diseases=list()
                for i in range(2,len(info)):
                    symptom_diseases.append(info[i])
                self.Symptoms.append(Symptom(symptom,symptom_diseases))
            elif(info[0]=='E'):
                self.Exams[info[1]]=Exam(info[1],info[2],float(info[3]),float(info[4]))
            elif(info[0]=='M'):
                time_step_results=list()
                for i in range(1,len(info),2):
                    if(info[i+1]=='T'):
                        result=True
                    else:
                        result=False
                    time_step_results.append(Result(info[i],result))
                self.Measurements.append(time_step_results)
            elif(info[0]=='P'):
                self.propagation_probability=float(info[1])
    
    def get_evidences(self):
        '''
        -------------------------------------------------------------------------------
        Function to get the measured evidences (exams).
        Evidences are used on elimination_ask to solve the Bayesian Network
        -------------------------------------------------------------------------------
        '''
        evidence = {m.exam_name+f'#t{i}': m.result for i
                    , measurements in enumerate(self.Measurements) for m in measurements}
        return evidence
    
    def get_parents(self):
        '''
        -------------------------------------------------------------------------------
        Function to get the diseases with sharing symptons
        Returns a dictionary with a disease as a key and related diseases as entry
        -------------------------------------------------------------------------------
        '''
        parents={disease.name:list([disease.name]) for disease in self.Diseases}
        for symptom in self.Symptoms:
            for i in range(len(symptom.rel_diseases)):
                for j in range(len(symptom.rel_diseases)):
                        if(i!=j):
                            # Create connection between diseases wih the same symptoms
                            if(symptom.rel_diseases[j] not in parents[symptom.rel_diseases[i]]):
                                parents[symptom.rel_diseases[i]].append(symptom.rel_diseases[j])
        return parents
        
    def get_probability_for_disease(self,entry):
        '''
        ----------------------------------------------------------------------------------
        Function to get the disease probability from the truth table entry of the diseases
        ----------------------------------------------------------------------------------
        # The probability of having disease i will be smaller for t + 1
          , when having at least one other disease with sharing symptoms at t. 
          We call this the propagation probability.
        #Paremeters:
            entry:Truth Table entry
        '''
        if(entry[0]==False):#if there is no disease#t there will be no disease#t+1
            return 0
        else:#the patient had the disease#t
            for disease in entry[1:]:
                #check if there is a disease with sharing symptoms
                if disease==True:
                    return self.propagation_probability#there is a disease with sharing symptoms
            return 1#there is no disease with sharing symtpoms
        
    def get_conditional_probabilities(self,parents):
        '''
        ----------------------------------------------------------------------------
        Function to get the truth table of the disease|other_diseases and associated 
        conditional probability P(disease|other_diseases)
        ----------------------------------------------------------------------------
        #Paremeters:
            parents: Dictionary containing the diseases with sharing symptons at t-1
        '''
        # Initialize conditional probabilities
        cond_prob = {disease: 0 for disease in self.Diseases}

        for disease in self.Diseases:
            n = len(parents[disease.name])
            # Generate the truth table
            table = list(product([False, True], repeat=n))
            prob=[self.get_probability_for_disease(entry) for entry in table]
            cond_prob[disease.name] = dict(zip(table, prob))
        return cond_prob
    
    def create_bayes_network(self):
        '''
        ----------------------------------------------------------------------------
        Function to create the Bayesian Network using diseases conditional
        probabilities (propagation probability) and exams TPR and FPR
        ----------------------------------------------------------------------------
        '''
        bayes_net=BayesNet()
        #P_D is the probability of disease at t0. P_D=0.5 since there is no 
        #information at t0
        for disease in self.Diseases:
            bayes_net.add((disease.name+'#t0', '', self.P_D))
        
        #Get the diseases with sharing symptons at the several time steps
        parents=self.get_parents()
        #Get the conditional probabilities using the diseases with sharing symptons
        conditional_prob=self.get_conditional_probabilities(parents)
        
        #Add the calculated conditional_probabilities information to the bayes network
        for i in range(1, len(self.Measurements)):
            for disease in self.Diseases:
                parents_i = [parent+f'#t{i-1}' for parent in parents[disease.name]]
                bayes_net.add((disease.name+f'#t{i}', ' '.join(parents_i), conditional_prob[disease.name]))
        
        #Get the probabilitiy of the exam being false/true knowing that the patient has the disease
        exam_prob = {exam : {False: self.Exams[exam].FPR
            , True: self.Exams[exam].TPR} for exam in self.Exams}
        
        #Add the measurements/exam information to the Bayesian Network
        for i, measurements in enumerate(self.Measurements):
            for m in measurements:
                exam = m.exam_name    
                bayes_net.add((exam+f'#t{i}', self.Exams[exam].disease+f'#t{i}', exam_prob[exam]))

        return bayes_net
    
    def solve(self) :
        '''
        ----------------------------------------------------------------------------
        Function to solve the Bayesian Network and return the disease with maximum
        probability
        ----------------------------------------------------------------------------
        '''
        #get the diseases at the last time step (self.last_nodes)
        results = {disease.rsplit('#', 1)[0]: elimination_ask(disease, self.evidences
                   , self.bayes_network) for disease in self.last_nodes}
        
        print('Results')
        for disease in results:
            print(disease, '\t', results[disease].show_approx())
        
        #get the disease with maximum probability
        disease = max(results.keys(), key=(lambda disease: results[disease][True]))
        likelihood = results[disease][True]
        
        return (disease,likelihood )
