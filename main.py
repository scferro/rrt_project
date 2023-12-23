from tree import Tree
from rrt import RRT
import random
import imageio.v3 as iio

# User defined variables
xRange = [0, 100] #set the size of the display area
yRange = [0, 100] #set the size of the display area
filepath = 'Documents/rrt_project/N_map.png' #filepath for image file
delta = 1
angleDelta = 1
timeDelta = 0.1
numVert = 2000
numObs = random.randint(20, 40)
minRadius = 3
maxRadius = 12
pixelSubGrid = 3
buffer = 1

# Initialize variables 
checkValid = False
checkImage = False
counter = 0
pointsList = []

def create_preview(nextTask):
    print("Generating preview. Goal position is shown in blue and Start position is shown in orange.")
    print("Close preview to " + nextTask + ".")
    print("")
    tree.plot_points()

while checkImage == False:
    askRandom = bool(input("Would you like to use enter positions for the start and goal? Press [Enter] to continue with a random start and goal, or enter anything to manually enter start and goal positions:"))
    #set start and goal positions, random or user defined
    if askRandom == True:
        print("User input selected. X values should be in the range " + str(xRange) + ". Y values should be in the range " + str(yRange) + ".")
        print("")
        startPoint = [0,0]
        goal = [0,0]
        startPoint[0] = float(input("Enter start point X coordinate: "))
        startPoint[1] = float(input("Enter start point Y coordinate: "))
        goal[0] = float(input("Enter goal X coordinate: "))
        goal[1] = float(input("Enter goal Y coordinate: "))
        print("")
    else:
        print("Generating random start and goal...")
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
    createCircles = False
    circlesComplete = False

    while randomObstacles == importImage == createCircles:
        print("Select the method for generating obstacles. You must select one method to continue.")
        print("")
        randomObstacles = False
        importImage = False
        createCircles = False
        circlesComplete = False

        randomObstacles = bool(input('Generate random circular obstacles? Enter anything here to generate random obstacles or press [Enter] to skip: '))
        if randomObstacles == True:
            print("Random obstacles will be generated.")
        else:
            print("Not generating random obstacles.")
            print("")
            importImage = bool(input('Generate obstacles based on a binary image? Enter anything here to use the image to create obstacles or press [Enter] to skip. The image that will be used is stored at ' + filepath + ': '))
            if importImage == True:
                print("Obstacles will be generated based on image.")
            else:
                print("Not generating obstacles based on binary image.")
                print("")
                createCircles = bool(input('Manually enter data for circular obstacles? Enter anything here to enter data for obstacles or press [Enter] to skip: '))
                if createCircles == True:
                    print("Obstacles will be generated based on user inputs. You will need to enter [x,y] coordinates for the center and a radius length.")
                else:
                    print("Not generating obstacles based on user inputs.")
            print("")

    while checkValid == False:
        tree.change_goal_start(startPoint, goal)
        #create obstacles
        obsCount = 0
        if randomObstacles == True:
            while obsCount < numObs:
                tree.create_obstacle_random(maxRadius, minRadius)
                obsCount += 1
        elif importImage == True:
            im = iio.imread(filepath)
            xStart = (xRange[1] - im.shape[1])/2
            yStart = (yRange[1] + im.shape[0])/2 
            tree.create_obs_from_image(im, yStart, xStart, pixelSubGrid)
        elif createCircles == True:
            obsCount = 1
            while circlesComplete == False:
                xObs = float(input("Please input X coordinate of obstacle " + str(obsCount) + ": "))
                yObs = float(input("Please input Y coordinate of obstacle " + str(obsCount) + ": "))
                rad = float(input("Please input radius of obstacle " + str(obsCount) + ": "))
                tree.create_obstacle(xObs, yObs, rad)
                print("")
                circlesComplete = not bool(input("Currently " + str(obsCount) + " obstacle(s) created. Would you like to create another? Enter anything here to create another obstacle or press [Enter] to continue: "))
                obsCount += 1
                

        checkValid = False
        checkImage = False
        
        #check that start and goal are not within an obstacle and that there is not a direct path between them. create new obstacles and points if there is conflict
        obsList = tree.all_obstacles()
        checkValid = rrt.check_point(startPoint, obsList)
        print(checkValid)
        if checkValid == True:
            checkValid = rrt.check_point(goal, obsList)
            print(checkValid)
            if checkValid == True:
                if createCircles == False:
                    checkValid = not rrt.obstacle_check(goal, startPoint, obsList, buffer) 
                else:
                    checkValid = True
                print(checkValid)

        if importImage == True:
            if checkValid == True:
                checkImage = rrt.image_check(goal, im, xStart, yStart)
                if checkImage == True:
                    checkImage = rrt.image_check(startPoint, im, xStart, yStart)
                    if checkImage == False and askRandom == True:
                        print("Start position is within obstacle area of image. Please review the preview and select a new Start location. ")
                        create_preview("continue")
                    elif checkImage == False and askRandom != True:
                        startPoint = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])] 
                        goal = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])]
                        checkValid = False
                elif checkImage == False and askRandom == True:
                    print("Goal position is within obstacle area of image. Please review the preview and select a new Goal location. ")
                    create_preview("continue")
                elif checkImage == False and askRandom != True:
                    startPoint = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])] 
                    goal = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])]
                    checkValid = False
            elif checkValid == False and askRandom == True and createCircles != True:
                print("Goal and/or Start position is not valid. Please review the preview and select a new Goal and/or Start location. ")
                create_preview("continue")
                checkValid = True
            elif checkValid == False and askRandom != True:
                startPoint = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])] 
                goal = [random.randint(xRange[0], xRange[1]), random.randint(yRange[0], yRange[1])]
        else:
            checkImage = True

print("Puzzle created successfully!")
create_preview("run solver")

#create points using RRT algo
checkComplete = False
while (counter < numVert) and (checkComplete == False):
    pointsList = tree.all_points()
    obsList = tree.all_obstacles()
    validPoint = False
    while validPoint == False:
        newPoint, closePoint = rrt.generate_point_simple(xRange[0], xRange[1], yRange[0], yRange[1], pointsList, delta)
        validPoint = rrt.obstacle_check(newPoint, closePoint, obsList)
    tree.add_point(newPoint)
    tree.add_link(closePoint, newPoint)
    checkComplete = rrt.obstacle_check(goal, newPoint, obsList)
    counter+= 1
    print(counter)

#if goal is accessible, add link to goal
if checkComplete == True:
    tree.add_link(newPoint, goal)
    tree.set_solved(True)
    tree.find_solution()
    print("Task accomplished using " + str(counter) + " links.")
    print("Generated solution plot. Correct path to the goal is shown in blue, incorrect paths are red.")
else:
    print("No solution found.")

#plot output
tree.plot_points()