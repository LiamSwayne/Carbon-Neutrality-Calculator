# import built-in
import sys
import random

# import external libraries
import cvxpy as cp

# info for README.md
logs = []

# simple 2D matrix sum function
def sumMatrix(matrix):
    return int(sum(sum(row) for row in matrix))

# solve linear system
def calculate(floors=1, xLength=1, yLength=1):
    # floors is the number of floors of the building
    # xLength is the length of the building in square meter tiles
    # yLength is the width of the building in square meter tiles
    
    # weight of each square meter of subfloor
    # figure from https://www.lowes.com/pd/AdvanTech-Flooring-23-32-CAT-PS2-10-Tongue-and-Groove-OSB-Subfloor-Application-as-4-x-8/50126556#:~:text=Actual%20Length%20(Feet)-,7.989,-Common%20Thickness%20Measurement
    # converted 7.989*3.953 feet to 2.93392603407 square meters
    # weight of a 4x8 board with 5/8 inch thickness is 53 pounds, which converts to 0.0240404
    # we assume three layers of boards are used, amounting to 0.0721212
    # divide 0.0721212/2.93392603407 square meters for weight per square meter of 0.02458180579
    subflooringTileWeight = 0.02458180579

    # floor weight based on corridor measurement from https://www.researchgate.net/figure/Total-weight-for-each-floor_tbl1_231000789
    # conversion to weight per square meter is 0.5674154216
    floorWeight = 0.5674154216
    
    # create columns
    aluminumColumns = cp.Variable((xLength,yLength), integer = True)
    steelColumns = cp.Variable((xLength,yLength), integer = True)
    
    # create trees
    oakTreeAcres = cp.Variable(nonneg=True)
    slashPineAcres = cp.Variable(nonneg=True)
    eucalyptusTreeAcres = cp.Variable(nonneg=True)
    
    # cost calculation (measured in USD)
    # cost of aluminum columns from https://www.homedepot.com/p/Afco-8-x-7-5-8-Endura-Aluminum-Column-Round-Shaft-Load-Bearing-21-000-lbs-Non-Tapered-Fluted-Gloss-White-EA0808ANFSATUTU/301315907
    cost = cp.sum(aluminumColumns)*278
    # cost of steel columns from https://web.archive.org/web/20161210125922/http://www.homedepot.com:80/p/Tiger-Brand-8-ft-to-8-ft-4-in-Adjustable-Steel-Building-Support-Column-3-in-O-D-3A-8084/202086528
    cost += cp.sum(steelColumns)*64.90
    # cost of each square meter tile from https://www.lowes.com/pd/AdvanTech-Flooring-23-32-CAT-PS2-10-Tongue-and-Groove-OSB-Subfloor-Application-as-4-x-8/50126556
    # we buy 3 boards at 54.30, and divide by 2.93392603407 to get the cost per square meter tile
    cost += 3*54.3/2.93392603407*xLength*yLength*floors
    # cost of oak tree saplings per acre
    # 50 trees per acre from the lowest figure from page 1 of https://www.in.gov/dnr/forestry/files/underplantingoak.pdf,
    # priced at 18.99 each from https://sequoiatrees.com/products/valley-oak-medium-tree-seedling?variant=30222711062591&currency=USD
    cost += 50*18.99*oakTreeAcres
    # slash pine cost per acre from page 3 of https://web.archive.org/web/20231126224531id_/https://bugwoodcloud.org/bugwood/productivity/pdfs/SeriesPaper5.pdf
    cost += slashPineAcres*(55+110)
    #eucalyptus density is assumed to be identical to oak density at 50 trees per acre from https://www.in.gov/dnr/forestry/files/underplantingoak.pdf
    # cost is 8.99 each from https://sequoiatrees.com/products/rainbow-eucalyptus-mini-grow-kit
    cost += 50*8.99*eucalyptusTreeAcres
    # asphalt parking lot cost of 2$ per square foot from https://www.miconcrete.org/concrete-parking-lot-and-your-business
    # 15 square meters are in a parking space and 162 feet is approximately 15 square meters, so the cost is 324 dollars per space.
    cost += ((xLength*yLength*floors)/9)*324
    
    # constraints
    constraints = []
    
    # CO2 constraint measured in metric tons
    # aluminum and steel column figures from https://www.wesa.fm/development-transportation/2017-08-31/aluminum-production-leaves-a-big-carbon-footprint-so-alcoa-is-adapting-with-sustainable-products#:~:text=For%20each%20ton%20of%20steel%20produced%2C%202%20tons%20of%20carbon%20is%20emitted.%20And%20for%20each%20ton%20of%20aluminum%2C%20the%20worldwide%20average%20is%2011.7%20tons%20of%20carbon%20emitted
    # each aluminum column is 30 pounds, equivalent to 0.0136078, and 0.0136078*11.7 = 0.15921126
    # each steel column is 35 pounds, equivalent to 0.0158757, and 0.0158757*2 = 0.0317514
    # slash pine carbon absorbtion per acre from https://extension.psu.edu/carbon-accounting-in-forest-management#:~:text=100%2C000%20pounds%20carbon%20per%20acre%20%C3%B7%2045,tons%20of%20CO2%20emissions%20avoided
    # 3.69 metric tons times 45 years is 166.05 metric tons in total
    # the carbon emissions of a typical office building per square meter from https://www.environmentenergyleader.com/2007/10/epa-tool-estimates-greenhouse-gas-emissions-of-commercial-buildings/#:~:text=a%20look%20at%20a%20typical%20office%20building%20in%20the%20New%20England%20region%20shows%20that%20the%20building%20contributes%2020%20pounds%20of%20CO2%20per%20square%20foot
    # 10.7639 square feet in a square meter time 20 pounds per square foot, converting the output to metric tons, gives 0.0976484582 metric tons
    # oak tree carbon absorbtion per tree from https://www.greenereveryday.co.uk/carbon-offsetting#:~:text=The%204.5%20tons%20of%20C%20in%20the%20Oak%20tree%20has%20required%20the%20sequestration%20of%2016.5%20tons%20of%20CO2.%20Spread%20over%20100%20years
    # oak carbon sequestration per hectare from https://winrock.org/flr-calculator/
    # 1000 hectares (about 2471 acres) absorb about 9500 metric tons of CO2 per year, so 
    # an acre of oak trees will absorb about 3.8446 metric tons of CO2 per year.
    # assuming a 100 year lifespan and consistent carbon sequestration over that time, 
    # an acre of oak trees will absorb 384.46 metric tons of CO2 over its lifetime.
    # eucalyptus carbon sequestration per hectare from https://winrock.org/flr-calculator/
    # the calculations for eucalyptus are similar to oak trees, absorbing 37800 metric tons of CO2 per 100 hectares per year and
    # absorbing 15.176 metric tons of CO2 per acre per year and 1138 tons over its lifetime of 75 years.
    # the parking lot size of the building is defined to be 1 parking spot per 9 tiles of space, rounded up,
    # and with emissions of 52264 metric tons of CO2 over 560000 square meters, so
    # the emissions are approximately 0.09333 metric tons per square meter, from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4809014/.
    # the size of a parking space is approximately 15 square meters, so the CO2 cost of a parking spot is appoximately
    # 1.4 metric tons per parking space.
    constraints.append(cp.sum(steelColumns)*0.0317514 + cp.sum(aluminumColumns)*0.15921126 + xLength*yLength*floors*0.0976484582 + ((xLength*yLength*floors)/9)*1.4 - oakTreeAcres*384.46 - slashPineAcres*166.05 - eucalyptusTreeAcres*1138.20 <= 0)
    
    # columns supporting each floor
    # aluminum column support figure from https://www.homedepot.com/p/Afco-8-x-7-5-8-Endura-Aluminum-Column-Round-Shaft-Load-Bearing-21-000-lbs-Non-Tapered-Fluted-Gloss-White-EA0808ANFSATUTU/301315907#:~:text=bearing%20limit%20(lb.)-,21000,-Material
    # 21000 pounds has been converted to metric tons
    # steel column support figure from https://www.homedepot.com/p/Tiger-Brand-8-ft-to-8-ft-4-in-Adjustable-Steel-Building-Support-Column-3-in-O-D-3A-8084/202086528#:~:text=maximum%20extension%20(lb.)-,11200%20lb,-Maximum%20load%20at
    # 11200 pounds has been converted to metric tons
    # we want to be able to support at least 1.5 times the load amount
    constraints.append(cp.sum(aluminumColumns)*9.5254398 + cp.sum(steelColumns)*5.0802345 >= 1.5*floors*(subflooringTileWeight+floorWeight)*xLength*yLength)

    # nonnegativity
    constraints.append(aluminumColumns >= 0)
    constraints.append(steelColumns >= 0)

    # constraints to ensure biodiversity amongst the tree species
    # no tree can be planted twice as much as any other tree
    constraints.append(oakTreeAcres>=(1/2)*eucalyptusTreeAcres)
    constraints.append(oakTreeAcres<=2*eucalyptusTreeAcres)

    constraints.append(oakTreeAcres>=(1/2)*slashPineAcres)
    constraints.append(oakTreeAcres<=2*slashPineAcres)
    
    constraints.append(eucalyptusTreeAcres>=(1/2)*slashPineAcres)
    constraints.append(eucalyptusTreeAcres<=2*slashPineAcres)
    
    # create and solve problem
    problem = cp.Problem(cp.Minimize(cost), constraints)
    problem.solve(verbose = True)
    
    logs.append("Parameters given: " + str(floors) + " floor, " + str(xLength) + " meter x length, " + str(yLength) + " meter y length.")
    logs.append("\nCost of materials and offsets (measured in USD): $" + "{:.2f}".format(round(cost.value, 2)))
    logs.append("\nColumns (measured in quantity):")
    logs.append("Aluminum columns needed: "+str(sumMatrix(aluminumColumns.value)))
    logs.append("Steel columns needed: "+str(sumMatrix(steelColumns.value)))
    logs.append("\nCarbon offsets (measured in acres):")
    logs.append("Oak tree acres: " + str(abs(oakTreeAcres.value)))
    logs.append("Slash pine acres: " + str(abs(slashPineAcres.value)))
    logs.append("Eucalyptus tree acres: " + str(abs(eucalyptusTreeAcres.value)))
    logs.append("Number of parking spaces needed: " + str(int(xLength*yLength*floors/9)))

# get arguments from command line
if len(sys.argv) == 4 or len(sys.argv) == 5:
    # extract command-line arguments
    floors = int(sys.argv[1])
    xLength = int(sys.argv[2])
    yLength = int(sys.argv[3])
    calculate(floors, xLength, yLength)
else:
    print("Invalid command-line arguments. Follow this format: python script.py floors xLength yLength")
    randomFloors = random.randint(10, 50)
    randomXLength = random.randint(10, 50)
    randomYLength = random.randint(10, 50)
    print("Running randomized values: floors=" + str(randomFloors) + " xLength=" + str(randomXLength) + " yLength=" + str(randomYLength))
    calculate(randomFloors, randomXLength, randomYLength)

# only run if it is a test case
# example of a command-line run that updates a test: python3 "linear_program.py" 4 20 30 1
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
