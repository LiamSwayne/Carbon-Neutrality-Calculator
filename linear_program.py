# import built-in
import sys
import random

# import external libraries
import cvxpy as cp

# 1000 is used a placeholder throughout the document for unknown values

# info for README.md
logs = []

# solve linear system
def calculate(floors=1, xLength=1, yLength=1):
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
    cost = slashPineAcres*(55+110)
    # cost of wood columns
    cost += cp.sum(woodColumns)*1000
    # cost of each tile
    cost += 1000*xLength*yLength*floors
    
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
    problem = cp.Problem(cp.Minimize(cost), constraints)
    problem.solve(verbose = True)
    
    logs.append("Parameters given: " + str(floors) + " floor, " + str(xLength) + " tile x length, " + str(yLength) + " tile y length.")
    logs.append("cost (measured in USD):")
    logs.append(cost.value)
    logs.append("\ncolumns (measured in quantity):")
    logs.append("Wood columns:\n"+str(woodColumns.value))
    logs.append("Steel columns:\n"+str(steelReinforcedColumns.value))
    logs.append("\ncarbon offsets (measured in acres):")
    logs.append(slashPineAcres.value)

# get arguments from command line
if len(sys.argv) == 4 or len(sys.argv) == 5:
    # extract command-line arguments
    floors = int(sys.argv[1])
    xLength = int(sys.argv[2])
    yLength = int(sys.argv[3])
    calculate(floors, xLength, yLength)
else:
    print("Invalid command-line arguments. Follow this format: python script.py floors xLength yLength")
    randomFloors = random.randint(1, 10)
    randomXLength = random.randint(1, 10)
    randomYLength = random.randint(1, 10)
    print("Running randomized values: floors=" + str(randomFloors) + " xLength=" + str(randomXLength) + " yLength=" + str(randomYLength))
    calculate(randomFloors, randomXLength, randomYLength)

# only run if it is a test case
# example of a command-line run that updates a test: python3 "linear_program.py" 1 2 3 1
if len(sys.argv) == 5:
    testCaseNum = int(sys.argv[4])

    # open the README.md file
    file = open("./README.md", "r")
    fileContents = file.read()

    # locate case
    startCaseIndex = fileContents.index("<!-- TEST CASE " + str(testCaseNum) + " -->")
    endCaseIndex = fileContents[startCaseIndex:].index("<!-- END TEST CASE -->") + startCaseIndex

    newContents = fileContents[:startCaseIndex]
    newContents += "<!-- TEST CASE " + str(testCaseNum) + " -->" # add test case indicator
    newContents += "\n```python" # add markdown code start
    for i in range(len(logs)):
        newContents += "\n" + str(logs[i]) # add log
    newContents += "\n```" # add markdown code end
    newContents += "\n" + fileContents[endCaseIndex:]
    file.close()

    # writing updated content to file
    file = open("./README.md", "w")
    file.write(newContents)
    file.close()
