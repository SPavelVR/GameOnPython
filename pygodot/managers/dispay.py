import pygame

from ..variables import *


class Display:

    display: pygame.Surface = None
    display_rect            = None

    pygame_display          = None

    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kw):
        if self._initialized: return None
        self._initialized = True

        self.pygame_display = pygame.display.set_mode(*args)
        self.display_rect   = self.pygame_display.get_rect()
        self.display        = pygame.Surface((self.display_rect.w, self.display_rect.h))
        pass

    def set_mode(self, *args):
        self.pygame_display = pygame.display.set_mode(*args)
        pass

    def get_surface(self):
        return self.display
    
    def get_rect(self):
        return self.display.get_rect()
    
    def get_scale(self)->Vector2D:
        pygame_display_size = Vector2D(Rect(self.pygame_display.get_rect()).getSizeByTuple())
        display_size = Vector2D(Rect(self.display_rect).getSizeByTuple())
        return Vector2D(pygame_display_size.x / display_size.x, pygame_display_size.y / display_size.y)
        pass
    
    def blit(self, *args):
        self.display.blit(*args)
        pass

    def fill(self, color):
        self.display.fill(color)

    def flip(self):

        surface = self.display
        pygame_display_rect = self.pygame_display.get_rect()
        if pygame_display_rect.w != self.display_rect.w or pygame_display_rect.h != self.display_rect.h:
            surface = pygame.transform.scale(surface, (pygame_display_rect.w, pygame_display_rect.h))
            pass

        self.pygame_display.blit(surface, (0,0))
        pygame.display.flip()
        pass

    pass