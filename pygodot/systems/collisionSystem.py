
from ..system import *
from ..variables import *

import pygame

class CollisionSystem(GameSystem):

    name_system = 'CollisionSystem'

    

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.spatial_grid = SpatialGrid(cell_size=100)
        pass
    
    def process(self, delta_time):
        self.spatial_grid.clear()
        for node in self.node_array:
            if node.visible:
                self.spatial_grid.insert(node)
                pass
        
        size = len(self.node_array)

        i = 0
        while i < len(self.node_array):
            node1 = self.node_array[i]
            i += 1
            if not node1.visible: continue

            rect1: Rect = node1.global_collide()
            nearby = self.spatial_grid.get_potential_collisions(rect1)

            for node2 in nearby:
                if node2 is node1: continue

                rect2: Rect = node2.global_collide()

                if not rect1.colliderect(rect2): continue

                collide_flag = False

                if node1.layer in node2.mask:
                    node2.on_collision(node1)
                    collide_flag = True
                    pass

                if node2.layer in node1.collide:
                    node1.on_collision(node2)
                    collide_flag = True
                    pass
                
                if node1.collidable == False or node2.collidable == False or collide_flag == False: continue

                vector = [1,0,rect1.x + rect1.w - rect2.x]

                if abs(rect1.y + rect1.h - rect2.y) < abs(vector[2]):
                    vector = [0,1,rect1.y + rect1.h - rect2.y]
                
                if abs(rect1.x - rect2.x - rect2.w) < abs(vector[2]):
                    vector = [-1, 0, -rect1.x + rect2.x + rect2.w]

                if abs(rect1.y - rect2.y - rect2.h) < abs(vector[2]):
                    vector = [0, -1, -rect1.y + rect2.y + rect2.h]

                vector[0] *= vector[2]
                vector[1] *= vector[2]

                vector = Vector2D(vector[0], vector[1])

                chrBD1 = node1.find_character_body()
                chrBD2 = node2.find_character_body()

                if not (chrBD1 and chrBD2): return None

                if node1.heavy == node2.heavy:
                    vector = vector // 2
                    chrBD1.set_local_position(chrBD1.local_position() - vector)
                    chrBD2.set_local_position(chrBD2.local_position() + vector)
                elif node1.heavy > node2.heavy:
                    chrBD2.set_local_position(chrBD2.local_position() + vector)
                else:
                    chrBD1.set_local_position(chrBD1.local_position() - vector)
                pass
            pass
        pass
        

        return super().process(delta_time)
    
    def process__V1(self, delta_time: int):

        size = len(self.node_array)
        
        for i in range(size):
            node1 = self.node_array[i]
            if not node1.visible: continue
            for j in range(i + 1, size):
                node2 = self.node_array[j]
                if not node2.visible: continue


                rect1: Rect = node1.global_collide()
                rect2: Rect = node2.global_collide()

                if not rect1.colliderect(rect2): continue

                collide_falg = False

                if node1.layer in node2.mask:
                    node2.on_collision(node1)
                    collide_falg = True
                    pass

                if node2.layer in node1.collide:
                    node1.on_collision(node2)
                    collide_falg = True
                    pass
                
                if node1.collidable == False or node2.collidable == False or collide_falg == False: continue

                vector = [1,0,rect1.x + rect1.w - rect2.x]

                if abs(rect1.y + rect1.h - rect2.y) < abs(vector[2]):
                    vector = [0,1,rect1.y + rect1.h - rect2.y]
                
                if abs(rect1.x - rect2.x - rect2.w) < abs(vector[2]):
                    vector = [-1, 0, -rect1.x + rect2.x + rect2.w]

                if abs(rect1.y - rect2.y - rect2.h) < abs(vector[2]):
                    vector = [0, -1, -rect1.y + rect2.y + rect2.h]

                vector[0] *= vector[2]
                vector[1] *= vector[2]

                vector = Vector2D(vector[0], vector[1])

                chrBD1 = node1.find_character_body()
                chrBD2 = node2.find_character_body()

                if not (chrBD1 and chrBD2): return None

                if node1.heavy == node2.heavy:
                    vector = vector // 2
                    chrBD1.set_local_position(chrBD1.local_position() - vector)
                    chrBD2.set_local_position(chrBD2.local_position() + vector)
                elif node1.heavy > node2.heavy:
                    chrBD2.set_local_position(chrBD2.local_position() + vector)
                else:
                    chrBD1.set_local_position(chrBD1.local_position() - vector)
                pass
            pass
        pass
    pass



class SpatialGrid:
    def __init__(self, cell_size=100):
        self.cell_size = cell_size
        self.grid = {}
    
    def clear(self):
        self.grid.clear()
    
    def get_cell_key(self, rect):
        cx = int(rect.centerx // self.cell_size)
        cy = int(rect.centery // self.cell_size)
        return (cx, cy)
    
    def insert(self, node):
        key = self.get_cell_key(node.global_collide())
        if key not in self.grid:
            self.grid[key] = []
        self.grid[key].append(node)
    
    def get_potential_collisions(self, rect):
        cells = [
            self.get_cell_key(Rect(rect.x + dx, rect.y + dy, rect.w, rect.h))
            for dx in [-self.cell_size, 0, self.cell_size]
            for dy in [-self.cell_size, 0, self.cell_size]
        ]
        
        nearby = []
        for cell in set(cells):
            if cell in self.grid:
                nearby.extend(self.grid[cell])
        return nearby