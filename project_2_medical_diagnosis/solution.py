from probability import BayesNet
from probability import elimination_ask

class Disease :
    def __init__ (self,name):
        self.name=name
    
    def __str__(self):
     return self.name
 
class Symptom:
    def __init__ (self,name,rel_diseases):
        self.name=name
        self.rel_diseases=rel_diseases
        
    def __str__(self):
     string="S"+self.name
     for disease in self.rel_diseases:
         string+=(" "+disease)
     return string
        
class Exam:
    def __init__ (self,name,disease,TPR,FPR):
        self.name=name
        self.disease=disease
        self.TPR=TPR
        self.FPR=FPR
    
    def __str__(self):
     return "E"+self.name+" "+self.disease+" "+self.TPR+" "+self.FPR

class Result:
    def __init__ (self,exam_name,result):
        self.exam_name=exam_name
        self.result=result
    
    def __str__(self):
     return "M"+self.exam_name+" "+str(self.result)
 
class MDProblem :
    def __init__ (self,fh):
        # Place here your code to load problem from opened file object fh
        # and use probability . BayesNet () to create the Bayesian network .
        self.diseases=list()
        self.symptoms=list()
        self.exams=dict()
        self.results=list()
        self.propagation_probability=0
        self.total_time_steps=0
        #there is no information about the probability of the patient having the disease
        self.P_D=0.5    
        self.load_from_file(fh)
        self.bayes_network=self.create_bayes_network()
        self.evidences=self.get_evidences()
        n = len(self.results)-1
        self.last_nodes = [disease.name+f'@{n}' for disease in self.diseases]
        
    def load_from_file(self,fh):
        for line in fh:
            line = line.rstrip()
            if not line:
                continue
            info=line.split()
            if (info[0]=='D'):
                for i in range(1,len(info)):
                    self.diseases.append(Disease(info[i]))
            elif(info[0]=='S'):
                symptom=info[1]
                symptom_diseases=list()
                for i in range(2,len(info)):
                    symptom_diseases.append(info[i])
                self.symptoms.append(Symptom(symptom,symptom_diseases))
            elif(info[0]=='E'):
                self.exams[info[1]]=Exam(info[1],info[2],float(info[3]),float(info[4]))
            elif(info[0]=='M'):
                self.total_time_steps+=1
                time_step_results=list()
                for i in range(1,len(info),2):
                    if(info[i+1]=='T'):
                        result=True
                    else:
                        result=False
                    time_step_results.append(Result(info[i],result))
                self.results.append(time_step_results)
            elif(info[0]=='P'):
                self.propagation_probability=float(info[1])
    
    def get_parents(self):
        parents={disease.name:set([disease.name]) for disease in self.diseases}
        for symptom in self.symptoms:
            for i in range(len(symptom.rel_diseases)):
                for j in range(len(symptom.rel_diseases)):
                        if(i!=j):
                            # Create connection between diseases wih the same symptoms
                            parents[symptom.rel_diseases[i]].add(symptom.rel_diseases[j])
        return parents
    
    def get_conditional_probabilities(self,parents):
        from itertools import product

        # Initialize dictionary
        cond_prob = {disease: 0 for disease in self.diseases}

        for disease in self.diseases:
            # Number of columns of the truth table
            n = len(parents[disease.name])
            # Generate the truth table input
            table = list(product([False, True], repeat=n))
            # The first column corresponds to the same room in the previous time instant.
            # The second half of that table has that column as True, which means the room was on fire and, therefore, the probability of being on fire is 1.
            # For the other cases, the probability of being on fire is the probability of fire propagation (except the first row)
            half = 2**(n-1)
            print(type(self.propagation_probability))
            prob = [self.propagation_probability if i<half else 1 for i in range(len(table))]
            # For the first row, since no room was on fire, the probability of being on fire is 0
            prob[0] = 0

            cond_prob[disease.name] = dict(zip(table, prob))
        return cond_prob
    
    def create_bayes_network(self):
        bayes_net=BayesNet()
        for disease in self.diseases:
            bayes_net.add((disease.name+'@0', '', self.P_D))
        
        parents=self.get_parents()
        conditional_prob=self.get_conditional_probabilities(parents)
        # Add connections between diseases at the time steps 
        #(the amount of time steps correspond to the number of instants of the exam results)
        for i in range(1, len(self.results)):
            for disease in self.diseases:
                # Getting parents name at step i-1
                parents_i = [parent+f'@{i-1}' for parent in parents[disease.name]]

                # Adding node to the net. Name is the name of the room plus @<time instant>, parents is a string of all
                # the parents_i separated by spaces, and the conditional probability depends on the fire propagation law
                bayes_net.add((disease.name+f'@{i}', ' '.join(parents_i), conditional_prob[disease.name]))
        
        
        # Get a dictionary containing the conditional probabilities tables from the sensor nodes
        exam_prob = {exam : {False: self.exams[exam].FPR
            , True: self.exams[exam].TPR} for exam in self.exams}
        
        # Add measurements nodes at all time steps
        for i, measurements in enumerate(self.results):
            for m in measurements:
                # Sensor name
                exam = m.exam_name
                # Adding node to the net. Name is the sensor name plus @<time instant>, parent is the room where
                # it is installed plus @<time instant> and conditional probability corresponds to the FPR and TPR.
                bayes_net.add((exam+f'@{i}', self.exams[exam].disease+f'@{i}', exam_prob[exam]))

        return bayes_net
                
    def toString(self):
        for disease in self.diseases:
            print(disease)
        for symptom in self.symptoms:
            print(symptom)
        for exam in self.exams:
            print(exam)
        for time_step in self.results:
            for result in time_step:
                print(result,end=" ")
            print("\n",end="")
        print(self.propagation_probability)
    
    def get_evidences(self):

        evidence = {m.exam_name+f'@{i}': m.result for i
                    , measurements in enumerate(self.results) for m in measurements}
        return evidence
    
    def solve(self) :
        # Place here your code to determine the maximum likelihood
        # solution returning the solution disease name and likelihood .
        # Use probability . elimination_ask () to perform probabilistic
        # inference .

        results = {disease.rsplit('@', 1)[0]: elimination_ask(disease, self.evidences
                   , self.bayes_network) for disease in self.last_nodes}
        

        print('Results')
        for disease in results:
            print(disease, '\t', results[disease].show_approx())
        
        # Get the diseases with maximum probability and its probability
        disease = max(results.keys(), key=(lambda disease: results[disease][True]))
        likelihood = results[disease][True]
        
        return (disease,likelihood )
