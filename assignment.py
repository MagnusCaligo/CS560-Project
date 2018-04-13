import math
import cv2
import numpy as np
import time
import random
import sys

size = 233

class Hexigon:
    def __init__(self):
        self.topLeftHex = None
        self.topHex = None
        self.topRightHex = None
        self.botRightHex = None
        self.botHex = None
        self.botLeftHex = None


        self.index = 0
        self.value = 0
        self.visited = False
        self.totalValue = 999999
        self.previousNode = None
        
        
        self.drawn = False
        self.size = 20
        self.distance = 50
        
    def getLengthOfSnake(self, up):
        if up:
            if self.topLeftHex == None:
                return 1
            else:
                return self.topLeftHex.getLengthOfSnake(False)
        else:
            if self.botLeftHex == None:
                return 1
            else:
                return self.botLeftHex.getLengthOfSnake(True)

    def drawHex(self, image, x, y, shortestPath):
        if self.drawn == True:
            return
        w, h, c = image.shape
        height = h - y
        cv2.circle(image, (int(x),int(y)), self.size, (0,0,0), -1)
        if self.index in shortestPath:
            cv2.circle(image, (int(x),int(y)), self.size, (0,0,255), -1)
            
        
        font                   = cv2.FONT_HERSHEY_PLAIN
        bottomLeftCornerOfText = (int(x) - int(self.size/2), int(y)+int(self.size/2))
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2
        
        cv2.putText(image,str(self.value), 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)

        self.drawn = True

        locations = []
        angle = 150
        for i in range(6):
            locations.append(((self.distance*math.cos(math.radians(angle))) + x, 
                (self.distance *math.sin(math.radians(angle + 180))) + y))
            angle -= 60

        #for i in locations:
        #    cv2.circle(image, (int(i[0]), int(i[1])), 20, (0,0,0), -1)

        self.references = [
            self.topLeftHex, 
            self.topHex, 
            self.topRightHex, 
            self.botRightHex,
            self.botHex, 
            self.botLeftHex,
                ]

        for i, hex in enumerate(self.references):
            if hex == None:
                continue
            if i == 2:
                pass
            if hex.value == 7:
                pass
            height = h - locations[i][1]
            hex.drawHex(image, locations[i][0], locations[i][1], shortestPath)




class HexMap:

    def __init__(self):
        self.hexagons = []
        self.shortestPath = []

        for i in range(size):
            self.hexagons.append(Hexigon())
            self.hexagons[i].value = random.randrange(-1,5,1)
            self.hexagons[i].index = i

        for i,v in enumerate(self.hexagons):
            if i - 8 >= 0 and (i-15)%15 != 0:
                v.topLeftHex = self.hexagons[i-8]
            if i - 15 >= 0: 
                v.topHex = self.hexagons[i-15]
            if i - 7 >= 0:
                v.topRightHex = self.hexagons[i-7]
            if i + 8 < size:
                v.botRightHex = self.hexagons[i+8]
            if i +15 < size:
                v.botHex = self.hexagons[i+15]
            if i + 7 < size and (i)%15 != 0:
                v.botLeftHex = self.hexagons[i+7]
                
            if (i-7)%15 == 0:
                v.topRightHex = None
                v.botRightHex = None
                
        pass
    
    def findShortestPath(self):
        
        def findSmallestNotVisited():
            smallest = self.hexagons[7]
            for hex in self.hexagons:
                if hex.visited == False and hex.totalValue < smallest.totalValue:
                    smallest = hex
            return smallest
        
        current = self.hexagons[225]
        current.visited = True
        current.totalValue = 0
        
        while True:
            print "Looking at node", current.index
            if current == self.hexagons[7]:
                if current.previousNode == None: #Failed to find smallest; i.e. no more left in not visited
                    return -1
                else:
                    while True:
                        print current.index
                        self.shortestPath.append(current.index)
                        current = current.previousNode
                        if current == None:
                            break
                    return 1
            
            current.references = [
                current.topLeftHex, 
                current.topHex, 
                current.topRightHex, 
                current.botRightHex,
                current.botHex, 
                current.botLeftHex,
                    ]
            
            
            for neighbor in current.references:
                if neighbor == None:
                    continue
                if neighbor.value <0:
                    continue
                tentativeValue = current.totalValue + neighbor.value
                if tentativeValue < neighbor.totalValue:
                    neighbor.totalValue = tentativeValue
                    neighbor.previousNode = current
                    
            current.visited = True
            current = findSmallestNotVisited()
        


    def drawHexes(self):
        image = np.zeros((850,700,3), np.uint8)
        image[:, :] = (255, 255,255)
        
        cv2.namedWindow("Test", cv2.WINDOW_AUTOSIZE)

        
        self.hexagons[0].drawHex(image, 50, 50, self.shortestPath)

        while True:
            cv2.imshow("Test", image)
            key = cv2.waitKey(1)
            if key == ord('q'):
                sys.exit(0)
            elif key == ord(' '):
                break
        map = HexMap()
        map.findShortestPath()
        map.drawHexes()


map = HexMap()
map.findShortestPath()
map.drawHexes()
