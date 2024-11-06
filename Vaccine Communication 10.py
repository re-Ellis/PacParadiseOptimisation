from gurobipy import *
import numpy as np
setParam('MIPGap', 0)
# Sets
C = range(25)
P = range(4)
# Data
 # Virus eradication probabilities
Probs = [0.95,0.975,0.99,0.995]
LogProbs = [np.log(0.95),np.log(0.975),np.log(0.99),np.log(0.995)]
Budget = 2000000

 # cost of eradication probability
ECost = [
[53000,134000,251000,422000],
[62000,134000,254000,473000],
[55000,103000,237000,418000],
[64000,130000,243000,465000],
[67000,123000,230000,402000],
[60000,136000,243000,476000],
[70000,101000,214000,475000],
[66000,114000,210000,453000],
[62000,137000,215000,406000],
[53000,107000,258000,401000],
[54000,112000,245000,460000],
[62000,124000,248000,431000],
[51000,132000,218000,463000],
[60000,117000,213000,430000],
[64000,112000,224000,420000],
[67000,107000,206000,469000],
[64000,104000,253000,467000],
[64000,134000,256000,458000],
[58000,114000,246000,437000],
[69000,111000,240000,470000],
[59000,121000,247000,412000],
[51000,117000,246000,445000],
[58000,118000,251000,415000],
[56000,109000,254000,479000],
[54000,119000,206000,473000]
]

m = Model("Vaccine Distribution Strategy")

# Variables
 # X = 1 if probability p option chosen for CCD c
X = { (c,p): m.addVar(vtype=GRB.BINARY) for c in C for p in P}
# Objective
m.setObjective(quicksum(X[c,p]*LogProbs[p] for c in C for p in P), GRB.MAXIMIZE)

# Constraints
 # only one option chosen per CCD
for c in C:
    m.addConstr(quicksum(X[c,p] for p in P)==1)


m.addConstr(quicksum(ECost[c][p]*X[c,p] for c in C for p in P) <= Budget)

m.optimize()
print(X)
print("The eradication probability is",np.exp(m.objVal),"% given a budget of $",Budget)