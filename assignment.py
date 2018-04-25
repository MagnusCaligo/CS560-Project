import math
import cv2
import numpy as np
import time
import random
import sys

size = 233

class Hexagon:
    def __init__(self):
        self.topLeftHex = None
        self.topHex = None
        self.topRightHex = None
        self.botRightHex = None
        self.botHex = None
        self.botLeftHex = None


        self.index = 0 # each hexagon has an index. start at zero.
        self.value = 0 # the cost of traveling to this hexagon from a neighbor.
        self.visited = False # after checking all of this hexagon's neighbors, it has been visited.
        self.totalValue = 999999 # an initial value for comparison for the first total path value
        self.previousNode = None # since each path is a linked list, we need to be able to backtrack to the previous node
        
        
        self.drawn = False
        self.size = 20
        self.distance = 50
        

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
        self.shortestPath = [] # will be the linked list of the indices of the shortest path of hexagons.
        inputFile = open('input.txt')
        input = []
		
        for line in inputFile.readlines():
            chomp = line.rstrip('\n')
            input.append(chomp.split(" ")) # input is now an array of arrays, each array within input being a row from the file

        i = 0
        for row in input:
            self.hexagons.append(Hexagon())
            self.hexagons[i].value = int(row[1])
            self.hexagons[i].index = int(row[0])
            i += 1
			# self.hexagons[i].value = random.randrange(-1,5,1) # RANDOM VALUE GENERATED. adds a new hexagon.
			# self.hexagons[i].index = i # give that hexagon an index

		# assign the neighbors of the current hexagon.
        for i,v in enumerate(self.hexagons):
            if i - 8 >= 0 and (i-15)%15 != 0: # if the current hexagon is in the top row, or the left column, don't set a top left neighbor
                v.topLeftHex = self.hexagons[i-8] # set the top left neighbor
            if i - 15 >= 0: # if the current hexagon is in the top row, don't set a top neighbor
                v.topHex = self.hexagons[i-15] # set the top neighbor
            if i - 7 >= 0: # if the current hexagon is in the top row, don't set a top right neighbor
                v.topRightHex = self.hexagons[i-7] # set the top right neighbor
            if i + 8 < size:  # if the current hexagon is in the bottom row, don't set a bottom right neighbor
                v.botRightHex = self.hexagons[i+8] # set the bottom right neighbor
            if i +15 < size: # if the current hexagon is on the bottom row, don't set a bottom neighbor
                v.botHex = self.hexagons[i+15] # set bottom neighbor
            if i + 7 < size and (i)%15 != 0: # if the current hexagon is on the bottom row or left column, don't set a bottom neighbor
                v.botLeftHex = self.hexagons[i+7] # set bottom left neighbor
                
            if (i-7)%15 == 0: # if the current hexagon is in the right column, don't set a top right and bottom right neighbor
                v.topRightHex = None
                v.botRightHex = None

    
    def findShortestPath(self):
        
        # Find the smallest and non visited hexagon in the map
        # This is so that all the paths grow at approximately the same pace
        def findSmallestNotVisited():
            smallest = self.hexagons[7] # Set this as an initial comparison value
            for hex in self.hexagons:
                if hex.visited == False and hex.totalValue < smallest.totalValue:
                    smallest = hex
            return smallest
        
        current = self.hexagons[225]
        current.visited = True
        current.totalValue = 0
		
        output = open("output.txt", "w") 
		
        while True:
            # print "Looking at node", current.index
            if current == self.hexagons[7]: # if we've made it to the destination hexagon
                if current.previousNode == None: # Failed to find smallest; i.e. no more left in not visited
                    return -1
                else:
                    cost = current.totalValue
                    while True:
                        # print current.index  # this prints the smallest path. shortestPath contains all the indeces of the shortest path
                        self.shortestPath.insert(0, current.index)
                        current = current.previousNode
                        if current == None:
                            break
                    for node in self.shortestPath:
                        output.write(str(node))
                        output.write("\n")
                    output.write("MINIMAL-COST PATH COSTS: %d" % (cost))
                    output.close()
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
                if neighbor.value < 0: # if neighbor is a -1, then we can't go through it
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
