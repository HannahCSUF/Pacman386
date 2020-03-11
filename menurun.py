import pygame as pg
from timer import Timer


class Display:
    def __init__(self, game):
        self.game = game
        self.viewMenu = True
        self.yellow = (225, 225, 0)
        self.white = (225, 225, 225)
        self.font = pg.font.SysFont("comicsansms", 40)
        self.font1 = pg.font.SysFont("comicsansms", 40)
        self.font2 = pg.font.SysFont("comicsansms", 40)

        self.ply = self.font.render("PLAY", True, self.yellow)
        self.ply_button = self.ply.get_rect()
        self.ply_button.centerx = game.screen.get_rect().centerx + 50
        self.ply_button.centery = game.screen.get_rect().centery + 300

        self.intro = pg.image.load('images/1.png')
        self.intro = pg.transform.scale(self.intro, (600, 357))
        self.intro_button = self.intro.get_rect()
        self.intro_button.centerx = game.screen.get_rect().centerx
        self.intro_button.centery = game.screen.get_rect().centery - 100
        self.index = 1
        images = []
        for i in range(83):
            images.append(str(i+1))
        self.introTimer = Timer(self.game, images, wait=200, frameindex=0, step=1, looponce=False, sizex=500, sizey=350)

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.game.screen.blit(self.ply, self.ply_button)
        temp = self.introTimer.imagerect()
        self.game.screen.blit(temp.image, self.intro_button)

    def button_clicks(self):
        ply_clicked = self.ply_button.collidepoint(pg.mouse.get_pos())
        if ply_clicked:
            self.viewMenu = False
