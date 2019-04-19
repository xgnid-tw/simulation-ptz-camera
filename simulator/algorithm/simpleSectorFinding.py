from algorithm.algorithm import Algorithm
from pointCalculator import PointCalculator
import numpy as np
import math
from operator import attrgetter

class SimpleSectorFinding(Algorithm):

    def __init__(self, cameras, things, point=0.3):
        super(SimpleSectorFinding,self).__init__(cameras,things,point)
        monitor = []

    def run(self):
        # enumerate all camera 
        for c in self._cameras:
            # sort by clockwise angle
            sort = self.cuppleThingWithAngle(c)
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
                if c.getRatio() == 1 :
                    fov['side'] = []
                    fov['center'] = [o2[1]]
                else:
                    fov['side'] = [o2[1]]
                    fov['center'] = []
                
                fov['weight'] = o2[1].getPriority() * self.point
                
                removeQueue = []
                for o in sort:
                    # if thing in the anchor's sector

                    if o[0] > o2[0] and o[0] - o2[0] < cVAngle :
                        removeQueue.append(o)
                        # check the thing position
                        #print(  cVAngle * c.getRatio() ,  cVAngle/2*(1+c.getRatio()) )
                        if o[0] - o2[0] >= cVAngle/2*(1-c.getRatio()) and  o[0] - o2[0] <= cVAngle/2*(1+c.getRatio()) :
                            fov['center'].append(o[1])
                            fov['weight'] += o[1].getPriority()
                        else :
                            fov['side'].append(o[1])
                            fov['weight'] += o[1].getPriority() * self.point
                            
                for o in removeQueue:
                    sort.remove(o)
                monitor.append(fov)

                if index+1 < len(sort):
                    index = index + 1
                else :
                    index = 0
            c.setMonitor(monitor)

        while self.isCameraTimeEnough():
            
            targetThing = max(self._things, key=lambda t: t.getPriority() * t.getRemainTime() )
            
            csLargest = targetThing.getCameras()
            if len(csLargest) == 0 :
                self._things.remove(targetThing)
                continue
            elif len(csLargest) > 1:
                cLargestTuple = max([ self.findFovOfCamera(c,targetThing) for c in csLargest ],key=lambda t : t[2].getRemainPeriod())
            else:
                cLargestTuple = self.findFovOfCamera(csLargest[0],targetThing)

            # set time
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