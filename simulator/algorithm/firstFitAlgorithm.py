from algorithm.algorithm import Algorithm
from pointCalculator import PointCalculator
import numpy as np
import math
from operator import attrgetter
import copy

class FirstFitAlgorithm(Algorithm):

    def __init__(self, cameras, things, point=0.3):
        super(FirstFitAlgorithm,self).__init__(cameras,things,point)
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
            cVAngle = math.degrees(c.getVAngle())

            monitor = []
            for o2 in sort:
                # create a fov for sector
                
                fov = {}
                fov['side'] = []
                fov['center'] = [o2[1]]
                fov['weight'] = o2[1].getPriority()
                
                removeQueue = []
                for o in sort:
                    # if thing in the anchor's sector
                    if o[1].getIndex() == o2[1].getIndex():
                        continue

                    oAngle = o[0]
                    if o2[0] > cVAngle and oAngle <= cVAngle:
                        oAngle += 360

                    if abs(oAngle - o2[0]) <= cVAngle * c.getRatio() / 2 :
                        fov['center'].append( self.getSelfThing(o[1]))
                        fov['weight'] += o[1].getPriority()
                    elif abs(oAngle - o2[0]) <= cVAngle / 2:
                        fov['side'].append( self.getSelfThing(o[1]))
                        fov['weight'] += o[1].getPriority() * self.point
                    else :
                        continue

                monitor.append(fov)

            c.setMonitor(monitor)


        while self.isCameraTimeEnough():
            
            targetThing = max(self._things, key=lambda t: t.getPriority() * t.getRemainTime() )
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