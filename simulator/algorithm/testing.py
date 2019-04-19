from algorithm.algorithm import Algorithm
from pointCalculator import PointCalculator
import numpy as np
import math
from operator import attrgetter
import copy

class Testing(Algorithm):

    def __init__(self, cameras, things):
        super(Testing,self).__init__(cameras,things)
        monitor = []

    def getSelfThing(self, copyThing):
        for t in self._things:
            if t.getIndex() == copyThing.getIndex():
                return t
                
    def run(self):
        # enumerate all camera 
        for c in self._cameras:
            # sort by clockwise angle
            sort = self.cuppleThingWithAngle(c)
            sort_cp = copy.deepcopy(sort)
            #print(sort)
            cVAngle = math.degrees(c.getVAngle())
            anchor, anchorIndex = self.findFisrtAnchor(sort,cVAngle)

            monitor = []
            index = 0
            while len(sort) :
                try:
                    o2 = sort[anchorIndex]
                except IndexError:
                    o2 = sort[0]

                sort.remove(o2)
                # create a fov for sector
                
                fov = {}
                fov['side'] = []
                fov['center'] = [o2[1]]
                fov['maxThingTime'] = o2[1].getRemainTime()
                fov['value'] = 1
                
                removeQueue = []
                for o in sort_cp:
                    # if thing in the anchor's sector
                    if o[1].getIndex() == o2[1].getIndex():
                        continue

                    oAngle = o[0]
                    if o2[0] > cVAngle and oAngle <= cVAngle:
                        oAngle += 360

                    if oAngle >= o2[0] and oAngle - o2[0] <= cVAngle * c.getRatio():
                        fov['center'].append( self.getSelfThing(o[1]))
                        fov['value'] += 1
                    elif oAngle >= o2[0] and oAngle - o2[0] <= cVAngle/2*(1+c.getRatio()) :
                        fov['side'].append( self.getSelfThing(o[1]))
                        fov['value'] += 0.5
                    elif oAngle < o2[0] and o2[0] - oAngle <= cVAngle/2*(1-c.getRatio()):
                        fov['side'].append( self.getSelfThing(o[1]))
                        fov['value'] += 0.5
                    else:
                        continue

                    if o[1].getMinTime() < fov['maxThingTime']:                            
                        removeQueue.append( o ) 

                for do in removeQueue:
                    for o in sort:
                        if do[1].getIndex() == o[1].getIndex():
                            sort.remove(o)
                monitor.append(fov)

                if index+1 < len(sort):
                    index = index + 1
                else :
                    index = 0
            c.setMonitor(monitor)

        i = 0
        while self.isCameraTimeEnough():
            
            cs = None
            targetThing = None
            for t in self._things:

                if len(t.getDetectedCameras() ) == 1:
                    cs = t.getDetectedCameras()
                    targetThing = t
                    """print( "%d : " %(t.getIndex()), end='')
                    for c in cs :
                        print( "%d " %(c.getIndex()), end='')
                    print()"""

            #largestTimeThing = max(self._things, key=attrgetter('remainTime'))

            if targetThing == None:
                targetThing = max(self._things, key=attrgetter('remainTime'))

            if cs == None :
                cs = targetThing.getCameras()

            csLargest = targetThing.getCameras()
            if len(csLargest) == 0 :
                self._things.remove(targetThing)
                continue
            elif len(csLargest) > 1:
                cLargestTuple = max([ self.findFovOfCamera(c,targetThing) for c in csLargest ], key=lambda t : t[2].getRemainPeriod())
            else:
                cLargestTuple = self.findFovOfCamera(csLargest[0],targetThing)

            self.setTime(cLargestTuple)
            
            
        return self._cameras, self._things
     
        # scheduling according by 
        # 1. max minimum time
        # 2. fov total time
"""
        for c in self._cameras:
            for fov in c.getMonitor() :
                for k,v in fov.items() :
                    if isinstance(v,list):
                        print( k , end='')
                        for t in v:
                            print( " %d," % (t.getIndex()) , end='')
                        print('')
                    else:
                        print( k + ": %d" % (v))
"""