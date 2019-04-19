from mapObject import MapObject

class Thing(MapObject):
    """
    Args:
        minTime(int): the minimun of monitoring time
        rMax(int): radius of things
    """
    def __init__(self, index, minTime, rMax, priority = 1):
        super(Thing,self).__init__('T')
        self.__index = index
        self.__minTime = minTime
        self.__cameras = []
        self.__rMax = rMax
        self.remainTime = minTime
        # 權重 (口試後新增)
        self.__priority = priority
    
    def getIndex(self):
        return self.__index

    def getMinTime(self):
        return self.__minTime

    def getRMax(self):
        return self.__rMax

    def addDetectedCamera(self, camera):
        self.__cameras.append(camera)
    
    def removeDetectedCamera(self, camera):
        self.__cameras.remove(camera)

    def getDetectedCameras(self):
        return self.__cameras

    def getRemainTime(self):
        return self.remainTime

    def setRemainTime(self, time):
        self.remainTime = time

    def getCameras(self):
        return self.__cameras

    def getPriority(self):
        return self.__priority