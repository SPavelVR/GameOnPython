


from .collide2D import *
from ..variables import *
from ..systems import DrawSystem2D

import pygame

class Shape2D(Collide2D):

    type_name: str = "Shape2D"

    include_systems = [DrawSystem2D]

    shape: pygame.Surface
    color: Vector3D
    type_shape: str

    layer: int = 0

    def __init__(self, *args, **kw):
        self.layer = clamp(kw.get("layer", 0), 0, 32)
        
        self.color = Vector3D(kw.get('color', Vector3D(0,0,0)))
        self.type_shape = kw.get('type_shape', 'square')


        super().__init__(*args, **kw)
        self.update_shape()
        pass

    def update_shape(self):

        if self.collide == Rect(0,0,0,0):
            self.shape = None
        else:
            self.shape = pygame.Surface(self.collide.getSizeByTuple(), pygame.SRCALPHA).convert_alpha()
            self.shape.fill((0,0,0,0))

            if self.type_shape == 'square':
                pygame.draw.rect(self.shape, self.color.getByTuple(), self.shape.get_rect())
            elif self.type_shape == 'circle':
                rct = self.shape.get_rect()
                center = rct.center

                pygame.draw.circle(self.shape, self.color.getByTuple(), center, min(rct.h // 2, rct.w // 2))
            pass
        pass

    def get_shape(self):
        return self.shape

    pass