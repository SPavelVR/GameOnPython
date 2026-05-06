
from .nodeUI import *
from ..node2D.text2D import Text2D
from ..systems import *

class TextUI(Text2D, NodeUI):

    type_name = 'TextUI'
    include_systems = [DrawSystemUI, EventSystem]
    pass
