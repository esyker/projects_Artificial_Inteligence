from probability import BayesNet
from probability import elimination_ask

class Disease :
    def __init__ (self,name):
        self.name=name
    
    def __str__(self):
     return "D"+self.name
 
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
     return "M"+self.exam_name+" "+self.result
 
class MDProblem :
    def __init__ (self,fh):
        self.BayesNet=BayesNet()
        # Place here your code to load problem from opened file object fh
        # and use probability . BayesNet () to create the Bayesian network .
        self.diseases=list()
        self.symptons=list()
        self.exams=list()
        self.results=list()
        self.propagation_probability=0
        self.total_time_steps=0
                
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
                self.symptons.append(Symptom(symptom,symptom_diseases))
            elif(info[0]=='E'):
                self.exams.append(Exam(info[1],info[2],info[3],info[4]))
            elif(info[0]=='M'):
                self.total_time_steps+=1
                time_step_results=list()
                for i in range(1,len(info),2):
                    time_step_results.append(Result(info[i],info[i+1]))
                self.results.append(time_step_results)
            elif(info[0]=='P'):
                self.propagation_probability=info[1]
        
    def toString(self):
        for disease in self.diseases:
            print(disease)
        for symptom in self.symptons:
            print(symptom)
        for exam in self.exams:
            print(exam)
        for time_step in self.results:
            for result in time_step:
                print(result,end=" ")
            print("\n",end="")
        print(self.propagation_probability)
        
    def solve(self) :
        # Place here your code to determine the maximum likelihood
        # solution returning the solution disease name and likelihood .
        # Use probability . elimination_ask () to perform probabilistic
        # inference .
        """
        [Figure 14.11]
        Compute bn's P(X|e) by variable elimination.
        >>> elimination_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary
        ...  ).show_approx()
        'False: 0.716, True: 0.284'"""
        for i in range(self.total_time_steps):
            elimination_ask(X,e,self.BayesNet)

        return (disease,likelihood )
