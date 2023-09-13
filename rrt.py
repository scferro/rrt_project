import random 
import math

class RRT:
    def __init__(self):
        pass
    
    def generate_point(self, xMin, xMax, yMin, yMax, pointsList, delta): 
        #function to generate a random point on the plot, find the nearest plotted point, and create a new point in the direction of the random point
        goodPoint = False
        while goodPoint == False:
            randomPoint = [random.randint(xMin, xMax), random.randint(yMin, yMax)]
            minDist = 10000000
            closestPoint = [0,0]
            for point in pointsList:
                dist = math.dist(point, randomPoint)  
                if dist < minDist:
                    minDist = dist
                    closestPoint = point
            if minDist == 0:
                goodPoint = False
            else:
                goodPoint = True
        a = delta / minDist
        newPoint = [closestPoint[0] + (a * (-closestPoint[0]+randomPoint[0])), closestPoint[1] + (a * (-closestPoint[1]+randomPoint[1]))]
        return [newPoint, closestPoint]

    def obstacle_check(self, point1, point2, obsList):
        goodPoint = True
        print("Checking: ")
        for obs in obsList:
            try:
                slope = (-point2[1]+point1[1])/(-point2[0]+point1[0])
            except ZeroDivisionError as e:
                slope = 2**32
            try:
                slopePerp = -(-point2[0]+point1[0])/(-point2[1]+point1[1])
            except ZeroDivisionError as e:
                slopePerp = 2**32
            yInt = point2[1] - (slope * point2[0])
            yIntPerp = obs[1] - (slopePerp * obs[0])
            try:
               intersect = [(yIntPerp-yInt)/(slope-slopePerp)]
            except ZeroDivisionError as e:
                intersect = [2**32]
            intersect.append(slope * intersect[0] + yInt)
            distInt = math.dist([obs[0], obs[1]], intersect)  
            distPoint1 = math.dist([obs[0], obs[1]], point1)   
            distPoint2 = math.dist([obs[0], obs[1]], point2)  
            print(str([obs[0], obs[1]]) + "    " + str(obs[2]) + "    " + str(distInt) + "    " + str(intersect) + "    " + str(slope) + "    " + str(slopePerp) + "    " + str(yInt) + "    " + str(yIntPerp))
            if (distInt <= obs[2]) and (max(abs(point1[0]), abs(point2[0])) > abs(intersect[0]) > min(abs(point1[0]), abs(point2[0]))):
                goodPoint = False
                break
            elif (distPoint1 <= obs[2]) or (distPoint2 <= obs[2]) :
                goodPoint = False
                break
        return goodPoint
    
    def check_point(self, point, obsList):
        goodPoint = True
        for obs in obsList:
            dist = math.dist([obs[0], obs[1]], point)  
            if (dist <= obs[2]):
                goodPoint = False
                break
        return goodPoint
        