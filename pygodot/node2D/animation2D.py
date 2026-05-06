

from .collide2D import *
from .sprite2D import *
from ..variables import *
from ..service.timerNode import *
from ..managers import ManagerImage
from ..systems import DrawSystem2D



class Animation2D(Sprite2D):

    type_name = 'Animation2D'
    timer: TimerNode


    frames: int = 1
    frames_x: int = 1

    frame: int = 0

    beginer_surface: Rect


    def __init__(self, image_name = '', scale=Vector2D(0,0), sub_surface=Rect(0,0,0,0), repeat_mode=SpriteRepeatMode.CLAMP, *args, **kw):
        self.frames = kw.get('frames', 1)
        self.frames_x = kw.get('frames_x', self.frames)

        count_repeat = kw.get('count_repeat', 0) * self.frames

        if count_repeat: count_repeat -= 1

        self.timer = TimerNode(kw.get('duration', 50), count_repeat, running=False)
        
        self.timer.connect('repeat', self.update_animation, self)
        self.timer.connect('timeout', self.time_out_animation, self)

        super().__init__(image_name, scale, sub_surface, repeat_mode, *args, **kw)
        self.append_children(self.timer)
        self.beginer_surface = self.sub_surface.copy()
        pass
    
    def time_out_animation(self):
        self._call_signal('timeout')
        self.sub_surface.x = self.beginer_surface.x
        self.sub_surface.y = self.beginer_surface.y

        self.frame = 0

        self.update_shape()
        pass

    def update_animation(self):
        self.sub_surface.x = self.beginer_surface.x + self.beginer_surface.w * (self.frame % self.frames_x)
        self.sub_surface.y = self.beginer_surface.y + self.beginer_surface.h * (self.frame // self.frames_x)

        self.frame = (self.frame + 1) % self.frames

        self.update_shape()
        pass

    def play(self):
        self.timer.play()
        pass

    def __str__(self):
        return super().__str__() + f'ANM {self.layer} >'
    pass