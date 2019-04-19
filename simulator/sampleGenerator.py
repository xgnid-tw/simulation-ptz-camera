import random
import numpy as np
from camera import Camera
from thing import Thing
import math

class SampleGenerator:
    SG_CAMERA_TIME = 10
    SG_CAMERA_RMAX = 5
    SG_CAMERA_VANGEL = np.pi / 3
    SG_CAMERA_RATIO = 1/3


    """initialize mbc algorithm 

    Args:
        grid (Grid): the map
        mapObject (mapObject): the thing insert to the grid
        amount (int): the amount of mapObject
        candidates (int): the number of candidates
    """
    def __init__(self, grid, candidate=100, vangel= np.pi/3 , ratio = 1/3, sampleType = 0):
        self.__grid = grid
        self.__candidate = candidate
        self.SG_CAMERA_VANGEL = vangel
        self.SG_CAMERA_RATIO = ratio
        # sample type 0 = uniform , 1 = extreme(1:70% 5:20% 10:10% )
        self.__sampleType = sampleType

    def prioritySample(self, amount):
        rat = [ [1/3,1/3,1/3] , [0.7,0.2,0.1]]
        s = []

        for i in range(0, math.floor(rat[self.__sampleType][0] * amount )):
            s.append(1)
        
        for i in range(0, math.floor(rat[self.__sampleType][1] * amount )):
            s.append(5)

        for i in range(0, math.floor(rat[self.__sampleType][2] * amount )):
            s.append(10)
    
        for i in range(len(s), amount):
            s.append(random.choice([1,5,10]))
        
        return s

    def distance2(self, pt1, pt2):
        return (pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2 

    def pointVaild(self, pt, all_pt , r ):
        for p in all_pt:
            if r**2 > self.distance2(pt, p.getPosition()):
                return False
        return True

    def distanceOfTwoObject(self, mapObject1, mapObject2):
        return self.distance2(mapObject1.getPosition(), mapObject2.getPosition() )

    def generateThingTimeSample(self, amount, total):
        divider = sorted(random.sample(range(1,total), amount-1))
            
        return [ a-b for a,b in zip(divider + [total], [0] + divider)]
    
    """
    random generate point in the distance from indx between radius/2 to radius, and check whether the point is near by all_pt

    Args:
        idx (mapObject): random select 
        all_pt (lis of mapObject): all generated pt
        idx_radius (double): the radius of idx , which decide the pt position range
        pt_radius (double): the distance between pts
    Return:
        pt (list) [x,y] : position set of mapObject, it placed from idx between radius/2 to radius
    """
    def getPoint(self, idx, all_pt, idx_radius, pt_radius):
        width , height = self.__grid.getMap()
        idxpt = idx.getPosition()
        
        j = 0
        while j < self.__candidate :
            rho, theta = np.random.uniform(idx_radius/2, idx_radius) , np.random.uniform(0, 2*np.pi)
            pt = [idxpt[0] + rho*np.cos(theta) , idxpt[1] + rho*np.sin(theta)]

            if not (0 < pt[0] < width and 0 < pt[1] < height) :
                continue
            if self.pointVaild( pt, all_pt, pt_radius/2 ):    
                return pt
            j += 1
        return False


    def connectThingToCameras(self, thing, cameras):
        for c in cameras:
            if c.getRMax() ** 2> self.distanceOfTwoObject(thing, c):
                thing.addDetectedCamera(c)
                c.addDetectableThing(thing)


    """
    random camera sampling in grid 

    Args:
        cameraAmount (int): the amount of camera
    """
    def cameraSampling(self, cameraAmount):
        inactiveP = []
        activeP = []
        
        cameras = []
        for i in range(0, cameraAmount):
            cameras.append(Camera(i, self.SG_CAMERA_TIME, self.SG_CAMERA_RMAX, self.SG_CAMERA_VANGEL, self.SG_CAMERA_RATIO ))
        width, height = self.__grid.getMap()
        # random select a point as base camera point 
        self.__grid.insertObject(cameras[0], [width/2, height/2] )
        #self.__grid.insertObject(cameras[0], [np.random.uniform(0,width), np.random.uniform(0,height)] )
        activeP.append(cameras[0])

        i = 1
        while activeP and i < cameraAmount :
            idx = np.random.choice(activeP)
            pt = self.getPoint(idx, activeP + inactiveP, idx.getRMax(), idx.getRMax())
            if pt:
                self.__grid.insertObject(cameras[i], pt)
                activeP.append(cameras[i])
                i += 1
            else :
                activeP.remove(idx)
                inactiveP.append(idx)

        #samples = [p.getPosition() for p in (activeP + inactiveP)]

    """random thing sampling in grid 

    Args:
        thingAmount (int): the amount of thing
    """
    def thingSampling(self, thingAmount):
        inactiveP = []
        activeP = []
        placedThing = []
        cameras = self.__grid.getMapObj('C')

        things = []

        # 取得權重設定之陣列
        priSample = self.prioritySample(thingAmount)
        random.shuffle(priSample)
        
        # 根據相機的Rmax利用三角函數算出物體的距離
        t_dis = np.sin(self.SG_CAMERA_VANGEL/2)*self.SG_CAMERA_RMAX/(np.sin(self.SG_CAMERA_VANGEL/2)+1)

        # initial things
        cameraTotal = sum( c.getPeriod() for c in cameras )
        time = self.generateThingTimeSample(thingAmount, cameraTotal)
        for i in range(0, thingAmount):
            if time[i] >= self.SG_CAMERA_TIME :
                time[i] = self.SG_CAMERA_TIME/2
            
            things.append(Thing(i,time[i], t_dis, priSample.pop() ))
            
        width, height = self.__grid.getMap()

        # random select a camera as first base point
        cs = np.random.choice(cameras)
        cspt = cs.getPosition()

        # random get a length from 0 to Rmax and get a angel from 0 to 2pi
        rho, theta = np.random.uniform(0, cs.getRMax()) , np.random.uniform(0, 2*np.pi)
        pt = [ cspt[0] + rho*np.cos(theta) , cspt[1] + rho*np.sin(theta) ]
        self.__grid.insertObject(things[0], pt)
        self.connectThingToCameras(things[0], cameras)

        # at first , all cameras are seclectable points
        activeP.extend(cameras)

        i = 1
        while len(inactiveP) < len(cameras) and i < thingAmount :

            # random choose a index point from active points group
            idx = np.random.choice(activeP)

            # get a point in the range of index point , and verify wethter that point have distance from other point 
            pt = self.getPoint(idx, placedThing, idx.getRMax() , t_dis*2)
            if pt:
                
                # get a position , set one thing to the position
                self.__grid.insertObject(things[i], pt)

                # append this new thing to group of things
                placedThing.append(things[i])
                self.connectThingToCameras(things[i], cameras)
                i += 1
            else :
                
                # if all candicate are incompatible , set this index point to inactive group
                activeP.remove(idx)
                inactiveP.append(idx)
            