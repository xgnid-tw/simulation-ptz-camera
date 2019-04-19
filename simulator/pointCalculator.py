import math


class PointCalculator :
    
    CENTER_POINT = 1
    SIDE_POINT = 0.5

    def __init__(self):
        pass

    def distance2( self, a, b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2

    def consineLaw( self, p, a, b ):
        A = self.distance2(b,p)
        B = self.distance2(a,p)
        C = self.distance2(a,b)
        return math.degrees( math.acos( (C-B-A)/2/math.sqrt(A)/math.sqrt(B)*-1 ) )

    def getPointWeight( self, camera, baseThing, targetThing):
        c_p = camera.getPosition()
        bt_p = baseThing.getPosition()
        tt_p = targetThing.getPosition()
        tAngle = self.consineLaw(c_p, bt_p, tt_p)
        vAgnle = math.degrees(camera.getVAngle())
        #print( vAgnle/6 , vAgnle/2 , tAngle)
        if vAgnle * camera.getRatio()/2  >= tAngle:
            return 1
        elif vAgnle/2 >= tAngle:
            return 0.5
        else:
            return 0

