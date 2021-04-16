import itertools
import operator
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

#reading DIMACS file & creating clause set  res = [i for i in clause_set if i not in removal]  
txtfile = open("4queens.txt", "r")
clauselist=[]
for x in txtfile:
    if (x[0]=="p" or x[0]=="c"):
        pass
    else:
        if x[0] not in ('c','p'):
            clause=[int(n) for n in x.split()]
            clause.remove(0)
            clauselist.append(clause)

#print(clauselist)  
simple_sat_solve(clauselist)     

