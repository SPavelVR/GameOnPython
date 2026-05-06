

from .collide2D import *
from ..variables import *
from ..managers import ManagerFont
from ..systems import DrawSystem2D

import pygame


class Text2D(Collide2D):

    type_name = 'Text2D'
    
    include_systems = [DrawSystem2D]

    antialias: bool = True
    color: Vector3D = Vector3D(0,0,0)

    font: pygame.font.Font = None
    size: int = 16

    text: str = ''

    layer: int = 0

    font_obj = None
    stretch_on: bool = False

    def __init__(self, *args, **kw):

        self.antialias  = kw.get('antialias', self.antialias)
        self.layer      = clamp(kw.get("layer", self.layer), 0, 32)
        self.color      = Vector3D(kw.get('color', self.color))
        self.stretch_on = kw.get('stretch', self.stretch_on)
        self.size       = kw.get('size',self.size)

        self.set_font(kw.get('font'), kw.get('filefont'), kw.get('sysfont'))

        self.text = kw.get('text', self.text)

        super().__init__(*args, **kw)
        self.update_shape()
        pass

    def set_font(self, font=None, filefont=None, sysfont=None):
        if font:
            self.font = font
        elif filefont:
            self.font = ManagerFont().load(filefont, self.size)
        elif sysfont:
            self.font = pygame.font.SysFont(sysfont, self.size)
        else:
            self.font = pygame.font.SysFont('arial', self.size)
        pass

    def update_shape(self):
        self.font_obj = self.font.render(self.text, self.antialias, self.color.getByTuple())
        font_onj_rect = self.font_obj.get_rect()

        self.collide = Rect(self.font_obj.get_rect())
            

        if self.stretch_on and (font_onj_rect.w != self.collide.w or font_onj_rect.h != self.collide.h):
            self.font_obj = pygame.transform.scale(self.font_obj, (self.collide.w, self.collide.h))
        pass


    def get_shape(self):
        return self.font_obj



    pass