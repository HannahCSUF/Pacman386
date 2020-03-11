import pygame
from timer import Timer


class Portal:
    NUM_FRAMES = 40

    def __init__(self, game, x, y, color, wait=200):
        self.game = game
        self.images = color
        self.x, self.y = x, y
        self.color = color
        self.opensize = Portal.NUM_FRAMES
        self.timeropening = Timer(self.game, images=color, wait=wait, frameindex=0, step=1, looponce=True, sizex=40)
        idx = len(self.images) - 1
        self.timerclosing = Timer(self.game, images=color, wait=wait, frameindex=idx, step=-1, looponce=True, sizex=40)
        self.timer = None
        self.rect = pygame.Rect(x, y, self.opensize, self.opensize)
        self.rect.center = (x, y)
        self.isopen = False
        self.isclosed = False
        self.portal_opening = pygame.mixer.Sound("sounds/portal_open.wav")
        self.portal_closing = pygame.mixer.Sound("sounds/portal_close.wav")

    def __str__(self): return 'Portal(' + str(self.x) + ',' + str(self.y) + ')'

    def open(self, game):
        other = game.portals[0] if self == game.portals[1] else game.portals[0]
        if self.isopen:    # close open portal of same color and reopen it here
            self.close()
        if self.rect.colliderect(other.rect):   # if opening it will overlap other portal, close other too
            other.close()
        self.timer = self.timeropening
        self.timer.reset()
        pygame.mixer.Sound.play(self.portal_opening)
        self.isopen = True
        self.isclosed = False

    def close(self):
        if self.isclosed:
            return
        self.timer = self.timerclosing
        self.timer.reset()
        pygame.mixer.Sound.play(self.portal_closing)
        self.isopen = False
        self.isclosed = True

    def collide_with(self, rect):
        k = 4    # force tiny overlap
        ssmaller = self.rect.inflate(rect.width/k, rect.height/k)
        rsmaller = rect.inflate(rect.width/k, rect.height/k)
        return ssmaller.colliderect(rsmaller)
        # return self.rect.colliderect(rect)

    @staticmethod
    def attempt_transport(character, game):
        if not (game.portals[0].isopen and game.portals[1].isopen):
            return False
        char = character
        ocollide = game.portals[0].collide_with(char.rect)
        bcollide = game.portals[1].collide_with(char.rect)
        if not ocollide and not bcollide:
            return False
        other = game.portals[1] if ocollide else game.portals[0]
        # char.rect.x, char.rect.y = other.rect.x, other.rect.y
        char.rect.center = other.rect.center
        other.close()
        return True

    def draw(self):
        if not self.isopen and not self.isclosed:
            return
        imgrect = self.timer.imagerect()
        self.game.screen.blit(imgrect.image, self.rect)
