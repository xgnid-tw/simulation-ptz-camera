
class MapObject:

    def __init__(self, mark):
        self.__x = 0
        self.__y = 0
        self.__mark = mark

    def setPosition(self,x,y):
        self.__x = x
        self.__y = y
    
    def getPosition(self):
        return [self.__x,self.__y]

    def showPosition(self):
        print("x : %f, y: %f" % (self.__x, self.__y) )

    def getMark(self):
        return self.__mark
