

from pygodot import *


class ProgressBar(node2D.Node2D):



    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


        self.bg_progress_bar = node2D.Shape2D(parent=self,
                                              collide=kw.get('bg_collide', (0,0,0,0)),
                                              layer=kw.get('layer', 0),
                                              color=kw.get('bg_color', (0,0,0)),
                                              name='bg_prograss_shape'
                                              )
        
        self.bg_progress_bar.to_center()

        lc_pos = self.bg_progress_bar.local_position()
        
        self.fr_progress_bar = node2D.Shape2D(parent=self,
                                              name='fr_prograss_shape',
                                              collide=self.bg_progress_bar.local_collide(),
                                              layer=kw.get('layer', 0) + 1,
                                              color=kw.get('fr_color', (255,255,255)),
                                              position=lc_pos)
        
        self.prograss = 0
        self.MAX_PROGRASS = kw.get('MAX_PROGRESS', 100)

        self.visible_while_full = False

        self.set_progress(self.prograss)
        pass

    def set_progress(self, prograss):

        self.prograss = prograss
        
        kf = self.prograss / self.MAX_PROGRASS
        
        self.fr_progress_bar.collide.w = self.bg_progress_bar.collide.w * kf

        self.fr_progress_bar.update_shape()
        pass

    def process(self, delta_time):

        if not self.visible_while_full and self.prograss == self.MAX_PROGRASS:
            self.fr_progress_bar.hide()
            self.bg_progress_bar.hide()
        else:
            self.fr_progress_bar.show()
            self.bg_progress_bar.show()
        return super().process(delta_time)


    pass