import itertools
import operator
from copy import deepcopy

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
    partialassign = []
    while any([len(clause) == 1 for clause in clause_set]):
        units=[]  
        units =[i for innerlist in clause_set for i in innerlist if len(innerlist)==1] 
        units = list(set(units))
            
        for unit in units:
            removal =[]      
            for i in clause_set:
                if unit in i:
                    partialassign.append(unit)
                    removal.append(i) 
                if (-unit) in i:
                    try:
                        while True:
                            i.remove(-unit)    
                    except ValueError:
                        pass
            clause_set= [x for x in clause_set if x not in removal]

    return clause_set, partialassign

def pure_literal_elimate(clause_set):

    maxvalue=getVars(clause_set)
    for literal in maxvalue:
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
            
def getVars(clause_set):  #finds all literals in clause_set
    literals=[]
    for clause in clause_set:
        for literal in clause:
            if literal < 0 and (-1*literal) not in literals:
                literals.append(int((-1*literal)))
            elif literal > 0 and literal not in literals:
                literals.append(int(literal))
    return literals

def assign_true(clause_set,x):
    result=[]
    for clause in clause_set:
        if x in clause:
            continue
        else:
            result.append(clause)
    return result

def assign_false(clause_set,x):
    result=[]
    for clause in clause_set:
        if x in clause:
            try:
                while True:
                        clause.remove(x)
            except ValueError:
                pass
        result.append(clause)
    return result

def ChooseVariable(literals,partial_assignment):
    for x in literals:
        if x not in partial_assignment:
            break
        if all(items in literals for items in partial_assignment):
            x = False
    return x
    
def branching(clause_set,partial_assignment):
    global assignment
    if len(clause_set)==0:
        assignment=partial_assignment
        return True
    if any([len(clause)==0 for clause in clause_set]):
        return False

    literals=getVars(clause_set)
    x = ChooseVariable(literals,partial_assignment)
    newcnf=assign_true(deepcopy(clause_set),x)
    newcnf=assign_false(newcnf,-x)
    sat = branching_sat_solve(newcnf,partial_assignment+[x])
    if not sat:
        newcnf=assign_true(deepcopy(clause_set),-x)
        newcnf=assign_false(newcnf,x)
        sat = branching_sat_solve(newcnf,partial_assignment+[-x])
    return sat

def branching_sat_solve(clause_set,partial_assignment):
    truthassignments=[]
    satis=[]
    global assignment
    sat= branching(clause_set,partial_assignment)
    if sat == True:
        print('SAT')
        truthassignments.append(sorted(assignment,key=abs))
    for each in truthassignments:
        check =[]
        for x in each:
            if x<0:
                x=0
                check.append(x)
            elif x>0:
                x=1
                check.append(x)
        print(check)
    
def dpll(clause_set,partial_assignment):
    global assignment
    clause_set, unitassign = unit_propagate(clause_set)
    clause_set = pure_literal_elimate(clause_set)
    unitassign = list(set(unitassign))
    partial_assignment = partial_assignment + unitassign
    partial_assignment = list(set(partial_assignment))
    #print(partial_assignment)
    if len(clause_set)==0:
        assignment=partial_assignment
        return True
    if any([len(clause)==0 for clause in clause_set]):
        return False

    while True:
        literals=getVars(clause_set)
        x = ChooseVariable(literals,partial_assignment)
        newcnf=assign_true(deepcopy(clause_set),x)
        newcnf=assign_false(newcnf,-x)

        if newcnf == clause_set:
            partial_assignment.remove(x)
        else:
            break
    sat = dpll(newcnf,partial_assignment+[x])
    if not sat:
        newcnf=assign_true(deepcopy(clause_set),-x)
        newcnf=assign_false(newcnf,x)
        sat = dpll(newcnf,partial_assignment+[-x])
    return sat

def dpll_sat_solve(clause_set,partial_assignment):
    truthassignments=[]
    global assignment
    sat= dpll(clause_set,partial_assignment)
    if sat == True:
        truthassignments.append(sorted(assignment,key=abs))
    if len(truthassignments) ==0:
        print('UNSAT')
    else:
        print('SAT')
        for each in truthassignments:
            check =[]
            for x in each:
                if x<0:
                    x=0
                    check.append(x)
                elif x>0:
                    x=1
                    check.append(x)
            print(check)

#reading DIMACS file & creating clause set 
txtfile = open("wvbw15dimacs.txt", "r")
clauselist=[]
for x in txtfile:
    if (x[0]=="p" or x[0]=="c"):
        pass
    else:
        if x[0] not in ('c','p'):
            clause=[int(n) for n in x.split()]
            clause.remove(0)
            clauselist.append(clause)

simple_sat_solve(clauselist)
