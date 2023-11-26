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
M=1000
e=0.5
for i in range(floor_count):
    columns_pos.append([])
    for j in columns_per_floor[i]:
        pos = cp.Variable(2,integer=True)
        for (y,x) in columns_pos[i]:
            #constraints to create the boolean variables
            b=cp.Variable(3,integer=True)
            constraints.append(b[0]>=0)
            constraints.append(b[0]<=1)
            constraints.append(b[1]>=0)
            constraints.append(b[1]<=1)
            constraints.append(b[2]>=0)
            constraints.append(b[2]<=1)
            xdiff=0
            ydiff=0
            #constraints to ensure different y positions
            constraints.append(xdiff>=0-M*b)
            #constraints to ensure different x positions
            constraints.append(ydiff>=0-M*(1-b))
        columns_pos[i].append(pos)
        #constraints to verify that the column connects to both the current floor and the floor it's supporting.
        constraints.append(dimensions[i][pos[0]][pos[1]]==1)
        constraints.append(dimensions[i+1][pos[0]][pos[1]]==1)