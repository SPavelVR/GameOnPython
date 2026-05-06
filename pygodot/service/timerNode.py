

from ..variables import *
from ..timer import *
from ..node import Node
from ..managers import ManagerImage
from ..systems import DrawSystem2D



class TimerNode(Node):

    type_name = 'TimerNode'

    time: int = 0
    delta: int = 0
    duration: int = 0

    count_repeat: int = 0
    counter: int = 0
    running: bool    = True

    def __init__(self, duration: int, count_repeat: int = 0, *args, **kw):        
        self.duration = duration
        self.running = kw.get("running", self.running)

        self.count_repeat = count_repeat
        self.counter = 0

        super().__init__(*args, **kw)
        pass

    def ready(self):
        return super().ready()

    def process(self, delta: int)->bool:
        super().process(delta)
        if not self.running: return False

        self.delta += delta
        self.time += delta
        if self.delta >= self.duration:
            self.delta -= self.duration
            
            if self.count_repeat != 0 and self.counter >= self.count_repeat:
                self.running = False
                self._call_signal("timeout")
            else:
                self._call_signal("repeat")
            self.counter += 1
            return True
        
        return False
    
    def finaly(self):
        return super().finaly()

    def get_time(self):
        return self.time

    def play(self):
        self.delta = 0
        self.running = True
        self.counter = 0

        self._call_signal("to_play")
        pass
    pass


    pass
