from algorithm.firstFitAlgorithm import FirstFitAlgorithm
from algorithm.simpleSectorFinding import SimpleSectorFinding
from algorithm.simpleCenterSectorFinding import SimpleCenterSectorFinding
import copy

class ScheduleGenerator:

    def __init__(self, grid, point=0.3):
        self.__grid = copy.deepcopy(grid)
        self.point = point

    

    # algorithm interface
    """
    Args:
        type (int): kinds of scheduling
    """
    def scheduling(self, kind):
        cameras = self.__grid.getMapObj('C')
        things =  self.__grid.getMapObj('T')

        algo = [FirstFitAlgorithm,SimpleSectorFinding,SimpleCenterSectorFinding]
        return algo[kind](cameras, things, self.point )

        
    

