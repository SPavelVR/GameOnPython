

from .collide2D import *
from ..variables import *
from ..managers import ManagerImage
from ..systems import DrawSystem2D

import pygame

class SpriteRepeatMode:
    STRETCH = "stretch"      # Растянуть до размера области
    REPEAT = "repeat"        # Повторить (замостить)
    CLAMP = "clamp"          # Обрезать по краям (не повторять)

class Sprite2D(Collide2D):

    type_name: str = "Sprite2D"

    include_systems = [DrawSystem2D]

    repeat_mode = SpriteRepeatMode.STRETCH
    shift_sprit: Vector2D = Vector2D(0,0)

    sub_surface: Rect               = Rect(0,0,0,0)
    scale: Vector2D                 = Vector2D(0,0)

    image: pygame.Surface           = None
    result_image: pygame.Surface    = None

    layer: int = 0

    flip_x: bool = False
    flip_y: bool = False

    angel: float = 0.0

    def __init__(self, image_name: str = '', scale=Vector2D(0,0), sub_surface=Rect(0,0,0,0), repeat_mode=SpriteRepeatMode.CLAMP, *args, **kw):
        self.repeat_mode = repeat_mode
        self.layer = clamp(kw.get("layer", 0), 0, 32)

        self.scale = Vector2D(kw.get('scale', (0,0)))
        self.sub_surface = Rect(kw.get('sub_surface', (0,0,0,0)))

        self.angel = kw.get('angel', self.angel)

        super().__init__(*args, **kw)
        self.set_image(image_name, scale, sub_surface)
        pass

    def set_image(self, image_name: str, scale=Vector2D(0,0), sub_surface=Rect(0,0,0,0)):
        if not image_name: return False

        self.image = ManagerImage().load(image_name)

        self.sub_surface = sub_surface
        self.scale = scale
        
        if self.sub_surface == Rect(0,0,0,0):
            self.sub_surface = Rect(self.image.get_rect())
        if self.scale == Vector2D(0,0):
            self.scale = Vector2D(self.sub_surface.w, self.sub_surface.h)
        
        self.update_shape()
        pass

    def place_image(self):

        if self.sub_surface == Rect(0,0,0,0):
            self.sub_surface = Rect(self.image.get_rect())
        if self.scale == Vector2D(0,0):
            self.scale = Vector2D(self.sub_surface.w, self.sub_surface.h)
        
        self.update_shape()

        pass

    def update_shape(self):
        if self.image is None: return None

        image = self.image.subsurface(self.sub_surface)
        image = pygame.transform.scale(image, self.scale.getByTuple())

        if self.collide == Rect(0,0,0,0):
            self.collide = Rect(image.get_rect())

        if self.repeat_mode is SpriteRepeatMode.CLAMP:
            self.collide = Rect(0,0,self.scale.x, self.scale.y)
        elif self.repeat_mode is SpriteRepeatMode.STRETCH and (self.collide.w != self.scale.x or self.collide.h != self.scale.y):
            image = pygame.transform.scale(image, (self.collide.w, self.collide.h))
        elif self.repeat_mode is SpriteRepeatMode.REPEAT:
            if self.collide.w <= self.scale.x:
                image = pygame.transform.scale(image, (self.collide.w, image.get_rect().h))
            if self.collide.h <= self.scale.y:
                image = pygame.transform.scale(image, (image.get_rect().w, self.collide.h))

            tempRect = image.get_rect()
            resSurface = pygame.Surface((self.collide.w, self.collide.h))
            
            for x in range(0, resSurface.get_rect().w // tempRect.w + ((resSurface.get_rect().w % tempRect.w) != 0)):
                for y in range(0, resSurface.get_rect().h // tempRect.h + ((resSurface.get_rect().h % tempRect.h) != 0)):
                    resSurface.blit(image, (tempRect.w * x, tempRect.h * y))
            image = resSurface

        if self.flip_x or self.flip_y:
            image = pygame.transform.flip(image, self.flip_x, self.flip_y)

        if self.angel:
            image = pygame.transform.rotate(image, self.angel)

        self.result_image = image
        pass

    def get_shape(self)->pygame.Surface:
        return self.result_image


    pass