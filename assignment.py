import math
import cv2
import numpy as np


class Hexigon:
    def __init__(self):
        self.topLeftHex = None
        self.topHex = None
        self.topRightHex = None
        self.botRightHex = None
        self.botHex = None
        self.botLeftHex = None


        self.value = 0
        self.drawn = False
        self.size = 10
        self.distance = 25

    def drawHex(self, image, x, y):
        if self.drawn == True:
            return
        w, h, c = image.shape
        height = h - y
        cv2.circle(image, (int(x),int(y)), self.size, (0,0,0), -1)

        if x == 50 and y == 50:
            cv2.circle(image, (int(x),int(height)), self.size, (255, 0,0), -1)

        self.drawn = True

        locations = []
        angle = 150
        for i in range(6):
            locations.append(((self.distance*math.cos(math.radians(angle))) + x, 
                (self.distance *math.sin(math.radians(angle + 180))) + y))
            angle += 60

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
            height = h - locations[i][1]
            hex.drawHex(image, locations[i][0], locations[i][0])




class HexMap:

    def __init__(self):
        self.hexagons = []

        for i in range(233):
            self.hexagons.append(Hexigon())

        for i,v in enumerate(self.hexagons):
            if i - 8 >= 0:
                v.topLeftHex = self.hexagons[i-8]
            if i - 15 >= 0: 
                v.topHex = self.hexagons[i-15]
            if i - 7 >= 0:
                v.topRightHex = self.hexagons[i-7]
            if i + 8 < 233:
                v.botRightHex = self.hexagons[i+8]
            if i +15 < 233:
                v.botHex = self.hexagons[i+15]
            if i + 7 < 233:
                v.botLeftHex = self.hexagons[i+7]


    def drawHexes(self):
        image = np.zeros((480,640,3), np.uint8)
        image[:, :] = (255, 255,255)
        
        cv2.namedWindow("Test", cv2.WINDOW_AUTOSIZE)

        
        self.hexagons[0].drawHex(image, 50, 50)

        while True:
            cv2.imshow("Test", image)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break




map = HexMap()
map.drawHexes()
