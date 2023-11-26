import cvxpy as cp
import numpy as np
#goals: add a parameter that places the columns away from other columns and away from building edges.
#way to encode the floor shapes: use a numpy boolean grid.
#steps: optimization phase 1 will be determinimng number of columns needed and carbon offset quantities
#optimization phase 2 will be placing the columns in the building.

inputs=["# of floors", ["dimensions of floor n"]]
floor_count=inputs[0]
dimensions=inputs[1]
columns_per_floor=[1,2,3]
columns_pos=[]
cp.Variable(3, integer=True)
constraints=[]
for i in range(floor_count):
    columns_pos.append([])
    for j in columns_per_floor[i]:
        x = cp.Variable(1,integer=True)
        y = cp.Variable(1,integer=True)
        columns_pos[i].append((x,y))
        #constraints to verify that the column connects to both the current floor and the floor it's supporting.
        constraints.append(dimensions[i][y][x]==1)
        constraints.append(dimensions[i+1][y][x]==1)