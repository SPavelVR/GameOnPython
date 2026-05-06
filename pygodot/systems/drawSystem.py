
from ..system import *
from ..variables import *
from ..managers.dispay import Display

import pygame

class DrawSystem2D(GameSystem):


    name_system = 'DrawSystem2D'
    camera = None
    layers: list = None

    screen = None

    def __init__(self, *args, **kw):
        if self._initialized: return None
        super().__init__(*args, **kw)

        self.screen: pygame.Surface = kw.get("screen", Display().get_surface())
        self.layers = list()
        for _ in range(33):
            self.layers.append(list())
        pass

    def add_node(self, node):
        if node.type_name == 'Camera2D':
            self.camera = node
            return None
        

        if node is None or not hasattr(node, 'layer'):
            return None
        

        if self in node.systems:
            return None
        

        layer_list = self.layers[node.layer]
        layer_list.append(node)
        
        node.systems[self] = len(layer_list) - 1
        
        return node
        pass

    def remove_node(self, node):
        
        if self.camera and node is self.camera:
            self.camera = None
            return None

        if node is None or not hasattr(node, 'layer') or self not in node.systems:
            return None

        layers = self.layers[node.layer]
        index = node.systems[self]
        
        if index < 0 or index >= len(layers):
            print(f"Ошибка: index {index} вне диапазона [0, {len(layers)-1}]:{node}")
            return None
        
        last_index = len(layers) - 1
        last_node = layers[last_index]
        
        layers[index] = last_node
        
        if last_node is not None and self in last_node.systems:
            last_node.systems[self] = index
        

        layers.pop()
        
        node.systems.pop(self, None)
        
        return node

    def print_array(self):
        print(self.layers)


    def process(self, delta_time):
        surface = self.camera

        if surface is None or not surface.visible: surface = Display()

        rect = surface.get_rect()
        
        for layer in self.layers:
            for elm in layer:
                if elm.visible:
                    
                    pos = elm.global_position()
                    img = elm.get_shape()

                    trct: Rect = pos + Rect(img.get_rect())

                    if img and rect.colliderect(trct):
                        surface.blit(img, pos.getByTuple())
        pass



class DrawSystemUI(DrawSystem2D):
    name_system = 'DrawSystemUI'

    def __init__(self, *args, **kw):
        if self._initialized: return 
        super().__init__(*args, **kw)

    def process(self, delta_time):
        if self.camera:
            self.camera = None
        return super().process(delta_time)
    pass
