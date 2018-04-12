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

    def drawHex(self, image, x, y, distance):
        if self.drawn == True:
            return
        cv2.circle(image, (int(x),int(y)), 20, (0,0,0), -1)

        if x == 50 and y == 50:
            cv2.circle(image, (int(x),int(y)), 20, (255, 0,0), -1)

        self.drawn = True

        locations = []
        angle = 180
        for i in range(6):
            locations.append(((distance*math.cos(math.radians(angle))) + x, 
                (distance *math.sin(math.radians(angle))) + y))
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
            #hex.drawHex(image, locations[i][0], locations[i][1], distance )




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
        image = np.zeros((640,480,3), np.uint8)
        image[:, :] = (255, 255,255)

        distance = 50
        self.hexagons[0].drawHex(image, 50, 50, distance)

        while True:
            cv2.imshow("Test", image)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break




map = HexMap()
map.drawHexes()
