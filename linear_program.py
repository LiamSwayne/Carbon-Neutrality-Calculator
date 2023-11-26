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
    # xLength is the length of the building in square-meter tiles
    # yLength is the width of the building in square-meter tiles
    
    # create building layout
    tiles = cp.Variable((xLength,yLength), integer = True)
    
    # weight of each tile used on each floor
    tileWeight = 1000
    
    # create columns
    aluminumColumns = cp.Variable((xLength,yLength), integer = True)
    steelColumns = cp.Variable((xLength,yLength), integer = True)
    
    # create trees
    # TODO: add more trees
    slashPineAcres = cp.Variable(integer = True)
    
    # cost calculation (measured in USD)
    # page 3 of https://bugaluminumcloud.org/bugaluminum/productivity/pdfs/SeriesPaper5.pdf for slash pine cost per acre
    cost = slashPineAcres*(55+110)
    # cost of aluminum columns from https://www.homedepot.com/p/Afco-8-x-7-5-8-Endura-Aluminum-Column-Round-Shaft-Load-Bearing-21-000-lbs-Non-Tapered-Fluted-Gloss-White-EA0808ANFSATUTU/301315907
    cost += cp.sum(aluminumColumns)*278
    # cost of steel columns from https://web.archive.org/web/20161210125922/http://www.homedepot.com:80/p/Tiger-Brand-8-ft-to-8-ft-4-in-Adjustable-Steel-Building-Support-Column-3-in-O-D-3A-8084/202086528
    cost += cp.sum(steelColumns)*64.90
    # cost of each square-meter tile from https://www.forbes.com/home-improvement/home/cost-to-add-second-story/#:~:text=average%20of%20%24100%20to%20%24300%20per%20square%20foot
    # middle figure of 200/square-foot taken, 200*10.7639 is the cost for a square-meter tile
    cost += 2152.78*xLength*yLength*floors
    
    # constraints
    constraints = []
    
    # CO2 constraint measured in metric tons
    # aluminum and steel column figures from https://www.wesa.fm/development-transportation/2017-08-31/aluminum-production-leaves-a-big-carbon-footprint-so-alcoa-is-adapting-with-sustainable-products#:~:text=For%20each%20ton%20of%20steel%20produced%2C%202%20tons%20of%20carbon%20is%20emitted.%20And%20for%20each%20ton%20of%20aluminum%2C%20the%20worldwide%20average%20is%2011.7%20tons%20of%20carbon%20emitted
    # each aluminum column is 30 pounds, equivalent to 0.0136078, and 0.0136078*11.7 = 0.15921126
    # each steel column is 35 pounds, equivalent to 0.0158757, and 0.0158757*2 = 0.0317514
    constraints.append(cp.sum(steelColumns)*0.0317514 + cp.sum(aluminumColumns)*0.15921126 - slashPineAcres*166.05 <= 0)
    
    # columns supporting each floor
    # aluminum column support figure from https://www.homedepot.com/p/Afco-8-x-7-5-8-Endura-Aluminum-Column-Round-Shaft-Load-Bearing-21-000-lbs-Non-Tapered-Fluted-Gloss-White-EA0808ANFSATUTU/301315907#:~:text=bearing%20limit%20(lb.)-,21000,-Material
    # 21000 pounds has been converted to metric tons
    # steel column support figure from https://www.homedepot.com/p/Tiger-Brand-8-ft-to-8-ft-4-in-Adjustable-Steel-Building-Support-Column-3-in-O-D-3A-8084/202086528#:~:text=maximum%20extension%20(lb.)-,11200%20lb,-Maximum%20load%20at
    # 11200 pounds has been converted to metric tons
    constraints.append(cp.sum(aluminumColumns)*0.0317514 + cp.sum(steelColumns)*5.0802345 >= floors*tileWeight)
    
    # nonnegativity
    constraints.append(aluminumColumns >= 0)
    constraints.append(steelColumns >= 0)
    constraints.append(slashPineAcres >= 0)
    
    # create and solve problem
    problem = cp.Problem(cp.Minimize(cost), constraints)
    problem.solve(verbose = True)
    
    logs.append("Parameters given: " + str(floors) + " floor, " + str(xLength) + " tile x length, " + str(yLength) + " tile y length.")
    logs.append("\nCost (measured in USD): $" + str(round(cost.value, 2)))
    logs.append("\ncolumns (measured in quantity):")
    logs.append("aluminum columns needed: "+str(cp.sum(aluminumColumns.value)))
    logs.append("Steel columns needed: "+str(cp.sum(steelColumns.value)))
    logs.append("\nCarbon offsets (measured in acres):")
    logs.append("Slash pine acres: " + str(slashPineAcres.value))

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
