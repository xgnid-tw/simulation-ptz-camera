from grid import Grid
from sampleGenerator import SampleGenerator
from scheduleGenerator import ScheduleGenerator
from camera import Camera
from mapSeeder import MapSeeder
import numpy as np
import copy
import math
import csv

def debug(cameras, things):
    for c in cameras:
        print("camera %d : time %d , position(%.2f,%.2f) , remain : %d " % (c.getIndex() , c.getPeriod(), c.getPosition()[0], c.getPosition()[1], c.getRemainPeriod() ) )
        
        for t in c.getThings():
            print( "\tThing %d : time %d , remain %d , position (%.2f,%.2f)" % (t.getIndex(), t.getMinTime(), t.getRemainTime(), t.getPosition()[0] , t.getPosition()[1] ) )
            
        for fov in c.getMonitor() :
            print("--")
            print("side   :" , end="")
            print([t.getIndex() for t in fov['side']])
            print('center :' , end='')         
            print([t.getIndex() for t in fov['center']])
            if "time" in fov:       
                print('**time   : %d' % (fov['time']))
    


def main(height, width, cameraAmount, thingAmount, vangel= np.pi/3 , ratio = 1/3, point=0.3):
    seed = MapSeeder()
    c,t = seed.mapObject()
    g =  Grid(height,width)
    #g.setSeed(c,t)
    sg = SampleGenerator(g,vangel=vangel,ratio=ratio)
    sg.cameraSampling(cameraAmount)
    sg.thingSampling(thingAmount)
    c,t = g.getMapObject()
    # before scheduling
#    debug(c,t)
    g1 = copy.deepcopy(g)
    g2 = copy.deepcopy(g)
    r1 = 0
    r1s = 0
    r2 = 0
    r2s = 0
    r3 = 0
    r3s = 0
    
    schgF = ScheduleGenerator(g,point)
    method = schgF.scheduling(0)
    c, t = method.run()
    r1,r1s = method.result()
    #debug(c,t)

    schgS = ScheduleGenerator(g1,point)
    method = schgS.scheduling(1)
    c, t = method.run()
    r2,r2s = method.result()
    #debug(c,t)

    schgC = ScheduleGenerator(g2,point)
    method = schgC.scheduling(2)
    c, t = method.run()
    r3,r3s = method.result()
    #debug(c,t)
    # after scheduling
    
    #g.draw()

    return [(r1,r1s),(r2,r2s),(r3,r3s)]
    
        
times = 100
loop = 30
vangel = np.pi / 3
ratio = 0.3
cameraAmount = 20
thingAmount = 120
point = 0.1

with open('output_p.csv', 'w', newline='') as csvfile:
    
    writer = csv.writer(csvfile)
    writer.writerow( np.linspace(0.1,0.9,9) )
    csvForm = [[],[],[],[],[],[]]
        
    print("物數量　： %d" %(thingAmount))
    print("相機數量： %d" %(cameraAmount))
    print("視角　　： %d" %( math.degrees(vangel) ))
    print("比率　　： %.2f" %(ratio) )
        
    while point < 1   :
        cbm = 0
        cbmE = 0
        ssf = 0
        ssfE = 0
        scsf = 0
        scsfE = 0
        for i in range(0,times):
            r1,r2,r3 = main(30, 30, cameraAmount, thingAmount, vangel, ratio,point)

            cbm += r1[0]
            cbmE += r1[1]
            ssf += r2[0]
            ssfE += r2[1]
            scsf += r3[0]
            scsfE += r3[1]
        print("=== 側邊分數 = %.2f ===" %(point) )
        print("cbm              : %.2f" % (cbm/times))
        print("cbm error ratio  : %.2f " % (cbmE/times*100))
        print("ssf              : %.2f" % (ssf/times))
        print("ssf error ratio  : %.2f " % (ssfE/times*100))
        print("scsf             : %.2f" % (scsf/times))
        print("scsf error ratio : %.2f " % (scsfE/times*100))

        print("%.2f" % (cbm/times))
        print("%.2f" % (ssf/times))
        print("%.2f" % (scsf/times))

        point += 0.1

        csvForm[0].append(cbm/times)
        csvForm[1].append(ssf/times)
        csvForm[2].append(scsf/times)

    for c in csvForm:
        writer.writerow(c)
    writer.writerow([])
