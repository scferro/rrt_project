import random 
import math

class RRT:
    def __init__(self):
        pass
    
    def generate_point_simple(self, xMin, xMax, yMin, yMax, pointsList, delta): 
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
    
    def generate_point(self, xMin, xMax, yMin, yMax, pointsList, angleDelta, obsList, timeDelta, im, xStart, yStart): 
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
        try:
            slope = (-closestPoint[1]+randomPoint[1])/(-closestPoint[0]+randomPoint[0])
        except ZeroDivisionError as e:
            slope = 2**32
        slopeRad = math.atan(slope)

        obsCheck = False
        counter = 1
        while obsCheck == False:
            slopeRadMod = (math.pi * angleDelta/180) * counter + slopeRad
            slopeMod = math.tan(slopeRadMod)

            intersect = self._find_intersect(slopeMod, closestPoint, randomPoint)
            
            newPoint = [closestPoint[0] + (timeDelta * (-closestPoint[0]+intersect[0])), closestPoint[1] + (timeDelta * (-closestPoint[1]+intersect[1]))]
            obsCheck = self.obstacle_check(newPoint, closestPoint, obsList)
            if obsCheck == True:
                obsCheck = self.image_check(newPoint, im, xStart, yStart)

            if obsCheck == False:
                slopeRadMod = -(math.pi * angleDelta/180) * counter + slopeRad
                slopeMod = math.tan(slopeRadMod)

                intersect = self._find_intersect(slopeMod, closestPoint, randomPoint)
                
                newPoint = [closestPoint[0] + (timeDelta * (-closestPoint[0]+intersect[0])), closestPoint[1] + (timeDelta * (-closestPoint[1]+intersect[1]))]
                obsCheck = self.obstacle_check(newPoint, closestPoint, obsList)
                if obsCheck == True:
                    obsCheck = self.image_check(newPoint, im, xStart, yStart)

            counter += 1
            
        return [newPoint, closestPoint]

    def obstacle_check(self, point1, point2, obsList):
        goodPoint = True
        for obs in obsList:
            try:
                slope = (-point2[1]+point1[1])/(-point2[0]+point1[0])
            except ZeroDivisionError as e:
                slope = 2**32

            intersect = self._find_intersect(slope, point2, obs)            

            distInt = math.dist([obs[0], obs[1]], intersect)  
            distPoint1 = math.dist([obs[0], obs[1]], point1)   
            distPoint2 = math.dist([obs[0], obs[1]], point2)  
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
        
    def image_check(self, point, im, xStart, yStart):
        rows = im.shape[0]
        columns = im.shape[1]
        xPos = round(point[0] - xStart + 0.5)
        if xPos > 99:
            xPos = 99
        yPos = round(-point[1] + yStart + 0.5)
        if yPos > 99:
            yPos = 99
        if (point[0] >= xStart) and (point[0] <= xStart + columns) and (point[1] <= yStart) and (point[1] >= yStart - rows):
            if im[yPos, xPos][0] == 0:
                return False
            else:
                return True
        else:
            return True         

    def _find_intersect(self, slope, point1, point2):
        try:
            slopePerp = -1/slope
        except ZeroDivisionError as e:
            slopePerp = 2**32

        yInt = point1[1] - (slope * point1[0])
        yIntPerp = point2[1] - (slopePerp * point2[0])

        try:
            intersect = [(yIntPerp-yInt)/(slope-slopePerp)]
        except ZeroDivisionError as e:
            intersect = [2**32]
        intersect.append(slope * intersect[0] + yInt)

        return intersect