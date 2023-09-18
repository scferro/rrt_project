from tree import Tree
from rrt import RRT
import random
import imageio.v3 as iio

# User defined variables
xRange = [0, 100] #set the size of the display area
yRange = [0, 100] #set the size of the display area
filepath = 'Documents/rrt_project/N_map.png' #filepath for image file
delta = 1
numVert = 2000
numObs = random.randint(30, 50)
minRadius = 3
maxRadius = 12
pixelSubGrid = 3

# Intialize variables 
checkValid = False
checkImage = False
counter = 0
pointsList = []

while checkImage == False:
    askRandom = input("Would you like to use enter positions for the start and goal? Enter [i] to input locations for the start and goal, or press [Enter] to continue with a random start and goal:")
    #set start and goal positions, random or user defined
    if askRandom == "i":
        print("User input selected. X values should be in the range " + str(xRange) + ". Y values should be in the range " + str(yRange) + ".")
        print("")
        startPoint = [0,0]
        goal = [0,0]
        startPoint[0] = float(input("Enter start point X coordinate as an integer: "))
        startPoint[1] = float(input("Enter start point Y coordinate as an integer: "))
        goal[0] = float(input("Enter goal X coordinate as an integer: "))
        goal[1] = float(input("Enter sgoal Y coordinate as an integer: "))
        print("")
    else:
        print("Generating random start and goal.")
        print("")
        startPoint = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])] 
        goal = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])]

    #initialize tree object
    tree = Tree(startPoint, goal, xRange[1], yRange[1], xRange[0], yRange[0])
    rrt = RRT()
    checkValid = False
    checkImage = False
    randomObstacles = False
    importImage = False

    while randomObstacles == importImage:
        print("Select the method for generating obstacles. You must select one method to continue.")
        print("")
        randomObstacles = False
        importImage = False

        randomObstacles = bool(input('Generate random obstacles? Enter anything here to generate random obstacles or [Enter] to skip: '))
        if randomObstacles == True:
            print("Random obstacles will be generated.")
        else:
            print("Not generating random obstacles.")
            print("")
            importImage = bool(input('Generate obstacles based on a binary image? Enter anything here to use the image to create obstacles or [Enter] to skip. The image that will be used is stored at ' + filepath + ": "))
            if importImage == True:
                print("Obstacles will be generated based on image.")
            else:
                print("Not generating obstacles based on binary image.")
            print("")

    while checkValid == False:
        tree.change_goal_start(startPoint, goal)

        #create obstacles
        obsCount = 0
        if randomObstacles == True:
            while obsCount < numObs:
                tree.create_obstacle(maxRadius, minRadius)
                obsCount += 1
        if importImage == True:
            im = iio.imread(filepath)
            xStart = (xRange[1] - im.shape[1])/2
            yStart = (yRange[1] + im.shape[0])/2 
            tree.create_obs_from_image(im, yStart, xStart, pixelSubGrid)

        checkValid = False
        checkImage = False
        
        #check that start and goal are not within an obstacle and that there is not a direct path between them. create new obstacles and points if there is conflict
        obsList = tree.all_obstacles()
        checkValid = rrt.check_point(startPoint, obsList)
        if checkValid == True:
            checkValid = rrt.check_point(goal, obsList)
            if checkValid == True:
                checkValid = not rrt.obstacle_check(goal, startPoint, obsList) 

        if importImage == True:
            if checkValid == True:
                checkImage = rrt.image_check(goal, im, xStart, yStart)
                if checkImage == True:
                    checkImage = rrt.image_check(startPoint, im, xStart, yStart)
                    if checkImage == False and askRandom == "i":
                        print("Start position is within obstacle area of image. Please review the preview and select a new Start location. ")
                        print("Generating preview. Goal position is shown in blue and Start position is shown in orange.")
                        print("Close preview to continue.")
                        print("")
                        tree.plot_points()
                    elif checkImage == False and askRandom != "i":
                        startPoint = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])] 
                        goal = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])]
                        checkValid = False
                elif checkImage == False and askRandom == "i":
                    print("Goal position is within obstacle area of image. Please review the preview and select a new Goal location. ")
                    print("Generating preview. Goal position is shown in blue and Start position is shown in orange.")
                    print("Close preview to continue.")
                    print("")
                    tree.plot_points()
                elif checkImage == False and askRandom != "i":
                    startPoint = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])] 
                    goal = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])]
                    checkValid = False
            elif checkValid == False and askRandom == "i":
                print("Goal and/or Start position is not valid. Please review the preview and select a new Goal and/or Start location. ")
                print("Generating preview. Goal position is shown in blue and Start position is shown in orange.")
                print("Close preview to continue.")
                print("")
                tree.plot_points()
                checkValid = True
            elif checkValid == False and askRandom != "i":
                startPoint = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])] 
                goal = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])]
        else:
            checkImage = True

print("Puzzle created successfully!")
print("Generating preview. Goal position is shown in blue and Start position is shown in orange.")
print("Close preview to run solver.")
tree.plot_points()
print("Running solver...")

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
    tree.set_solved(True)
    tree.find_solution()
    print("Task accomploished using " + str(counter) + " links.")
    print("Generated solution plot. Correct path to the goal is shown in blue, incorrect paths are red.")
else:
    print("No solution found.")

#plot output
tree.plot_points()