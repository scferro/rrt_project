import random 
import math

class RRT:
    def __init__(self):
        pass
    
    def generate_point(self, xMin, xMax, yMin, yMax, pointsList, delta): 
        #function to generate a random point on the plot, find the nearest plotted point, and create a new point in the direction of the random point
        randomPoint = [random.randint(xMin, xMax), random.randint(yMin, yMax)]
        minDist = 10000000
        closestPoint = [0,0]
        for point in pointsList:
            dist = math.dist(point, randomPoint)  
            if dist < minDist:
                minDist = dist
                closestPoint = point
        a = delta / minDist
        newPoint = [closestPoint[0] + (a * (-closestPoint[0]+randomPoint[0])), closestPoint[1] + (a * (-closestPoint[1]+randomPoint[1]))]
        return [newPoint, closestPoint]

    def obstacle_check(self, newPoint, closestPoint, obsList):
        goodPoint = True
        for obs in obsList:
            slope = (-closestPoint[1]+newPoint[1])/(-closestPoint[0]+newPoint[0])
            slopePerp = -(-closestPoint[0]+newPoint[0])/(-closestPoint[1]+newPoint[1])
            yInt = closestPoint[1] - (slope * closestPoint[0])
            yIntPerp = obs[1] - (slopePerp * obs[0])
            intersect = [(yIntPerp-yInt)/(slope-slopePerp)]
            intersect.append(slope * intersect[0] + yInt)
            distInt = math.dist([obs[0], obs[1]], intersect)  
            distNewPoint = math.dist([obs[0], obs[1]], newPoint)   
            distClosestPoint = math.dist([obs[0], obs[1]], closestPoint)  
            if (distInt <= obs[2]) and (max(abs(newPoint[0]), abs(closestPoint[0])) > abs(intersect[0]) > min(abs(newPoint[0]), abs(closestPoint[0]))):
                goodPoint = False
            elif (distNewPoint <= obs[2]) or (distClosestPoint <= obs[2]) :
                goodPoint = False
        return goodPoint

    def check_complete(self, goal, newPoint, obsList): 
        goodPoint = True
        for obs in obsList:
            slope = (goal[1]-newPoint[1])/(goal[0]-newPoint[0])
            slopePerp = -(goal[0]-newPoint[0])/(goal[1]-newPoint[1])
            yInt = goal[1] - (slope * goal[0])
            yIntPerp = obs[1] - (slopePerp * obs[0])
            intersect = [(yIntPerp-yInt)/(slope-slopePerp)]
            intersect.append(slope * intersect[0] + yInt)
            distInt = math.dist([obs[0], obs[1]], intersect)  
            #print(str(obs[2]) + "    " + str(distInt) + "    " + str(intersect) + "    " + str(slope) + "    " + str(slopePerp) + "    " + str(yInt) + "    " + str(yIntPerp))
            if (distInt <= obs[2]):
                goodPoint = False
        return goodPoint
    
    def check_point(self, point, obsList):
        goodPoint = True
        for obs in obsList:
            dist = math.dist([obs[0], obs[1]], point)  
            if (dist <= obs[2]):
                goodPoint = False
            print(dist)
        return goodPoint
        