import pygame

class ManagerFont:

    fonts: dict    = None

    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized: return None

        self.fonts = dict()
        self._initialized = True
        pass

    def load(self, filename: str, size: int):

        res = self.fonts.get(filename, None)

        try:
            if res is None or not size in res:
                if not res: res = dict()
                res[size] = pygame.font.Font(filename, size)
                self.fonts[filename]=res
        except:
            raise ValueError(f'Font file \'{filename}\' no find:\tCRITICAL ERROR')
        return res[size]
    
    pass