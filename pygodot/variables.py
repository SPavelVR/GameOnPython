import pygame
import math

class Rect(pygame.Rect):

    def __add__(self, other):

        if type(other) is Rect:
            return Rect(self.x + other.x,
                    self.y + other.y,
                    self.w + other.w,
                    self.h + other.h)
        elif type(other) is Vector2D:
            return Rect(self.x + other.x,
                        self.y + other.y,
                        self.w,
                        self.h)
        return NotImplemented
    
    def touching(self, other):
        if self.y > (other.y + other.h) or (self.y + self.h) < other.y or self.x > (other.x + other.w) or (self.x + self.w) < other.w: return False

        if self.y == (other.y + other.h) or self.x == (other.x + other.w) or (self.y + self.h) == other.y or (self.x + self.w) == other.x: return True

        return False
    
    def getSizeByTuple(self):
        return (self.w, self.h)
    pass


class Vector2D:

    x: int = 0
    y: int = 0

    def __init__(self, *args, **kw):

        larg = len(args)
        lkw  = len(kw)

        if larg > 0 and lkw == 0:
            tp = type(args[0])
            if hasattr(args[0], 'x'):
                self.x = args[0].x
                if hasattr(args[0], 'y'):
                    self.y = args[0].y
            elif tp is int or tp is float:
                self.x = args[0]
                if larg > 1 and (type(args[1]) is int or type(args[1]) is float):
                    self.y = args[1]
            elif tp is tuple or tp is list:
                self.x = args[0][0]
                if len(args[0]) > 1:
                    self.y = args[0][1]
        elif lkw > 0 and larg == 0:
            self.x = kw.get('x', 0)
            self.y = kw.get('y', 0)
        pass

    def __add__(self, other):
        tp = type(other)

        res = None

        if tp is Rect:
            res = Rect(other.x + self.x, other.y + self.y, other.w, other.h)
        elif tp is Vector2D:
            res = Vector2D(self.x + other.x, self.y + other.y)
        return res
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        tp = type(other)

        res = None

        if tp is Rect:
            res = Rect(self.x - other.x, self.y - other.y, other.w, other.h)
        elif tp is Vector2D:
            res = Vector2D(self.x - other.x, self.y - other.y)
        return res

    def __rsub__(self, other):
        return Vector2D.__sub__(other, self)
    
    def __mul__(self, other):
        tp = type(other)

        if not (tp is int or tp is float or tp is Vector2D or tp is Rect): return None


        if tp is Vector2D or tp is Rect:
            return self.x * other.x + self.y * other.y
        return Vector2D(self.x * other, self.y * other)
    
    def __rmul__(self, other):
        tp = type(other)

        if not (tp is int or tp is float): return None

        return Vector2D(self.x * other, self.y * other)
    

    def __truediv__(self, other):
        tp = type(other)

        if not (tp is int or tp is float): return None

        return Vector2D(self.x / other, self.y / other)

    def __floordiv__(self, other):
        tp = type(other)

        if not (tp is int or tp is float): return None

        return Vector2D(self.x // other, self.y // other)
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f'<Vector2D ({self.x}, {self.y})>'
    
    def __eq__(self, value):

        tp = type(value)
        if tp is Vector2D or tp is Rect:
            return value.x == self.x and value.y == self.y
        return False
    
    def getByTuple(self):
        return (self.x, self.y)
    
    def size(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normilized(self):
        size = self.size()
        if size == 0: return Vector2D(0,0)
        return Vector2D(self.x / size, self.y / size)
    
    def getAngel(self):

        vec = self.normilized()

        angel = -sing(vec.y) * math.acos(vec.x)

        return angel
        pass
    pass


class Vector3D:

    x: int | float = 0
    y: int | float = 0
    z: int | float = 0

    def __init__(self, *args, **kw):

        larg = len(args)
        lkw  = len(kw)
        
        if larg > 0 and lkw == 0:
            tp = type(args[0])
            if tp is int or tp is float:
                self.x = args[0]
                if larg > 1 and (type(args[1]) is int or type(args[1]) is float):
                    self.y = args[1]
            elif hasattr(args[0], 'x'):
                self.x = args[0].x
                if hasattr(args[0], 'y'):
                    self.y = args[0].y
                if hasattr(args[0], 'z'):
                    self.z = args[0].z
            elif tp is tuple or tp is list:
                self.x = args[0][0]
                if len(args[0]) > 1:
                    self.y = args[0][1]
                if len(args[0]) > 2:
                    self.z = args[0][2]
        elif lkw > 0 and larg == 0:
            self.x = kw.get('x', 0)
            self.y = kw.get('y', 0)
            self.z = kw.get('z', 0)
        pass

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f'<Vector3D ({self.x}, {self.y}, {self.z})>'

    def getByTuple(self):
        return (self.x, self.y, self.z)
    pass




def sing(number):
    if number == 0: return 0
    if number > 0: return 1
    return -1

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def fraction(value):
    return float(value - int(value))