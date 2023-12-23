import matplotlib.pyplot as plt
import random
import imageio.v3 as iio

plt.style.use('_mpl-gallery')

class Tree:
    def __init__(self, startPoint, goal, xMax, yMax, xMin, yMin):
        #intialize self variables
        self.points = [startPoint]
        self.startPoint = startPoint
        self.goal = goal
        self.obstacles = []
        self.xMax = xMax
        self.xMin = xMin
        self.yMax = yMax
        self.yMin = yMin
        self.links = []
        self.solved = False
        self.solution = []

    def set_solved(self, solved):
        self.solved = solved
        print("Puzzle solved!")

    def change_goal_start(self, startPoint, goal):
        self.startPoint = startPoint
        self.goal = goal
        self.obstacles = []
        self.links = []
        self.solved = False
        self.solution = []
        self.points = [startPoint]

    def find_solution(self):
        if self.solved == True:
            point = self.goal
            pos = 0
            pointList = []
            for link in self.links:
                pointList.append(link[1])
            while point != self.startPoint:
                pos = pointList.index(point)
                link = self.links[pos]
                self.solution.append(link)
                point = link[0]
        else:
            print("Solution not found.")

    def add_point(self, newPoint):
        #add point to tree points list
        self.points.append(newPoint)

    def add_link(self, point1, point2):
        #add pair of two points to the links list
        self.links.append([point1, point2])
        #print("New link added. Total links: " + str(len(self.links)))

    def create_obstacle_random(self, maxRadius, minRadius):
        #generate obstacles at random position with radius in specified range
        self.obstacles.append([random.randint(self.xMin, self.xMax), random.randint(self.yMin, self.yMax), random.randint(minRadius, maxRadius)])

    def create_obstacle(self, xPos, yPos, radius):
        #generate obstacles at random position with radius in specified range
        self.obstacles.append([xPos, yPos, radius])

    def create_obs_from_image(self, im, yStart, xStart, pixelSubGrid):
        #creates obstacles using a binary image file. (xStart,yStart) indicates upper left corner of image on plot
        rows = im.shape[0]
        columns = im.shape[1]
        xPos = 0
        yPos = 0
        subX = 0
        subY = 0
        while xPos < rows:
            yPos = 0
            while yPos < columns:
                yPlus = yPos + 1
                yMinus = yPos - 1
                xPlus = xPos + 1
                xMinus = xPos - 1
                edgeCheck = False

                if (yPlus > 99) or (yMinus < 0) or (xPlus > 99) or (xMinus < 0):
                    edgeCheck = True
                elif (im[yPos, xPos][0] == 0) and (im[yPlus, xPos][0] == 0) and (im[yMinus, xPos][0] == 0) and (im[yPos, xPlus][0] == 0) and (im[yPos, xMinus][0] == 0):
                    edgeCheck = False
                    self.obstacles.append([xStart + xPos + 1/2, yStart - yPos - 1/2, 1/2])
                elif im[yPos, xPos][0] > 0:
                    pass
                else:
                    edgeCheck = True
                
                if (edgeCheck == True) and (im[yPos, xPos][0] == 0):
                    subY = 0
                    while subY < pixelSubGrid:
                        subX = 0
                        while subX < pixelSubGrid:
                            xOffset = 1/(2*pixelSubGrid) + subX/pixelSubGrid - 0.5
                            yOffset = 1/(2*pixelSubGrid) + subY/pixelSubGrid - 0.5
                            self.obstacles.append([xStart + xPos + 1/2 + xOffset, yStart - yPos - 1/2 + yOffset, 1/(2*pixelSubGrid)])
                            subX += 1
                        subY += 1
                yPos += 1
            xPos += 1

    def all_points(self):
        #return the list of tree points
        return self.points

    def all_obstacles(self):
        #return the list of all obstacles
        return self.obstacles

    def plot_points(self): 
        #function to plot the points
        fig, ax = plt.subplots(figsize=(8, 8))
        """ UNCOMMENT THIS TO PLOT INDIVIDUAL TREE POINTS, NOT JUST LINKS
        pointX = []
        pointY = []
        for point in self.points:
            pointX.append(point[0])
            pointY.append(point[1])
        ax.scatter(pointX, pointY)
        """
        #plot links
        for pair in self.links:
            linkX = [pair[0][0], pair[1][0]]
            linkY = [pair[0][1], pair[1][1]]
            ax.plot(linkX, linkY, 'r-')

        #plot solution if solved
        if self.solved == True:
            for pair in self.solution:
                linkX = [pair[0][0], pair[1][0]]
                linkY = [pair[0][1], pair[1][1]]
                ax.plot(linkX, linkY, 'b-')

        #plot obstacles as circles
        for obs in self.obstacles:
            circle = plt.Circle(( obs[0] , obs[1] ), obs[2], color=[0,0,0,1])
            ax.add_artist(circle)

        #plot goal and start 
        ax.scatter(self.goal[0], self.goal[1])
        ax.scatter(self.startPoint[0], self.startPoint[1])

        #set limits for plot display and display the plot
        ax.set_aspect( 1 )
        ax.set(xlim=(self.xMin, self.xMax), ylim=(self.yMin, self.yMax))
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.1, hspace=0.1)
        plt.show()