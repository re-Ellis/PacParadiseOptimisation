from gurobipy import *

# Define sets

# Import depots
Depots = ['ID-A','ID-B','ID-C']
# Local Vaccination Centres
Centres= ['LVC0','LVC1','LVC2','LVC3','LVC4','LVC5','LVC6','LVC7']
# Census Collection Districts
Districts = ['CCD-0','CCD-1','CCD-2','CCD-3','CCD-4','CCD-5','CCD-6','CCD-7','CCD-8','CCD-9','CCD-10','CCD-11','CCD-12','CCD-13','CCD-14','CCD-15','CCD-16','CCD-17','CCD-18','CCD-19','CCD-20','CCD-21','CCD-22','CCD-23','CCD-24']
# Weeks passed
Weeks = ['W0','W1','W2','W3','W4','W5']

IMD = range(len(Depots))
LVC = range(len(Centres))
CCD = range(len(Districts)) 
W = range(len(Weeks))

# Data

# Population of each CCD
P = [2201,4585,3310,4382,3574,2574,2375,2075,4115,4588,2031,2597,2441,3624,2931,3969,2395,2544,3376,2370,2383,4475,3471,2444,4256]

# Cost to purchase vaccine dose from ID
CD = [173,145,144]

ID = [
[33.5,50.6,70.0,2.1,49.7,81.4,78.7,67.1],
[29.9,75.6,96.8,59.1,60.3,43.4,54.1,10.7],
[49.9,27.9,38.5,65.0,17.5,43.3,28.0,77.6]
]

DD = [
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

m = Model("Pacific Paradise")

# Variables
# Number of people from district CCD receiving vaccine at centre LVC in week W
X={}
for c in CCD:
    for l in LVC:
        for w in W:
            X[c,l,w] = m.addVar()
        
        
# Number of vaccines to be transported from depot IMD to centre LVC
Y={}
for i in IMD:
    for l in LVC:
        Y[i,l] = m.addVar()
        
# Percentage of people from district CCD vaccinated in week W
Z={}
for w in W:
    for c in CCD:
        Z[c,w]=m.addVar()
        
# Objective
m.setObjective(quicksum(quicksum(quicksum(X[c,l,w] for w in W)*DD[c][l]for l in LVC) for c in CCD) + quicksum(quicksum(Y[i,l]*ID[i][l]*0.2+CD[i]*Y[i,l] for i in IMD) for l in LVC) + quicksum(quicksum(quicksum(X[c,l,w] for l in LVC) for c in CCD)*10*w for w in W))

# Constraints
# Entire population vaccinated
for c in CCD:
    m.addConstr(quicksum(quicksum(X[c,l,w] for w in W) for l in LVC) == P[c])

# Vaccines received at nearby LVCs
for c in CCD:
    for l in LVC:
        if DD[c][l]==0:
            m.addConstr(quicksum(X[c,l,w] for w in W) == 0)
            
# Vaccines delivered to meet demand
for l in LVC:
    m.addConstr(quicksum(Y[i,l] for i in IMD) == quicksum(quicksum(X[c,l,w] for w in W) for c in CCD))
    
#IMDs maximum capacity
for i in IMD:
    m.addConstr(quicksum(Y[i,l] for l in LVC) <= 32000)

#LVCs weekly maximum capacity
for l in LVC:
    for w in W:
        m.addConstr(quicksum(X[c,l,w] for c in CCD) <= 2000)

# Difference in vaccination rate below 10%
for c in CCD:
    Z[c,0]=quicksum(X[c,l,0]/P[c] for l in LVC)
for w in range(len(Weeks)-1):
    for c in CCD:
        Z[c,w+1]=quicksum(X[c,l,w+1]/P[c] for l in LVC)+Z[c,w]

for w in W:
    for c in CCD:
        for b in CCD:
            m.addConstr(Z[c,w]-Z[b,w]<=0.1)
            m.addConstr(Z[c,w]-Z[b,w]>=-0.1)

m.optimize()
print("The total cost of the distributiion plan amounts to $",m.objVal )