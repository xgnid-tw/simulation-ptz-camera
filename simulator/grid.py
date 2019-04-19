from mapObject import MapObject
from camera import Camera
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Wedge
import numpy as np

class Grid :
    
    """
    Args:
        __width (int): width of grid
        __height (int): height of grid

    Attributes:
        __map (2d-list): grid
        __mapObjs (dictionary{'string':'list'}): the sample in grid with its represent mark to all sample position
    """
    def __init__( self , width , height ):
        self.__width = width
        self.__height = height
        self.__map = []
        self.__mapObjs = {}
                    
    def insertObject( self , mapObject:MapObject , pt ):
        mapObject.setPosition(pt[0],pt[1])
        mark = mapObject.getMark()
        if mark in self.__mapObjs :
            self.__mapObjs[mark].append(mapObject)
        else:
            self.__mapObjs[mark] = [mapObject]
         
    def getMap(self):
        return self.__width, self.__height

    def getMapObj(self, index):
        return self.__mapObjs[index]

    def getMapObject(self):
        return self.__mapObjs['C'],self.__mapObjs['T']

    def setSeed(self, cameras, things):
        self.__mapObjs['C'] = cameras
        self.__mapObjs['T'] = things

        """
        things = self.__mapObjs['T']
        for t in things:
            print( "\tThing %d : time %d , position (%.2f,%.2f)" % (t.getIndex(), t.getMinTime(), t.getPosition()[0] , t.getPosition()[1] ) )
        print( sum( t.getMinTime() for t in things ) )
        """
    def draw(self):
        cameras = self.__mapObjs['C']
        things = self.__mapObjs['T']

        samples = [ o.getPosition() for o in self.__mapObjs['C'] ]
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='equal')
        
        for c in cameras:
       
            x , y = c.getPosition()
            #fov = Wedge( (x,y), c.getRMax(), np.degrees(np.pi/2 - c.getVAngle()) , np.degrees( np.pi/2 + c.getVAngle()), alpha=0.3 )
            ax.add_artist(Circle(xy=(x, y), radius=c.getRMax() , color=(0.15,0.8,0.2,0.05) ))
            #ax.add_artist(fov)
        
        samples = [ o.getPosition() for o in self.__mapObjs['C'] ]
        plt.scatter(*zip(*samples), c='g')

        samples = [ o.getPosition() for o in self.__mapObjs['T'] ]
        plt.scatter(*zip(*samples), c=(0,0,0,1))

        plt.xlim(0, self.__width)
        plt.ylim(0, self.__height)
        plt.axis('off')
        plt.show()