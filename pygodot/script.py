
from .node import Node

class Script:

    owner: Node = None

    
    def __init__(self, *args, **kw):
        if len(args):
            self.owner = args[0]
        pass

    def connect(self, name_signal: str, func, node, *args, **kw):
        pool = self.signal.get(name_signal)
        if pool is None:
            pool = list()
            self.signal[name_signal] = pool
            pass
        pool.append([node, func, args, kw])

    def _call_signal(self, signal_name):
        pool = self.signal.get(signal_name)
        if pool:
            for i in pool:
                if i[0] and not i[0].visible: continue
                i[1](*i[2], **i[3])
        pass

    def ready(self):
        spr = super()
        if hasattr(spr, 'ready'): spr.ready()
        pass

    def process(self, delta_time: int):
        spr = super()
        if hasattr(spr, 'process'): spr.process()
        pass

    def finaly(self):
        spr = super()
        if hasattr(spr, 'finaly'): spr.finaly()
        pass

    def __call__(self, delta_time, *args, **kwds):

        if self.owner is None: return None
        self.process(delta_time)

        pass
    pass
    