
from .collide2D import *
from ..variables import *
from ..managers import ManagerImage, Display
from ..systems import DrawSystem2D

class Camera2D(Collide2D):

    type_name: str = "Camera2D"

    include_systems = [DrawSystem2D]

    scale_w = 1
    scale_h = 1

    def __init__(self, *args, **kw):
        if self.collide.w == 0 or self.collide.h == 0: self.collide = Rect(Display().get_rect())

        super().__init__(*args, **kw)
        
        self._set_scale_camera()
        pass

    def blit(self, surface, cord: tuple):
        display = Display()
        pos = self.global_position()

        sfr = surface.get_rect()

        pos = Vector2D(cord[0] - pos.x, cord[1] - pos.y)

        pos.x = pos.x * self.scale_w
        pos.y = pos.y * self.scale_h


        surface = pygame.transform.scale(surface, (sfr.w * self.scale_w, sfr.h * self.scale_h))

        display.blit(surface, pos.getByTuple())
        pass

    def get_rect(self):
        return self.global_collide()
    
    def _set_scale_camera(self):
        rect_dispay = Display().get_rect()
        self.scale_w = rect_dispay.w / self.collide.w
        self.scale_h = rect_dispay.h / self.collide.h
    pass
