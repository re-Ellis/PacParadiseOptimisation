from itertools import combinations

Z = range(9)

# The state is a 9-tuple where each element is
# -1 = outbreak, 0 = normal, 1 = protected
# NextStates returns a list of tuples with a probability
# in position 0 and a state as a tuple in position 1
def NextStates(State, OutbreakProb):
    ans = []
    # Z0 are the normal zones
    Z0 = [j for j in Z if State[j]==0]
    n = len(Z0)
    for i in range(n+1):
        for tlist in combinations(Z0, i):
            p = 1.0
            slist = list(State)
            for j in range(n):
                if Z0[j] in tlist:
                    p *= OutbreakProb[Z0[j]]
                    slist[Z0[j]] = -1
                else:
                    p *= 1-OutbreakProb[Z0[j]]
            ans.append((p, tuple(slist)))
    return ans

# example
# zones 0, 6, 7 have been protected
# zones 3, 4, 8 have outbreaks
# zones 1, 2, 5 are normal (so there will be 2**3 = 8 possible next states)
states = NextStates((1,0,0,-1,-1,0,1,1,-1), [0.2 for j in Z])

Facilities = [
    'Hospital',
    'Wedding Chapel',
    'Convenience Store',
    'Supermarket',
    'Ambulance',
    'Bus Depot',
    'Town Hall',
    'Hotel',
    'School',
    'Bank',
    'Library',
    'Fire Station',
    'Post Office',
    'Police Station',
    'Medical Centre',
    'Government Office'
]

Zones = [
    [1,6,9,14],
    [2,7,9],
    [3,8,15],
    [4,7],
    [0,9,10,14],
    [8],
    [2,4,7,10,12],
    [5,11,13],
    [4,15]
]

Plan=[6,4,0,7,2,1,8,3,5]
OutbreakProb=[0.2 for j in range(len(9))]

def Fac(S):
    tot={}
    for i in range(len(S)):
        for j in Zones[i]:
            if S[i]!=-1:
                tot[j]=1
    return(len(tot))

EofX={}
def V(t,s):
    if 0 not in s:
        return (Fac(s),s)
    else:
        for a in Plan:
            if s[a]!=0:
                continue
            s = list(s)
            s[a] = 1
            s = tuple(s)
            NS=NextStates(s,[0.2 for j in range(len(s))])
            return (sum(NS[j][0] * V(t+1,NS[j][1])[0] for j in range(len(NS))),s)