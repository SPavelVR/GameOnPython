import pygame

class Timer:

    time: int = 0
    delta: int = 0
    duration: int = 0

    auto_reset: bool = True
    running: bool    = True

    signal: dict = None
    ignor: bool  = False

    def __init__(self, duration: int, **kw):
        self.duration = duration
        self.auto_reset = kw.get("auto_reset", self.auto_reset)
        self.running = kw.get("running", self.running)

        self.signal = dict()
        pass
    
    def connect(self, name_signal: str, func, node, *args, **kw):
        pool = self.signal.get(name_signal)
        if pool is None:
            pool = list()
            self.signal[name_signal] = pool
            pass

        pool.append([node, func, args, kw])
        pass

    def _call_signal(self, signal_name):
        if self.ignor: return
        pool = self.signal.get(signal_name)  
        if pool:
            for i in pool:
                if i[0] and i[0].pause: continue
                i[1](*i[2], **i[3])
        pass

    def ready(self, delta: int)->bool:
        if not self.running: return False

        self.delta += delta
        self.time += delta

        if self.delta >= self.duration:
            if self.auto_reset:
                self.delta -= self.duration

                self._call_signal("reset_time")
            else:
                self.running = False
                self._call_signal("timeout")
            return True
        
        return False
    
    def pause(self):
        if not self.running: return
        self.running = False
        self._call_signal("to_pause")
        pass
    
    def start(self):
        if self.running: return
        self.running = True
        self._call_signal("to_start")
        pass

    def get_time(self):
        return self.time

    def play(self):
        self.delta = 0
        self.running = True

        self._call_signal("to_play")
        pass
    pass


class PyagemTimer:

    time: int = 0
    delta: int = 0

    delta_pause: int = 0

    running = True

    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __int__(self):
        if self._initialized: return None
        self._initialized = True

        self.time = pygame.time.get_ticks()
        self.delta = 0
        pass

    def update(self):
        time = pygame.time.get_ticks()
        self.delta = time - self.time
        self.time = time
        pass

    def get_delta(self):
        return self.delta
    
    def get_time(self):
        return self.time

    def pause(self):
        if not self.running: return None

        self.running = False
        self.delta_pause = pygame.time.get_ticks() - self.time
        pass

    def start(self):
        if self.running: return None

        self.running = True
        self.time = pygame.time.get_ticks() - self.delta_pause
        self.delta_pause = 0
        pass
    pass