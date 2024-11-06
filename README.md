# PacParadiseOptimisation
Author: Ryan Ellis

## Senario
As the employee of an operations research consulting company, you are tasked with communicating with a client to develop a mathematical formulation for a nation-wide vaccine distribution strategy.  The nation wishes to evalutate the most cost effective way to transport vaccinations across their country given their current distribution costs and constraints.  Through constant communication with the client to assess their needs, the Python code represents iterations of the optimisation code.

## The Problem
Vaccines are imported into the country through three depots (IDs) and are then transported to a vaccination centre (LVCs).  Citizens from each district (CCD) will be assigned a clininc to receive their vaccination from.

## The Data
The data is comprised of tables containing:
* Distances between each ID to each LVC
* Population of each CCD and distances to the nearest accessible LVCs
* Importation costs per dose of vaccine at each ID

## Client Communications
### Part One (linear programming)
* Communication 1: What is the most cost effective method of distribution that would minimise total distribution costs?
* Communication 2: Could you revise your proposal to account for the capacity limit of 32 000 doses at each ID and 14 000 doses at each LVC?
* Communication 3: We anticipate that we require 6 weeks of planning, where the maximum weekly doses that can be administered is 2 000.
* Communication 4: In practice there is a cost associated with delaying vaccine distribution of $10 per person per week
* Communication 5: To ensure that the rollout of vaccinations is fair, we must ensure that the difference between proportions of the population vaccinated does not exceed 10% for any week.

### Part Two (integer programming)
* Communication 6: Due to a population influx, it is required that some of the LVCs should be upgraded to handle the increased demand.  Given the capacity increases by 50%, and the costs associated, what LVCs should be upgraded to meet demand and minimise costs?
* Communication 7: Given the amount of savings closing each LVC would have, which LVCs should be closed and which should be upgraded?
* Communication 8: To simplify the distribution process, what would the total costs be where each population district is assigned a singular LVC to have their vaccination administered?
  
* Communication 9: In addition to the vaccination strategy, there is a range of public health options that would allow us to eradicate the virus.  Given the cost to implement the options and their probability of eradicating the virus, what options should be chosen to minimise the total cost while retaining at least a 80% overall eradication chance?
* Communication 10: Propose some further options and their eradication probabililties for a range of pricing options.

### Part Three (dynamic programming)
* Communication 11: We are now interested in the best way we can implement public health options for a single district. The district can be split into 9 zones, each zone containing some key facilities. After an outbreak occurs, the zone is quarantined, and its facilities are no longer accesible. Each week we are able to protect one zone from having a virus outbreak permanantly. Assuming the equal importance of facilities, which zone should be protected first?
* Communication 12: Given an outbreak probability of 0.2 per week per zone and given the plan to protect the facilities in this order: (6, 4, 0, 7, 2, 1, 8, 3, 5), what is the expected number of distinct facilities accessible after nine weeks?
* Communication 13: Given an outbreak probability of 0.2 per week per zone, evaluate which zone should be protected first to maximise the number of expected distinct facilities.
* Communication 14: in practice it becomes more likely that zones neighbouring each other have a higher chance of outbreak by 5% per adjacent zone.  Accounting for this, what is the optimal zone to protect and how many distinct facilities are expected to be available by the end of the nine weeks?
