from tree import Tree
from rrt import RRT
import random
import imageio.v3 as iio

# User defined options
importImage = True
randomObstacles = False
randomStart = True
randomGoal = True

# User defined variables
xRange = [0, 100] #set the size of the display area
yRange = [0, 100] #set the size of the display area
filepath = 'Documents/rrt_project/N_map.png' #filepath for image file


# Other variables
delta = 1
numVert = 1000
numObs = random.randint(30, 50)
minRadius = 3
maxRadius = 12
pixelSubGrid = 5


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
    if randomObstacles == True:
        while obsCount < numObs:
            tree.create_obstacle(maxRadius, minRadius)
            obsCount += 1
    if importImage == True:
        im = iio.imread(filepath)
        xStart = (xRange[1] - im.shape[1])/2
        yStart = (yRange[1] + im.shape[0])/2 
        tree.create_obs_from_image(im, yStart, xStart, pixelSubGrid)
    
    #check that start and goal are not within an obstacle and that there is not a direct path between them. create new obstacles and points if there is conflict
    obsList = tree.all_obstacles()
    checkValid = rrt.check_point(startPoint, obsList)
    if checkValid == True:
        checkValid = rrt.check_point(goal, obsList)
        if checkValid == True:
            checkValid = not rrt.obstacle_check(goal, startPoint, obsList)
            if (checkValid == True) and (importImage == True):
                checkValid = rrt.image_check(goal, im, xStart, yStart)
                if (checkValid == True) and (importImage == True):
                    checkValid = rrt.image_check(startPoint, im, xStart, yStart)

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
    checkComplete = rrt.obstacle_check(goal, newPoint, obsList)
    counter+= 1

#if goal is accessible, add link to goal
if checkComplete == True:
    tree.add_link(newPoint, goal)
    print("Task accomploished with " + str(counter) + " links.")
    tree.set_solved(True)
    tree.find_solution()
else:
    print("No solution found.")

#plot output
tree.plot_points()