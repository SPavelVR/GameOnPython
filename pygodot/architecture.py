
from .timer import PyagemTimer


class Architecture:

    time_update: int
    game_clock       = PyagemTimer()
    uno_update: bool = True

    pause: bool = False

    def __init__(self, *args, **kw):
        self.game_clock = kw.get("game_clock", self.game_clock)
        self.time_update = 0

        self.uno_update = kw.get("uno_update", self.uno_update)
        self.pause = kw.get("pause", self.pause)
        pass


    def process(self, delta_time: int):
        pass

    def ready(self, *args, **kw):
        pass

    def finaly(self):
        pass

    def __call__(self, *args, **kw):
        time = self.game_clock.get_time()
        if self.pause or (self.uno_update and self.time_update == time): return False

        self.time_update = time

        self.update(args[0])

        if self.update_children:
            for c in self.children:
                c(*args, **kw)
            pass

        pass


    pass