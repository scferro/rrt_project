import matplotlib.pyplot as plt
import random

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

    def add_point(self, newPoint):
        #add point to tree points list
        self.points.append(newPoint)

    def add_link(self, point1, point2):
        #add pair of two points to the links list
        self.links.append([point1, point2])

    def create_obstacle(self, maxRadius, minRadius):
        #generate obstacles at random position with radisu in specified range
        self.obstacles.append([random.randint(self.xMin, self.xMax), random.randint(self.yMin, self.yMax), random.randint(minRadius, maxRadius)])

    def all_points(self):
        #return the list of tree points
        return self.points

    def all_obstacles(self):
        #return the list of all obstacles
        return self.obstacles

    def plot_points(self): 
        #function to plot the points
        fig, ax = plt.subplots()

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
            ax.plot(linkX, linkY)

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
        plt.show()
