import sys
import random
import cvxpy as cp

# 1000 is used a placeholder throughout the document for unknown values

# solve linear system
def calculcate(floors=1, xLength=1, yLength=1):
    # floors is the number of floors of the building
    # xLength is the length of the building in tiles
    # yLength is the width of the building in tiles
    
    # create building layout
    tiles = cp.Variable((xLength,yLength), integer = True)
    
    # weight of each tile ceiling
    tileWeight = 1000
    
    # create columns
    woodColumns = cp.Variable((xLength,yLength), integer = True)
    steelReinforcedColumns = cp.Variable((xLength,yLength), integer = True)
    
    # create trees
    # TODO: add more trees
    slashPineAcres = cp.Variable(nonneg = True)
    
    # cost calculation
    # page 3 of https://bugwoodcloud.org/bugwood/productivity/pdfs/SeriesPaper5.pdf for slash pine cost per acre
    cost = slashPineAcres*(55+110) + cp.sum(woodColumns)*1000
    
    # constraints
    constraints = []
    
    # CO2 constraint measured in metric tons
    # slash pine figure from https://extension.psu.edu/carbon-accounting-in-forest-management#:~:text=100%2C000%20pounds%20carbon%20per%20acre%20%C3%B7%2045,tons%20of%20CO2%20emissions%20avoided
    # steel-reinforced column figure from https://www.mdpi.com/1996-1073/6/11/5609#:~:text=As%20shown%20in%20Figure%205%2C%20the,in%20Yeo%20and%20Potra%20%5B18%5D.
    constraints.append(cp.sum(steelReinforcedColumns)*485 + cp.sum(woodColumns)*1000 - slashPineAcres*166.05 <= 0)
    
    # columns supporting each tile
    for i in range(xLength):
        for j in range(yLength):
            constraints.append(woodColumns[i][j]*1000 + steelReinforcedColumns[i][j]*1000 >= floors*tileWeight)
    
    # nonnegativity
    constraints.append(woodColumns >= 0)
    constraints.append(steelReinforcedColumns >= 0)
    
    # create and solve problem
    problem = cp.Problem(cp.Maximize(cost), constraints)
    problem.solve(solver=cp.GUROBI,verbose = True)
    
    print("cost (measured in USD):")
    print(cost.value)
    print("\ncolumns (measured in quantity):")
    print(woodColumns.value)
    print(steelReinforcedColumns.value)
    print("\ncarbon offsets (measured in acres):")
    print(slashPineAcres.value)

# get arguments from command line
if len(sys.argv) == 4:
    # extract command-line arguments
    floors = int(sys.argv[1])
    xLength = int(sys.argv[2])
    yLength = int(sys.argv[3])
else:
    print("Invalid command-line arguments. Follow this format: python script.py floors xLength yLength")
    randomFloors = random.randint(1, 10)
    randomXLength = random.randint(1, 10)
    randomYLength = random.randint(1, 10)
    print("Running randomized values: floors=" + randomFloors + " xLength=" + randomXLength + " yLength=" + randomYLength)
