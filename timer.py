import pygame as pg
from imagerect import ImageRect


class Timer:
    def __init__(self, game, images, wait=100, frameindex=0, step=1, looponce=False, sizex=25, sizey=0):
        self.game = game
        self.screen = self.game.screen
        self.images = images
        self.frames = []
        self.wait = wait
        self.frameindex = frameindex
        self.step = step
        self.looponce = looponce
        self.loadimages(sizex=sizex, sizey=sizey)
        self.finished = False
        self.lastframe = len(self.frames) - 1 if step == 1 else 0
        self.last = None

    def loadimages(self, sizex=25, sizey=0):
        if sizey == 0:
            sizey = sizex
        for im in self.images:
            self.frames.append(ImageRect(self.screen, im, height=sizex, width=sizey))

    def frame_index(self):
        now = pg.time.get_ticks()
        if self.last is None:
            self.last = now
            self.frameindex = 0 if self.step == 1 else len(self.frames) - 1
            return 0
        elif not self.finished and now - self.last > self.wait:
            self.frameindex += self.step
            if self.looponce and self.frameindex == self.lastframe:
                self.finished = True
            else:
                self.frameindex %= len(self.frames)
            self.last = now
        return self.frameindex

    def reset(self):
        self.last = None
        self.finished = False

    def __repr__(self):
        return 'Timer(frames={}, wait={}, index={})'.format(self.frames,
                                                            str(self.wait),
                                                            str(self.frameindex))

    def imagerect(self):
        return self.frames[self.frame_index()]


class TimerDual:
    def __init__(self, game,  images1, images2, wait1=100, wait2=100, wait_switch_timers=1000,
                 frameindex1=0, frameindex2=0, step1=1, step2=1, looponce=False):

        self.game = game
        self.wait_switch_timers = wait_switch_timers
        self.timer1 = Timer(game, images1, wait1, frameindex1, step1, looponce)
        self.timer2 = Timer(game, images2, wait2, frameindex2, step2, looponce)
        self.timer = self.timer1   # start with timer1
        self.counter = 0

        self.now = pg.time.get_ticks()
        self.lastswitch = self.now

    def frame_index(self):
        now = pg.time.get_ticks()
        if now - self.lastswitch > self.wait_switch_timers:
            self.timer = self.timer2 if self.timer == self.timer1 else self.timer1
            self.lastswitch = now
            self.counter += 1
        return self.timer.frame_index()

    def reset(self):
        self.timer1.reset()
        self.timer2.reset()
        self.timer = self.timer1
        self.counter = 0

    def __str__(self): return 'TimerDual(' + str(self.timer1) + ',' + str(self.timer2) + ')'

    def imagerect(self):
        idx = self.frame_index()
#        print('idx: ' + str(idx))
        return self.timer.frames[idx]
