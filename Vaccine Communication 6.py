from gurobipy import *

# Sets
I = range(3)
L = range(8)
C = range(25)

# Data
  # distance from ID to LVC
IDtoLVC = [
[33.5,50.6,70.0,2.1,49.7,81.4,78.7,67.1],
[29.9,75.6,96.8,59.1,60.3,43.4,54.1,10.7],
[49.9,27.9,38.5,65.0,17.5,43.3,28.0,77.6]
]

 # Population of each CCD
CCDPop = [5766,5179,5646,5363,4025,3498,3763,5766,6587,3543,3646,4340,5297,4321,5864,3870,3852,5260,3998,3700,5518,5348,4064,5673,6059]

 # Distance from CCD to LVC
CCDtoLVC = [
[45.4,0,0,15.1,0,0,0,0],
[31.6,0,0,8.2,0,0,0,0],
[22.4,0,0,27.1,0,0,0,0],
[26.0,0,0,0,0,0,0,19.1],
[42.0,0,0,0,0,0,0,5.4],
[48.6,0,0,17.5,0,0,0,0],
[28.0,0,0,5.8,0,0,0,0],
[5.6,0,0,0,32.0,0,0,0],
[23.5,0,0,0,0,0,0,19.6],
[0,0,0,0,0,30.9,0,20.0],
[0,20.6,0,0,29.8,0,0,0],
[27.8,21.6,0,0,15.1,0,0,0],
[16.8,0,0,0,20.5,0,0,0],
[20.1,0,0,0,30.6,30.2,30.9,0],
[0,0,0,0,0,8.5,19.3,0],
[0,7.5,18.3,0,24.7,0,0,0],
[0,12.3,30.0,0,6.9,0,0,0],
[0,28.2,0,0,14.0,0,25.4,0],
[0,0,0,0,24.9,24.4,15.1,0],
[0,0,0,0,0,6.8,19.8,0],
[0,27.7,8.6,0,0,0,0,0],
[0,17.1,20.3,0,21.3,0,0,0],
[0,29.0,0,0,20.5,0,29.2,0],
[0,0,0,0,0,30.6,14.7,0],
[0,0,0,0,0,32.2,22.8,0]
]

 # Cost to purchase vaccine dose from ID
IDCost = [173,145,144]

 # Travel costs
DeliveryCost = 0.2 # per km
AccessCost = 1.0 # per km

 # Cost to upgrade LVCs
LVCUCost = [1826000,1879000,1918000,1690000,1879000,1289000,1318000,1678000]

m = Model("Vaccine Distribution Strategy")

# Variables

 # X[i,l] is amount to send from ID i to LVC l
X = { (i,l): m.addVar() for i in I for l in L}

 # Y[c,l] is people for CCD c to send to LVC l
Y = { (c,l): m.addVar() for c in C for l in L}

U = {l: m.addVar(vtype=GRB.BINARY) for l in L}

# Objective
 # (Vaccine purchase cost + delivery cost per vaccine)*number of vaccines sent from ID to LVC + Cost of driving from CCD to LVC
m.setObjective(quicksum((IDCost[i] + DeliveryCost*IDtoLVC[i][l])*X[i,l] for i in I for l in L) +
	quicksum(AccessCost*CCDtoLVC[c][l]*Y[c,l] for c in C for l in L) +
    quicksum(LVCUCost[l]*U[l] for l in L), GRB.MINIMIZE)

# Constraints
 # Balance at each LVC
for l in L:
	m.addConstr(quicksum(X[i,l] for i in I) == quicksum(Y[c,l] for c in C))

 # Meet population demands
for c in C:
	m.addConstr(quicksum(Y[c,l] for l in L) == CCDPop[c])
	
 # If no connection then Y must by 0
for c in C:
	for l in L:
		if CCDtoLVC[c][l] == 0:
			m.addConstr(Y[c,l] == 0)

IDMax = 48000
LVCMax = 14000
LVCUAmt = LVCMax*0.5

for i in I:
	m.addConstr(quicksum(X[i,l] for l in L) <= IDMax)
for l in L:
	m.addConstr(quicksum(Y[c,l] for c in C) <= LVCMax + LVCUAmt*U[l])	

m.optimize()
print(U)
print("The total cost of the distributiion plan amounts to $",m.objVal)