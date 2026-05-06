import pygame

class ManagerImage:

    images: dict    = None

    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized: return None

        self.images = dict()
        self._initialized = True
        pass

    def load(self, filename: str):

        res = self.images.get(filename, None)

        try:
            if res is None:
                res = pygame.image.load(filename).convert_alpha()
                self.images[filename]=res
        except:
            raise ValueError(f'Image file \'{filename}\' no find:\tCRITICAL ERROR')
        return res
        pass

    def __getitem__(self, key: str):
        image = self.images.get(key, None)
        if image is None:
            image = self.load(key)
        return image
    
    pass