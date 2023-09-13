from tree import Tree
from rrt import RRT
import random

#set user defined variables
xRange = [0, 200]
yRange = [0, 200]
delta = 1
numVert = 500
numObs = 15
minRadius = 5
maxRadius = 20

checkValid = False

while checkValid == False:
    #set start and goal positions, random or user defined
    startPoint = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])] 
    goal = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])]

    #initialize tree object
    tree = Tree(startPoint, goal, xRange[1], yRange[1], xRange[0], yRange[0])
    rrt = RRT()

    counter = 0
    pointsList = []
    obsCount = 0

    #create obstacles
    while obsCount < numObs:
        tree.create_obstacle(maxRadius, minRadius)
        obsCount += 1
    
    #check that start and goal are not within an obstacle. create new obstacles and points if there is conflict
    obsList = tree.all_obstacles()
    checkValid = rrt.check_point(startPoint, obsList)
    if checkValid == True:
        checkValid = rrt.check_point(goal, obsList)

#create points using RRT algo
checkComplete = False
while (counter < numVert) and (checkComplete == False):
    pointsList = tree.all_points()
    obsList = tree.all_obstacles()
    validPoint = False
    while validPoint == False:
        newPoint, closePoint = rrt.generate_point(xRange[0], xRange[1], yRange[0], yRange[1], pointsList, delta)
        validPoint = rrt.obstacle_check(newPoint, closePoint, obsList)
    tree.add_point(newPoint)
    tree.add_link(closePoint, newPoint)
    checkComplete = rrt.check_complete(goal, newPoint, obsList)
    counter += 1
tree.add_link(newPoint, goal)

#plot output
tree.plot_points()