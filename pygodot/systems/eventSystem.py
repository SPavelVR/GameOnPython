

from ..system import *
from ..variables import *
from ..managers import Display

import pygame


class EventSystem(GameSystem):


    name_system = 'EventSystem'

    last_mouse_position: Vector2D = None
    mouse_position: Vector2D
    mouse_motion: Vector2D

    _running = True

    mouse_down: set     = set()
    mouse_pressed: set  = set()
    mouse_up: set       = set()

    def process(self, delta_time):

        self.mouse_position = Vector2D(pygame.mouse.get_pos())

        scale = Display().get_scale()

        self.mouse_position.y //= scale.y
        self.mouse_position.x //= scale.x

        if self.last_mouse_position is None:
            self.last_mouse_position = self.mouse_position

        self.mouse_motion = self.mouse_position - self.last_mouse_position


        events = pygame.event.get()

        self.mouse_down.clear()
        self.mouse_up.clear()

        for event in events:
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down.add(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up.add(event.button)
            pass

        for nodeui in self.node_array:
            if not nodeui.visible or nodeui._pause: continue

            

            rect: Rect = nodeui.global_collide()

            if not rect.collidepoint(*self.mouse_position.getByTuple()): continue
            
            nodeui._on_hover()

            active_mouse = False

            if self.mouse_motion.x != 0 or self.mouse_motion.y != 0:
                nodeui._on_mousemotion(self.mouse_motion)
            if len(self.mouse_down):
                active_mouse = True
                nodeui._on_mouse_down(self.mouse_down)
            if len(self.mouse_up):
                active_mouse = True
                nodeui._on_mouse_up(self.mouse_up)
            if len(self.mouse_pressed):
                active_mouse = True
                nodeui._on_mouse_pressed(self.mouse_pressed)

            if active_mouse:
                nodeui._on_mouse_active(self.mouse_pressed | self.mouse_down | self.mouse_up)
            pass
        
        self.last_mouse_position = self.mouse_position
        self.mouse_pressed.update(self.mouse_down)
        self.mouse_pressed.difference_update(self.mouse_up)
        return True