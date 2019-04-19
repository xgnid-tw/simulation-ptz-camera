from mapObject import MapObject

class Camera(MapObject):

    def __init__(self, index, period, rMax, vAngle, centerRatio):
        super(Camera,self).__init__('C')
        self.__index = index
        self.__period = period
        self.remainPeriod = period
        self.__things = []
        self.__rMax = rMax
        self.__vAngle = vAngle
        self.__monitor = []
        self.__centerRAtio = centerRatio

    def getRMax(self):
        return self.__rMax

    def getVAngle(self):
        return self.__vAngle
    
    def getPeriod(self):
        return self.__period

    def getRemainPeriod(self):
        return self.remainPeriod

    def getIndex(self):
        return self.__index

    def getRatio(self):
        return self.__centerRAtio

    # things operations 
    def addDetectableThing(self, thing):
        self.__things.append(thing)

    def getThings(self):
        return self.__things

    def setThingTime(self, centerThing, sideThing, time):
        fov = {}
        fov['center'] = centerThing
        fov['side'] = sideThing
        fov['time'] = time
        self.__monitor.append(fov)
        self.remainPeriod -= time
        if self.remainPeriod < 0:
            raise Exception("camera remain negative")

    def setRemainPeriod(self, time):
        self.remainPeriod = time

    def removeDetectableThing(self, thing):
        self.__things.remove(thing)

    """
        monitor:
        [
            {
                "center" : [thingnumbers],
                "side" : [thingnumbers],
                "time" : integer
            },
            ...
        ]
    """
    def getMonitor(self):
        return self.__monitor

    def setMonitor(self, monitor ):
        self.__monitor = monitor

    def removeFov(self,fov):
        self.__monitor.remove(fov)
            
