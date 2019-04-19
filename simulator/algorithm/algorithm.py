from pointCalculator import PointCalculator
import numpy as np
from operator import attrgetter

class Algorithm:

    def __init__(self, cameras, things, point = 0.3):
        self._cameras = cameras
        self._things = things
        self.point = point

    def result(self):
        points = 0
        success = 0

        for c in self._cameras:
            if c.getRemainPeriod() > 0 and c.getMonitor() != []:
                largestFov = max( c.getMonitor() , key=lambda f: f['weight'] )
                if "time" in largestFov:
                    largestFov['time'] += c.getRemainPeriod()
                else :
                    largestFov['time'] = c.getRemainPeriod()
                #print("largestFov Value %d" % (largestFov['value']))
            for thing in c.getThings():
                if thing.getRemainTime() > 0:
                    success = 1
                    

        for camera in self._cameras:
            for fov in  camera.getMonitor():
                if "time" in fov:
                    points += fov['weight'] * fov['time']

        #if success == 1 :
        #    self.proofreading()


        return [points,success]
        #print("points: %d" % (points))

        """
    check whether any camera have time to monitor
    i.g. : iterating C , check all C can monitored object , 
    then check every camera which that object can be detected.

    C1 - O1
       / O2 - C2
    C3 - O3 /
    """
    def isCameraTimeEnough(self):
        
        for c in self._cameras:
        #    print("camera %d : %d" % (c.getIndex(), c.getRemainPeriod()))
            if c.getRemainPeriod() > 0:
                for t in c.getThings():
        #            print("\tthing %d : %d" % (t.getIndex(), t.getRemainTime()))
                    if t.getRemainTime() > 0:
                        return True
        """if self._things == []:
            return False

        for c in self._cameras:
            if c.getRemainPeriod() > 0:
                return True
            ts = c.getThings()
            for t in ts:
                if t.getRemainTime()>0 :
                    #print(t.getIndex())
                    for t_c in t.getCameras():
                        #print(t_c.getIndex())
                        if t_c != c and t_c.getRemainPeriod() > 0:
                            #print(t.getIndex())
                            return True"""
        return False

    def cleanNoTimeCamera(self, camera):
        # clean no time camera
        if camera.getRemainPeriod() == 0:
            for t in self._things:
                #print(camera.getIndex())
                if camera in t.getDetectedCameras():
                    #print(camera.getIndex())
                    t.removeDetectedCamera(camera)


    def cuppleThingWithAngle(self, camera):
        pc = PointCalculator()
        degree = []
        mt = camera.getThings()
        # get all angle of thing to camera and X-aix
        for t in mt:
            basePoint = camera.getPosition()
            angel = pc.consineLaw(camera.getPosition(),[basePoint[0]+1,basePoint[1]],t.getPosition())
            if t.getPosition()[1] < basePoint[1]:
                angel = 360 - angel 
            degree.append(angel)
        # sort by angle
        return [x for x in sorted(zip(degree,mt))]

    def findFisrtAnchor(self, sort, cVAngle):
        anchor = []
        anchorIndex = 0
        # find first anchor
        for index , cu in enumerate(sort):
            # if any two near thing angle > camera view angle , the next thing is anchor
            o1 = sort[index]
            if index+1 < len(sort):
                o2 = sort[index+1]
                angle = o2[0] - o1[0]
            else:
                o2 = sort[0]
                angle = o2[0] - o1[0] + 360
            if angle > cVAngle :
                anchor.append(o2)
                anchorIndex = index + 1
                break
        # if no anchor , random select
        if anchor == [] and sort != []:
            anchorIndex = np.random.choice(range(0,len(sort)))
            anchor.append(sort[anchorIndex]) 
        return anchor , anchorIndex

    """
        return (maxthingtime, fov , camera)
    """
    def findFovOfCamera(self,camera,thing):
        maxThingTime = 0
        for fov in camera.getMonitor():
            if thing in fov['side'] or thing in fov['center']:
                for t in fov['side']:
                    if t.getRemainTime() > maxThingTime:
                        maxThingTime = t.getRemainTime()
                    
                for t in fov['center'] :
                    if t.getRemainTime() > maxThingTime:
                        maxThingTime = t.getRemainTime()

                return (maxThingTime,fov,camera)
        return False

    def selfThingRemove(self, targetThing ):
        for t in self._things:
            if t.getIndex() == targetThing.getIndex():
                self._things.remove(t)
                #print("Remove thing %d" % (t.getIndex()))
                break

    def setTime(self, cameraTuple ):
        #print("camera : %d" %(cameraTuple[2].getIndex()) )
        # set time
        time = cameraTuple[0]
        if cameraTuple[2].getRemainPeriod() < cameraTuple[0]:
            time = cameraTuple[2].getRemainPeriod()
                
        for t in cameraTuple[1]['center']:
            t.setRemainTime( t.getRemainTime() - time )
            if t.getRemainTime() <= 0:
                self.selfThingRemove(t)
            
            #if time == 7 and cameraTuple[2].getIndex() == 1:
                #print("===thing %d , remain %d " % (t.getIndex(), t.getRemainTime()))
                
        for t in cameraTuple[1]['side']:
            t.setRemainTime( t.getRemainTime() - time )
            if t.getRemainTime() <= 0:
                self.selfThingRemove(t)

            #if time == 7 and cameraTuple[2].getIndex() == 1:
                #print("===thing %d , remain %d " % (t.getIndex(), t.getRemainTime()))
                
        cameraCurrent = cameraTuple[2].getRemainPeriod()
        #print("camera %d , remain %d , set time %d" % (cameraTuple[2].getIndex(), cameraCurrent, time))
        cameraTuple[2].setRemainPeriod( cameraCurrent - time )
        #print("camera remain %d " %(cameraTuple[2].getRemainPeriod()))
        if "time" in cameraTuple[1]:
            cameraTuple[1]['time'] += time
        else :
            cameraTuple[1]['time'] = time

        self.cleanNoTimeCamera(cameraTuple[2])