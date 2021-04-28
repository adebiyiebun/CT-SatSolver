import itertools
import sys
import operator
a_true = set()
a_false = set()
def simple_sat_solve(clause_set):
    maxlist=[max(element) for element in clause_set]
    maxvalue=max(maxlist) #finding largest/smallest number (truth_assignments[i[x]-1]) y[i[x]-1]
    n = maxvalue
    truth_assignments = list(itertools.product([0, 1], repeat=n)) 
    sat = []
    for y in truth_assignments:  
        final = []
        for i in clause_set:
            total=0
            for x in range(0,len(i)):
                if int(i[x])>0:
                    total = total + (y[i[x]-1])
                else:
                    if (y[abs(i[x])-1])==0:
                        total=total +1 
                    else:
                        total = total + 0

            final.append(total)

        if min(final)<1:
            sat.append(0)
        else:
            sat.append(1)
            #print('sat')
            truth=[]
            for var in range (0,maxvalue):
                if y[var]==1:
                    truth.append((var)+1)
                else:
                    truth.append(-1*(var +1))
            print(truth)
    if max(sat)!=1:
        print('this CNF is unsatisfiable')
    else:
        print('this CNF is satisfiable')

def unit_propagate(clause_set): 
    while any([len(clause) == 1 for clause in clause_set]):
        units=[]  
        units =[i for innerlist in clause_set for i in innerlist if len(innerlist)==1] 
    
        if len(units):
            for unit in units:
                print(unit)
                removal =[]
                for i in clause_set:
                    if unit in i:
                        removal.append(i) 
                    if (-1*unit) in i:
                
                        try:
                            while True:
                                i.remove(-1*unit)
                        except ValueError:
                            pass
                clause_set= [x for x in clause_set if x not in removal]
                units.remove(unit)   
        else:
            return clause_set
       
    if len(clause_set)==0:
        return True
    else:
        return clause_set

def pure_literal_elimate(clause_set):
    maxlist=[max(element) for element in clause_set]
    maxvalue=max(maxlist) #finding largest/smallest number (truth_assignments[i[x]-1]) y[i[x]-1]
    for literal in range (1,maxvalue+1): 
        instances =[]
        for clause in clause_set:
            if literal in clause:
                instances.append(literal)
            elif (-1*literal) in clause:
                instances.append(-1*literal)
        result = all(element == instances[0] for element in instances)
        if result == True: #pure elimination
            for clause in clause_set:
                if instances[0] in clause:
                    try:
                        while True:
                            clause.remove(instances[0])
                    except ValueError:
                        pass
            clause_set.append([instances[0]])
        else:
            pass
    return clause_set

def dpll_sat_solve(clause_set):
    unit_propagate(clause_set)
    pure_literal_elimate(clause_set)
    if any([len(clause) == 0 for clause in clause_set]):
        print('unsat')

#reading DIMACS file & creating clause set  res = [i for i in clause_set if i not in removal]  
txtfile = open("LNP-6.txt", "r")
clauselist=[]
for x in txtfile:
    if (x[0]=="p" or x[0]=="c"):
        pass
    else:
        if x[0] not in ('c','p'):
            clause=[int(n) for n in x.split()]
            clause.remove(0)
            clauselist.append(clause)

dpll_sat_solve(clauselist)