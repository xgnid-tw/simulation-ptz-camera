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
    

def rat(cameras):
    center = 0
    side = 0
    for c in cameras:
        for fov in c.getMonitor():
            if "time" in fov:
                center += len(fov['center'])
                side += len(fov['side'])

    total = center+side
    return (center/total,side/total)

def main(height, width, cameraAmount, thingAmount, vangel= np.pi/3 , ratio = 1/3):
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
    
    schgF = ScheduleGenerator(g)
    method = schgF.scheduling(0)
    c, t = method.run()
    r1,r1s = method.result()
    r1c , r1si = rat(c)
    #debug(c,t)

    schgS = ScheduleGenerator(g1)
    method = schgS.scheduling(1)
    c, t = method.run()
    r2,r2s = method.result()
    r2c , r2si = rat(c)
    #debug(c,t)

    schgC = ScheduleGenerator(g2)
    method = schgC.scheduling(2)
    c, t = method.run()
    r3,r3s = method.result()
    r3c , r3si = rat(c)
    #debug(c,t)
    # after scheduling
    
    #g.draw()

    return [(r1,r1s,r1c,r1si),(r2,r2s,r2c,r2si),(r3,r3s,r3c,r3si)]
    
        
times = 100
loop = 30
vangels = [np.pi / 3 *2 , np.pi / 2 , np.pi / 3 , np.pi / 6]

cameraAmount = 20
thingAmount = 120


with open('output_r.csv', 'w', newline='') as csvfile:
    
    writer = csv.writer(csvfile)
    writer.writerow( np.linspace(0.1,0.9,9) )

    for vangel in vangels:
        csvForm = [[],[],[],[],[],[]]
            
        print("物數量　： %d" %(thingAmount))
        print("相機數量： %d" %(cameraAmount))
        print("視角　　： %d" %( math.degrees(vangel) ))
        ratio = 0.1
        while ratio <= 1   :
            cbm = 0
            cbmE = 0
            cbmcc = 0
            cbmsi = 0
            ssf = 0
            ssfE = 0
            ssfcc = 0
            ssfsi = 0
            scsf = 0
            scsfE = 0
            scsfcc = 0
            scsfsi = 0

            for i in range(0,times):
                r1,r2,r3 = main(30, 30, cameraAmount, thingAmount, vangel, ratio)

                cbm += r1[0]
                cbmE += r1[1]
                cbmcc += r1[2]
                cbmsi += r1[3]

                ssf += r2[0]
                ssfE += r2[1]
                ssfcc += r2[2]
                ssfsi += r2[3]

                scsf += r3[0]
                scsfE += r3[1]
                scsfcc += r3[2]
                scsfsi += r3[3]

            print("=== 比率 = %.2f ===" %(ratio) )
            """print("cbm              : %.2f" % (cbm/times))
            print("cbm error ratio  : %.2f " % (cbmE/times*100))
            print("ssf              : %.2f" % (ssf/times))
            print("ssf error ratio  : %.2f " % (ssfE/times*100))
            print("scsf             : %.2f" % (scsf/times))
            print("scsf error ratio : %.2f " % (scsfE/times*100))"""

            print("%.2f" % (cbm/times))
            print("%.2f" % (cbmcc/times))
            print("%.2f" % (ssf/times))
            print("%.2f" % (ssfcc/times))
            print("%.2f" % (scsf/times))
            print("%.2f" % (scsfcc/times))

            ratio += 0.1


            csvForm[0].append(cbm/times)
            csvForm[1].append(cbmcc/times)
            csvForm[2].append(ssf/times)
            csvForm[3].append(ssfcc/times)
            csvForm[4].append(scsf/times)
            csvForm[5].append(scsfcc/times)


        for c in csvForm:
            writer.writerow(c)
        writer.writerow([])
    


