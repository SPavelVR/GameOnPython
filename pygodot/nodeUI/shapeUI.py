
from .nodeUI import *
from ..node2D.shape2D import Shape2D
from ..systems import *



class ShapeUI(Shape2D, NodeUI):

    type_name = 'ShapeUI'
    
    include_systems = [DrawSystemUI, EventSystem]
    pass


